from __future__ import print_function

from polygonetl_airflow.build_export_dag import build_export_dag
from polygonetl_airflow.variables import read_export_dag_vars

# airflow DAG
DAG = build_export_dag(
    dag_id='polygon_export_dag',
    **read_export_dag_vars(
        var_prefix='polygon_',
        export_schedule_interval='0 5 * * *',
        export_start_date='2020-05-30',
        export_max_active_runs=3,
        export_max_workers=5,
        export_traces_max_workers=10,
    )
)
