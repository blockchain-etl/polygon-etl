from __future__ import print_function

import collections
import logging
import os
from datetime import datetime, timedelta

from airflow import models
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from google.cloud import bigquery

from polygonetl_airflow.bigquery_utils import share_dataset_all_users_read
from polygonetl_airflow.common import read_json_file, get_list_of_files
from polygonetl_airflow.parse.parse_dataset_folder_logic import parse_dataset_folder
from polygonetl_airflow.parse.parse_state_manager import ParseStateManager

from utils.error_handling import handle_dag_failure

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

dags_folder = os.environ.get('DAGS_FOLDER', '/home/airflow/gcs/dags')


def build_parse_dag(
        dag_id,
        output_bucket,
        dataset_folder,
        parse_destination_dataset_project_id,
        source_project_id,
        source_dataset_name,
        internal_project_id,
        notification_emails=None,
        parse_start_date=datetime(2020, 5, 30),
        parse_schedule='0 0 * * *',
        parse_all_partitions=None,
):

    logging.info('parse_all_partitions is {}'.format(parse_all_partitions))

    PARTITION_DAG_ID = 'polygon_partition_dag'

    default_dag_args = {
        'depends_on_past': True,
        'start_date': parse_start_date,
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 5,
        'retry_delay': timedelta(minutes=5),
        'on_failure_callback': handle_dag_failure,
    }

    if notification_emails and len(notification_emails) > 0:
        default_dag_args['email'] = [email.strip() for email in notification_emails.split(',')]

    dag = models.DAG(
        dag_id,
        catchup=False,
        schedule=parse_schedule,
        default_args=default_dag_args)

    def create_parse_task():

        def parse_task(ds, **kwargs):
            validate_definition_files(dataset_folder)
            client = bigquery.Client()

            parse_dataset_folder(
                bigquery_client=client,
                dataset_folder=dataset_folder,
                ds=ds,
                source_project_id=source_project_id,
                source_dataset_name=source_dataset_name,
                destination_project_id=parse_destination_dataset_project_id,
                internal_project_id=internal_project_id,
                parse_state_manager=ParseStateManager(dataset_name, output_bucket, 'parse/state'),
                sqls_folder=os.path.join(dags_folder, 'resources/stages/parse/sqls'),
                parse_all_partitions=parse_all_partitions
            )

        dataset_name = get_dataset_name(dataset_folder)
        parsing_operator = PythonOperator(
            task_id=f'parse_tables_{dataset_name}',
            python_callable=parse_task,
            execution_timeout=timedelta(minutes=60 * 4),
            dag=dag
        )

        return parsing_operator

    def create_share_dataset_task(dataset_name):
        def share_dataset_task(**_):
            if parse_destination_dataset_project_id != "blockchain-etl":
                logging.info("Skipping sharing dataset.")
            else:
                client = bigquery.Client()
                share_dataset_all_users_read(
                    client, f"{parse_destination_dataset_project_id}.{dataset_name}"
                )
                share_dataset_all_users_read(
                    client,
                    f"{parse_destination_dataset_project_id}-internal.{dataset_name}",
                )

        return PythonOperator(
            task_id="share_dataset",
            python_callable=share_dataset_task,
            execution_timeout=timedelta(minutes=10),
            dag=dag,
        )

    wait_for_polygon_partition_dag_task = ExternalTaskSensor(
        task_id='wait_for_polygon_partition_dag',
        external_dag_id=PARTITION_DAG_ID,
        external_task_id='done',
        execution_delta=timedelta(minutes=30),
        priority_weight=0,
        mode='reschedule',
        retries=20,
        poke_interval=5 * 60,
        timeout=60 * 60 * 30,
        dag=dag)

    parse_task = create_parse_task()
    wait_for_polygon_partition_dag_task >> parse_task
    
    checkpoint_task = BashOperator(
        task_id='parse_all_checkpoint',
        bash_command='echo parse_all_checkpoint',
        dag=dag
    )

    parse_task >> checkpoint_task

    sql_files = get_list_of_files(dataset_folder, '*.sql')
    logging.info(sql_files)

    # TODO: Use folder name as dataset name and remove dataset_name in JSON definitions.
    dataset_name = os.path.basename(dataset_folder)
    full_dataset_name = 'polygon_' + dataset_name

    share_dataset_task = create_share_dataset_task(full_dataset_name)
    checkpoint_task >> share_dataset_task

    return dag


def validate_definition_files(dataset_folder):
    json_files = get_list_of_files(dataset_folder, '*.json')
    dataset_folder_name = get_dataset_name(dataset_folder)

    all_lowercase_table_names = []
    for json_file in json_files:
        file_name = json_file.split('/')[-1].replace('.json', '')

        table_definition = read_json_file(json_file)
        table = table_definition.get('table')
        if not table:
            raise ValueError(f'table is empty in file {json_file}')

        dataset_name = table.get('dataset_name')
        if not dataset_name:
            raise ValueError(f'dataset_name is empty in file {json_file}')
        if dataset_folder_name != dataset_name:
            raise ValueError(f'dataset_name {dataset_name} is not equal to dataset_folder_name {dataset_folder_name}')

        table_name = table.get('table_name')
        if not table_name:
            raise ValueError(f'table_name is empty in file {json_file}')
        if file_name != table_name:
            raise ValueError(f'file_name {file_name} doest match the table_name {table_name}')
        all_lowercase_table_names.append(table_name.lower())

    table_name_counts = collections.defaultdict(lambda: 0)
    for table_name in all_lowercase_table_names:
        table_name_counts[table_name] += 1

    non_unique_table_names = [name for name, count in table_name_counts.items() if count > 1]

    if len(non_unique_table_names) > 0:
        raise ValueError(f'The following table names are not unique {",".join(non_unique_table_names)}')


def get_dataset_name(dataset_folder):
    return dataset_folder.split('/')[-1]
