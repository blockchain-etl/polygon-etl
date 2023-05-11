from __future__ import print_function

import os
import logging
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from airflow import DAG, configuration
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from polygonetl.cli import (
    get_block_range_for_date,
    get_block_range_for_timestamps,
    extract_csv_column,
    export_blocks_and_transactions,
    export_receipts_and_logs,
    extract_contracts,
    extract_tokens,
    extract_token_transfers,
    export_geth_traces,
    extract_geth_traces
)
from polygonetl_airflow.gcs_utils import download_from_gcs, upload_to_gcs
from utils.error_handling import handle_dag_failure

# Use Composer's suggested Data folder for temp storage
# This is a folder in the Composer Bucket, mounted locally using gcsfuse
# Overcomes the 10GB ephemerol storage limit on workers (imposed by GKE Autopilot)
# https://cloud.google.com/composer/docs/composer-2/cloud-storage
COMPOSER_DATA_FOLDER = Path("/home/airflow/gcs/data/")
TEMP_DIR = COMPOSER_DATA_FOLDER if COMPOSER_DATA_FOLDER.exists() else None


def build_export_dag(
    dag_id,
    provider_uris,
    provider_uris_archival,
    output_bucket,
    export_start_date,
    export_end_date=None,
    notification_emails=None,
    export_schedule='0 0 * * *',
    export_max_workers=10,
    export_traces_max_workers=10,
    export_batch_size=200,
    export_max_active_runs=None,
    export_max_active_tasks=None,
    export_retries=5,
    **kwargs
):
    default_dag_args = {
        "depends_on_past": False,
        "start_date": export_start_date,
        "end_date": export_end_date,
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": export_retries,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": handle_dag_failure,
    }

    if notification_emails and len(notification_emails) > 0:
        default_dag_args['email'] = [email.strip() for email in notification_emails.split(',')]

    export_daofork_traces_option = False
    export_genesis_traces_option = True
    export_blocks_and_transactions_toggle = True
    export_receipts_and_logs_toggle = True
    extract_contracts_toggle = True
    extract_tokens_toggle = True
    extract_token_transfers_toggle = True
    export_traces_toggle = True
    export_traces_from_gcs = False

    if export_max_active_runs is None:
        export_max_active_runs = configuration.conf.getint('core', 'max_active_runs_per_dag')

    if export_max_active_tasks is None:
        export_max_active_tasks = configuration.conf.getint('core', 'max_active_tasks_per_dag')

    dag = DAG(
        dag_id,
        schedule=export_schedule,
        default_args=default_dag_args,
        max_active_runs=export_max_active_runs,
        max_active_tasks=export_max_active_tasks,
    )

    from airflow.providers.google.cloud.hooks.gcs import GCSHook
    cloud_storage_hook = GCSHook(gcp_conn_id="google_cloud_default")

    # Export
    def export_path(directory, date):
        return "export/{directory}/block_date={block_date}/".format(
            directory=directory, block_date=date.strftime("%Y-%m-%d")
        )

    def copy_to_export_path(file_path, export_path):
        logging.info('Calling copy_to_export_path({}, {})'.format(file_path, export_path))
        filename = os.path.basename(file_path)

   
       
        upload_to_gcs(
            gcs_hook=cloud_storage_hook,
            bucket=output_bucket,
            object=export_path + filename,
            filename=file_path)

    def copy_from_export_path(export_path, file_path):
        logging.info('Calling copy_from_export_path({}, {})'.format(export_path, file_path))
        filename = os.path.basename(file_path)
        
        download_from_gcs(bucket=output_bucket, object=export_path + filename, filename=file_path)

    def get_block_range(tempdir, date, provider_uri, hour=None):
        if hour is None:
            block_range_filename = "blocks_meta.txt"

            logging.info(
                f"Calling get_block_range_for_date({provider_uri}, {date}, ...)"
            )
            get_block_range_for_date.callback(
                provider_uri=provider_uri,
                date=date,
                output=os.path.join(tempdir, block_range_filename),
            )
        else:
            block_range_filename = f"blocks_meta_{hour:02}.txt"

            start_datetime = datetime.combine(
                date,
                time(hour=hour, minute=0, second=0, tzinfo=timezone.utc),
            )
            end_datetime = datetime.combine(
                date,
                time(hour=hour, minute=59, second=59, tzinfo=timezone.utc),
            )

            logging.info(
                "Calling get_block_range_for_timestamp"
                f"({provider_uri}, {start_datetime} to {end_datetime}, ...)"
            )
            get_block_range_for_timestamps.callback(
                provider_uri=provider_uri,
                start_timestamp=start_datetime.timestamp(),
                end_timestamp=end_datetime.timestamp(),
                output=os.path.join(tempdir, block_range_filename),
            )

        with open(os.path.join(tempdir, block_range_filename)) as block_range_file:
            block_range = block_range_file.read()
            start_block, end_block = block_range.split(",")

        return int(start_block), int(end_block)

    def export_blocks_and_transactions_command(logical_date, provider_uri, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            start_block, end_block = get_block_range(tempdir, logical_date, provider_uri)

            logging.info('Calling export_blocks_and_transactions({}, {}, {}, {}, {}, ...)'.format(
                start_block, end_block, export_batch_size, provider_uri, export_max_workers))

            export_blocks_and_transactions.callback(
                start_block=start_block,
                end_block=end_block,
                batch_size=export_batch_size,
                provider_uri=provider_uri,
                max_workers=export_max_workers,
                blocks_output=os.path.join(tempdir, "blocks.csv"),
                transactions_output=os.path.join(tempdir, "transactions.csv"),
            )

            copy_to_export_path(
                os.path.join(tempdir, "blocks_meta.txt"), export_path("blocks_meta", logical_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "blocks.csv"), export_path("blocks", logical_date)
            )

            copy_to_export_path(
                os.path.join(tempdir, "transactions.csv"), export_path("transactions", logical_date)
            )

    def export_receipts_and_logs_command(logical_date, provider_uri, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            copy_from_export_path(
                export_path("transactions", logical_date), os.path.join(tempdir, "transactions.csv")
            )

            logging.info('Calling extract_csv_column(...)')
            extract_csv_column.callback(
                input=os.path.join(tempdir, "transactions.csv"),
                output=os.path.join(tempdir, "transaction_hashes.txt"),
                column="hash",
            )

            logging.info('Calling export_receipts_and_logs({}, ..., {}, {}, ...)'.format(
                export_batch_size, provider_uri, export_max_workers))
            export_receipts_and_logs.callback(
                batch_size=export_batch_size,
                transaction_hashes=os.path.join(tempdir, "transaction_hashes.txt"),
                provider_uri=provider_uri,
                max_workers=export_max_workers,
                receipts_output=os.path.join(tempdir, "receipts.csv"),
                logs_output=os.path.join(tempdir, "logs.json"),
            )

            copy_to_export_path(
                os.path.join(tempdir, "receipts.csv"), export_path("receipts", logical_date)
            )
            copy_to_export_path(os.path.join(tempdir, "logs.json"), export_path("logs", logical_date))

    def extract_contracts_command(logical_date, hour, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            copy_from_export_path(
                export_path("traces", logical_date),
                os.path.join(tempdir, f"traces_{hour:02}.csv"),
            )

            logging.info('Calling extract_contracts(..., {}, {})'.format(
                export_batch_size, export_max_workers
            ))
            extract_contracts.callback(
                traces=os.path.join(tempdir, f"traces_{hour:02}.csv"),
                output=os.path.join(tempdir, f"contracts_{hour:02}.json"),
                batch_size=export_batch_size,
                max_workers=export_max_workers,
            )

            copy_to_export_path(
                os.path.join(tempdir, f"contracts_{hour:02}.json"),
                export_path("contracts", logical_date),
            )

    def extract_tokens_command(logical_date, provider_uri, hour, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            copy_from_export_path(
                export_path("contracts", logical_date),
                os.path.join(tempdir, f"contracts_{hour:02}.json"),
            )

            logging.info('Calling extract_tokens(..., {}, {})'.format(export_max_workers, provider_uri))
            extract_tokens.callback(
                contracts=os.path.join(tempdir, f"contracts_{hour:02}.json"),
                output=os.path.join(tempdir, f"tokens_{hour:02}.csv"),
                max_workers=export_max_workers,
                provider_uri=provider_uri,
            )

            copy_to_export_path(
                os.path.join(tempdir, f"tokens_{hour:02}.csv"),
                export_path("tokens", logical_date),
            )

    def extract_token_transfers_command(logical_date, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            copy_from_export_path(
                export_path("logs", logical_date), os.path.join(tempdir, "logs.json")
            )

            logging.info('Calling extract_token_transfers(..., {}, ..., {})'.format(
                export_batch_size, export_max_workers
            ))
            extract_token_transfers.callback(
                logs=os.path.join(tempdir, "logs.json"),
                batch_size=export_batch_size,
                output=os.path.join(tempdir, "token_transfers.csv"),
                max_workers=export_max_workers,
            )

            copy_to_export_path(
                os.path.join(tempdir, "token_transfers.csv"),
                export_path("token_transfers", logical_date),
            )

    def export_traces_command(logical_date, provider_uri, hour, **kwargs):
        with TemporaryDirectory(dir=TEMP_DIR) as tempdir:
            start_block, end_block = get_block_range(
                tempdir, logical_date, provider_uri, hour
            )
            if start_block == 0:
                start_block = 1

            export_traces_batch_size = 1
            logging.info('Calling export_geth_traces({}, {}, {}, ...,{}, {}, {}, {})'.format(
                start_block, end_block, export_traces_batch_size, export_max_workers, provider_uri,
                export_genesis_traces_option, export_daofork_traces_option
            ))

            if not export_traces_from_gcs:
                export_geth_traces.callback(
                    start_block=start_block,
                    end_block=end_block,
                    batch_size=export_traces_batch_size,
                    output=os.path.join(tempdir, f"geth_traces_{hour:02}.json"),
                    max_workers=export_traces_max_workers,
                    provider_uri=provider_uri,
                )
                copy_to_export_path(
                    os.path.join(tempdir, f"geth_traces_{hour:02}.json"),
                    export_path("traces", logical_date),
                )
            else:
                copy_from_export_path(
                   export_path("traces", logical_date),
                   os.path.join(tempdir, f"geth_traces_{hour:02}.json"), 
                )

            extract_geth_traces.callback(
                input=os.path.join(tempdir, f"geth_traces_{hour:02}.json"),
                output=os.path.join(tempdir, f"traces_{hour:02}.csv"),
                max_workers=1,
            )

            copy_to_export_path(
                os.path.join(tempdir, f"traces_{hour:02}.csv"),
                export_path("traces", logical_date),
            )

    def add_export_task(
        toggle,
        task_id,
        python_callable,
        op_kwargs=None,
        dependencies=None,
    ):
        if toggle:
            operator = PythonOperator(
                task_id=task_id,
                python_callable=python_callable,
                execution_timeout=timedelta(hours=24),
                op_kwargs=op_kwargs,
                dag=dag,
            )
            if dependencies is not None and len(dependencies) > 0:
                for dependency in dependencies:
                    if dependency is not None:
                        dependency >> operator
            return operator
        else:
            return None

    # Operators
    export_complete = EmptyOperator(task_id="export_complete", dag=dag)

    export_blocks_and_transactions_operator = add_export_task(
        export_blocks_and_transactions_toggle,
        "export_blocks_and_transactions",
        add_provider_uri_fallback_loop(export_blocks_and_transactions_command, provider_uris),
    )

    export_receipts_and_logs_operator = add_export_task(
        export_receipts_and_logs_toggle,
        "export_receipts_and_logs",
        add_provider_uri_fallback_loop(export_receipts_and_logs_command, provider_uris),
        dependencies=[export_blocks_and_transactions_operator],
    )

    extract_token_transfers_operator = add_export_task(
        extract_token_transfers_toggle,
        "extract_token_transfers",
        extract_token_transfers_command,
        dependencies=[export_receipts_and_logs_operator],
    )
    extract_token_transfers_operator >> export_complete

    for hour in range(24):
        export_traces_operator = add_export_task(
            export_traces_toggle,
            f"export_geth_traces_{hour:02}",
            add_provider_uri_fallback_loop(
                export_traces_command,
                provider_uris_archival,
            ),
            op_kwargs={"hour": hour},
        )

        extract_contracts_operator = add_export_task(
            extract_contracts_toggle,
            f"extract_contracts_{hour:02}",
            extract_contracts_command,
            op_kwargs={"hour": hour},
            dependencies=[export_traces_operator],
        )

        extract_tokens_operator = add_export_task(
            extract_tokens_toggle,
            f"extract_tokens_{hour:02}",
            add_provider_uri_fallback_loop(extract_tokens_command, provider_uris),
            op_kwargs={"hour": hour},
            dependencies=[extract_contracts_operator],
        )
        extract_tokens_operator >> export_complete

    return dag


def add_provider_uri_fallback_loop(python_callable, provider_uris):
    """Tries each provider uri in provider_uris until the command succeeds"""

    def python_callable_with_fallback(**kwargs):
        for index, provider_uri in enumerate(provider_uris):
            kwargs['provider_uri'] = provider_uri
            try:
                python_callable(**kwargs)
                break
            except Exception as e:
                if index < (len(provider_uris) - 1):
                    logging.exception('An exception occurred. Trying another uri')
                else:
                    raise e

    return python_callable_with_fallback
