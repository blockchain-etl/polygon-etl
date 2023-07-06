from __future__ import print_function

import json
import logging
import os
import time
from datetime import datetime, timedelta

from airflow import models
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from google.cloud import bigquery
from google.cloud.bigquery import TimePartitioning

from polygonetl_airflow.bigquery_utils import submit_bigquery_job

from utils.error_handling import handle_dag_failure

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def build_load_dag(
    dag_id,
    output_bucket,
    destination_dataset_project_id,
    chain='polygon',
    notification_emails=None,
    load_start_date=datetime(2018, 7, 1),
    load_end_date=None,
    load_catchup=False,
    load_schedule='0 0 * * *',
    load_all_partitions=True
):
    # The following datasets must be created in BigQuery:
    # - crypto_{chain}_raw
    # - crypto_{chain}_temp
    # - crypto_{chain}

    dataset_name = f'crypto_{chain}'
    dataset_name_raw = f'crypto_{chain}_raw'
    dataset_name_temp = f'crypto_{chain}_temp'

    if not destination_dataset_project_id:
        raise ValueError('destination_dataset_project_id is required')

    environment = {
        'dataset_name': dataset_name,
        'dataset_name_raw': dataset_name_raw,
        'dataset_name_temp': dataset_name_temp,
        'destination_dataset_project_id': destination_dataset_project_id,
        'load_all_partitions': load_all_partitions
    }

    def read_bigquery_schema_from_file(filepath):
        result = []
        file_content = read_file(filepath)
        json_content = json.loads(file_content)
        for field in json_content:
            result.append(bigquery.SchemaField(
                name=field.get('name'),
                field_type=field.get('type', 'STRING'),
                mode=field.get('mode', 'NULLABLE'),
                description=field.get('description')))
        return result

    def read_file(filepath):
        with open(filepath) as file_handle:
            content = file_handle.read()
            return content

    default_dag_args = {
        'depends_on_past': False,
        'start_date': load_start_date,
        'end_date': load_end_date,
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 5,
        'retry_delay': timedelta(minutes=5),
        'on_failure_callback': handle_dag_failure,
    }

    if notification_emails and len(notification_emails) > 0:
        default_dag_args['email'] = [email.strip() for email in notification_emails.split(',')]

    # Define a DAG (directed acyclic graph) of tasks.
    dag = models.DAG(
        dag_id,
        catchup=load_catchup,
        schedule=load_schedule,
        default_args=default_dag_args)

    dags_folder = os.environ.get('DAGS_FOLDER', '/home/airflow/gcs/dags')

    if not load_all_partitions:
        wait_sensor = ExternalTaskSensor(
            task_id="wait_export_dag",
            external_dag_id=f"{chain}_export_dag",
            external_task_id="export_complete",
            execution_delta=timedelta(hours=5),
            priority_weight=0,
            mode="reschedule",
            poke_interval=5 * 60,
            timeout=8 * 60 * 60,
            dag=dag,
        )

    def add_load_tasks(task, file_format, allow_quoted_newlines=False):
        def load_task(ds, **kwargs):
            client = bigquery.Client()
            job_config = bigquery.LoadJobConfig()
            schema_path = os.path.join(dags_folder, 'resources/stages/raw/schemas/{task}.json'.format(task=task))
            job_config.schema = read_bigquery_schema_from_file(schema_path)
            job_config.source_format = bigquery.SourceFormat.CSV if file_format == 'csv' else bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            if file_format == 'csv':
                job_config.skip_leading_rows = 1
            job_config.write_disposition = 'WRITE_TRUNCATE'
            job_config.allow_quoted_newlines = allow_quoted_newlines
            job_config.ignore_unknown_values = True

            export_location_uri = 'gs://{bucket}/export'.format(bucket=output_bucket)
            if load_all_partitions:
                # Support export files that are missing EIP-1559 fields (exported before EIP-1559 upgrade)
                job_config.allow_jagged_rows = True

                uri = "{export_location_uri}/{task}/*.{file_format}".format(
                    export_location_uri=export_location_uri,
                    task=task,
                    file_format=file_format,
                )
                table_ref = client.dataset(dataset_name_raw).table(task)
            else:
                uri = "{export_location_uri}/{task}/block_date={ds}/*.{file_format}".format(
                    export_location_uri=export_location_uri,
                    task=task,
                    ds=ds,
                    file_format=file_format,
                )
                table_name = f'{task}_{ds.replace("-", "_")}'
                table_ref = client.dataset(dataset_name_raw).table(table_name)

            load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
            submit_bigquery_job(load_job, job_config)
            assert load_job.state == 'DONE'

            if not load_all_partitions:
                table = client.get_table(table_ref)
                table.expires = datetime.now() + timedelta(days=3)
                client.update_table(table, ["expires"])

        load_operator = PythonOperator(
            task_id='load_{task}'.format(task=task),
            python_callable=load_task,
            execution_timeout=timedelta(minutes=30),
            dag=dag
        )

        if not load_all_partitions:
            wait_sensor >> load_operator

        return load_operator

    def add_enrich_tasks(task, time_partitioning_field='block_timestamp', dependencies=None, always_load_all_partitions=False):
        def enrich_task(ds, **kwargs):
            template_context = kwargs.copy()
            template_context['ds'] = ds
            template_context['params'] = environment

            if load_all_partitions or always_load_all_partitions:
                template_context["params"]["ds_postfix"] = ""
            else:
                template_context["params"]["ds_postfix"] = "_" + ds.replace("-", "_")

            client = bigquery.Client()

            # Need to use a temporary table because bq query sets field modes to NULLABLE and descriptions to null
            # when writeDisposition is WRITE_TRUNCATE

            # Create a temporary table
            temp_table_name = '{task}_{milliseconds}'.format(task=task, milliseconds=int(round(time.time() * 1000)))
            temp_table_ref = client.dataset(dataset_name_temp).table(temp_table_name)

            schema_path = os.path.join(dags_folder, 'resources/stages/enrich/schemas/{task}.json'.format(task=task))
            schema = read_bigquery_schema_from_file(schema_path)
            table = bigquery.Table(temp_table_ref, schema=schema)

            description_path = os.path.join(
                dags_folder, 'resources/stages/enrich/descriptions/{task}.txt'.format(task=task))
            table.description = read_file(description_path)
            if time_partitioning_field is not None:
                table.time_partitioning = TimePartitioning(field=time_partitioning_field)
            logging.info('Creating table: ' + json.dumps(table.to_api_repr()))
            table = client.create_table(table)
            assert table.table_id == temp_table_name

            # Query from raw to temporary table
            query_job_config = bigquery.QueryJobConfig()
            # Finishes faster, query limit for concurrent interactive queries is 50
            query_job_config.priority = bigquery.QueryPriority.INTERACTIVE
            query_job_config.destination = temp_table_ref

            sql_path = os.path.join(dags_folder, 'resources/stages/enrich/sqls/{task}.sql'.format(task=task))
            sql_template = read_file(sql_path)
            sql = kwargs['task'].render_template(sql_template, template_context)
            print('Enrichment sql:')
            print(sql)

            query_job = client.query(sql, location='US', job_config=query_job_config)
            submit_bigquery_job(query_job, query_job_config)
            assert query_job.state == 'DONE'

            if load_all_partitions or always_load_all_partitions:
                # Copy temporary table to destination
                copy_job_config = bigquery.CopyJobConfig()
                copy_job_config.write_disposition = 'WRITE_TRUNCATE'
                dest_table_name = '{task}'.format(task=task)
                dest_table_ref = client.dataset(dataset_name, project=destination_dataset_project_id).table(dest_table_name)
                copy_job = client.copy_table(temp_table_ref, dest_table_ref, location='US', job_config=copy_job_config)
                submit_bigquery_job(copy_job, copy_job_config)
                assert copy_job.state == 'DONE'
            else:
                # Merge
                # https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement
                merge_job_config = bigquery.QueryJobConfig()
                # Finishes faster, query limit for concurrent interactive queries is 50
                merge_job_config.priority = bigquery.QueryPriority.INTERACTIVE

                merge_sql_path = os.path.join(
                    dags_folder, 'resources/stages/enrich/sqls/merge/merge_{task}.sql'.format(task=task))
                merge_sql_template = read_file(merge_sql_path)

                merge_template_context = template_context.copy()
                merge_template_context['params']['source_table'] = temp_table_name
                merge_template_context['params']['destination_dataset_project_id'] = destination_dataset_project_id
                merge_template_context['params']['destination_dataset_name'] = dataset_name
                merge_sql = kwargs['task'].render_template(merge_sql_template, merge_template_context)
                print('Merge sql:')
                print(merge_sql)
                merge_job = client.query(merge_sql, location='US', job_config=merge_job_config)
                submit_bigquery_job(merge_job, merge_job_config)
                assert merge_job.state == 'DONE'

            # Delete temp table
            client.delete_table(temp_table_ref)

        enrich_operator = PythonOperator(
            task_id='enrich_{task}'.format(task=task),
            python_callable=enrich_task,
            execution_timeout=timedelta(minutes=60),
            dag=dag
        )

        if dependencies is not None and len(dependencies) > 0:
            for dependency in dependencies:
                dependency >> enrich_operator
        return enrich_operator

    def add_verify_tasks(task, dependencies=None):
        # The queries in verify/sqls will fail when the condition is not met
        # Have to use this trick since the Python 2 version of BigQueryCheckOperator doesn't support standard SQL
        # and legacy SQL can't be used to query partitioned tables.
        sql_path = os.path.join(dags_folder, 'resources/stages/verify/sqls/{task}.sql'.format(task=task))
        sql = read_file(sql_path)
        verify_task = BigQueryInsertJobOperator(
            task_id=f"verify_{task}",
            configuration={"query": {"query": sql, "useLegacySql": False}},
            params=environment,
            dag=dag,
        )
        if dependencies is not None and len(dependencies) > 0:
            for dependency in dependencies:
                dependency >> verify_task
        return verify_task

    def add_load_metadata_tasks(dependencies=None):
        load_metadata_query_path = os.path.join(dags_folder, 'resources/stages/load_metadata/sqls/load_metadata.sql')
        load_metadata_query = read_file(load_metadata_query_path)
        load_metadata_schema_path = os.path.join(dags_folder, 'resources/stages/load_metadata/schemas/load_metadata.json')
        load_metadata_schema = read_file(load_metadata_schema_path)

        load_metadata_task = BigQueryInsertJobOperator(
            task_id="load_metadata_task",
            configuration={
                "query": {
                    "destinationTable": {
                        "projectId": destination_dataset_project_id,
                        "datasetId": dataset_name,
                        "tableId": "load_metadata",
                    },
                    "schema": {"fields": json.loads(load_metadata_schema)},
                    "createDisposition": "CREATE_IF_NEEDED",
                    "writeDisposition": "WRITE_APPEND",
                    "query": load_metadata_query,
                    "useLegacySql": False,
                },
            },
            params={
                "chain": chain,
                "load_all_partitions": load_all_partitions,
            },
            dag=dag,
        )

        if dependencies is not None and len(dependencies) > 0:
            for dependency in dependencies:
                dependency >> load_metadata_task
        return load_metadata_task

    load_blocks_task = add_load_tasks('blocks', 'csv')
    load_transactions_task = add_load_tasks('transactions', 'csv')
    load_receipts_task = add_load_tasks('receipts', 'csv')
    load_logs_task = add_load_tasks('logs', 'json')
    load_contracts_task = add_load_tasks('contracts', 'json')
    load_tokens_task = add_load_tasks('tokens', 'csv', allow_quoted_newlines=True)
    load_token_transfers_task = add_load_tasks('token_transfers', 'csv')
    load_traces_task = add_load_tasks('traces', 'csv')

    enrich_blocks_task = add_enrich_tasks(
        'blocks', time_partitioning_field='timestamp', dependencies=[load_blocks_task])
    enrich_transactions_task = add_enrich_tasks(
        'transactions', dependencies=[load_blocks_task, load_transactions_task, load_receipts_task])
    enrich_logs_task = add_enrich_tasks(
        'logs', dependencies=[load_blocks_task, load_logs_task])
    enrich_token_transfers_task = add_enrich_tasks(
        'token_transfers', dependencies=[load_blocks_task, load_token_transfers_task])
    enrich_traces_task = add_enrich_tasks(
        'traces', dependencies=[load_blocks_task, load_traces_task])
    enrich_contracts_task = add_enrich_tasks(
        'contracts', dependencies=[load_blocks_task, load_contracts_task])
    enrich_tokens_task = add_enrich_tasks(
        'tokens', dependencies=[load_blocks_task, load_tokens_task])

    verify_blocks_count_task = add_verify_tasks('blocks_count', [enrich_blocks_task])
    verify_blocks_have_latest_task = add_verify_tasks('blocks_have_latest', [enrich_blocks_task])
    verify_transactions_count_task = add_verify_tasks('transactions_count',
                                                      [enrich_blocks_task, enrich_transactions_task])
    verify_transactions_have_latest_task = add_verify_tasks('transactions_have_latest', [enrich_transactions_task])
    verify_logs_have_latest_task = add_verify_tasks('logs_have_latest', [enrich_logs_task])
    verify_token_transfers_have_latest_task = add_verify_tasks('token_transfers_have_latest',
                                                               [enrich_token_transfers_task])

    # Load metadata tasks #

    add_load_metadata_tasks(dependencies=[
        verify_blocks_count_task,
        verify_blocks_have_latest_task,
        verify_transactions_count_task,
        verify_transactions_have_latest_task,
        verify_logs_have_latest_task,
        verify_token_transfers_have_latest_task,
        enrich_traces_task,
        enrich_contracts_task,
        enrich_tokens_task,
    ])

    return dag
