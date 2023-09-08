from __future__ import print_function

from datetime import datetime

from polygonetl_airflow.build_export_dag import build_export_dag
from polygonetl_airflow.variables import read_export_dag_vars, read_var

# airflow DAG


provider_uris_archival=read_var('provider_uris_archival_backfill', "polygon_", True)

v = read_export_dag_vars(
    var_prefix='polygon_',
    export_schedule='0 2 * * *',
    export_start_date='2020-05-30',
    export_max_active_runs=1,
    export_max_active_tasks=12,
    export_max_workers=5,
    export_traces_max_workers=10,
)
v['provider_uris_archival'] = [provider_uris_archival]
export_start_date = '2020-05-30'
export_start_date = datetime.strptime(export_start_date, '%Y-%m-%d')
v['export_start_date'] = export_start_date


DAG = build_export_dag(
    dag_id='backfill_polygon_export_dag',
    backfill=True,
    **v
)
