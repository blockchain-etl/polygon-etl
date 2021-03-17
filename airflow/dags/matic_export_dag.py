from __future__ import print_function

from maticetl_airflow.build_export_dag import build_export_dag
from maticetl_airflow.variables import read_export_dag_vars

# airflow DAG
DAG = build_export_dag(
    dag_id='matic_export_dag',
    **read_export_dag_vars(
        var_prefix='matic_',
        export_schedule_interval='0 1 * * *',
        export_start_date='2020-05-30',
        export_max_active_runs=3,
        export_max_workers=10,
    )
)
