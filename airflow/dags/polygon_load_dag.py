from __future__ import print_function

import logging

from polygonetl_airflow.build_load_dag import build_load_dag
from polygonetl_airflow.variables import read_load_dag_vars

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# airflow DAG
DAG = build_load_dag(
    dag_id='polygon_load_dag',
    chain='polygon',
    **read_load_dag_vars(
        var_prefix='polygon_',
        load_schedule_interval='0 6 * * *'
    )
)
