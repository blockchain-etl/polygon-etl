"""
In order to test this DAG, put it directly in the `dags` folder in the destination bucket.
"""

from datetime import datetime, timedelta

from airflow import models
from airflow.operators.python_operator import PythonOperator

from utils.error_handling import handle_dag_failure


def do_something():
    print("Doing something important...")
    raise Exception("A Lorem Ipsum error occurred.")


with models.DAG(
    "dummy_dag",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 11, 1),
    catchup=False,
    default_args={'on_failure_callback': handle_dag_failure},
) as dag:
    PythonOperator(
        task_id='do_something',
        python_callable=do_something,
    )
