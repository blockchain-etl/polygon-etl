from __future__ import print_function

import logging

from polygonetl_airflow.build_partition_dag import build_partition_dag
from polygonetl_airflow.variables import read_partition_dag_vars

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# airflow DAG
DAG = build_partition_dag(
    dag_id='polygon_partition_dag',
    load_dag_id='polygon_load_dag',
    partitioned_dataset_name = 'crypto_polygon_partitioned',
    public_dataset_name = 'crypto_polygon',
    **read_partition_dag_vars(
        var_prefix="polygon_",
        partition_schedule="0 8 * * *",
    ),
)
