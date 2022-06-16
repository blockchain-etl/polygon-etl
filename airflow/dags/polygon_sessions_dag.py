from __future__ import print_function
from airflow.models import Variable
from datetime import datetime
from polygonetl_airflow.build_sessions_dag import build_sessions_dag

import logging
import os

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

DAGS_FOLDER = os.environ.get('DAGS_FOLDER', '/home/airflow/gcs/dags')
sql_dir = os.path.join(DAGS_FOLDER, 'resources/stages/sessions/sqls')

environment = Variable.get('environment', 'prod')


# airflow DAG
DAG = build_sessions_dag(
    dag_id='polygon_sessions_dag',
    output_bucket=Variable.get('polygon_output_bucket'),
    sql_dir=sql_dir,
    source_project_id='public-data-finance',
    source_dataset_name='crypto_polygon',
    destination_project_id=Variable.get('polygon_destination_dataset_project_id'),
    # Variables default to the prod values. Override for dev environment.
    destination_dataset_name=Variable.get('polygon_destination_dataset_name', 'crypto_polygon'),
    temp_dataset_name=Variable.get('polygon_temp_dataset_name', 'crypto_polygon_temp'),
    # Load DAG should complete by 14:00.
    schedule_interval='0 14 * * *',
    start_date=datetime(2021, 11, 30),
    environment=environment
)
