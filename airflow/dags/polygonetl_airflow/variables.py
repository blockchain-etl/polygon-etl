from datetime import datetime

from airflow.models import Variable


def read_export_dag_vars(var_prefix, **kwargs):
    """Read Airflow variables for Export DAG"""
    export_start_date = read_var('export_start_date', var_prefix, True, **kwargs)
    export_start_date = datetime.strptime(export_start_date, '%Y-%m-%d')

    export_end_date = read_var('export_end_date', var_prefix, False, **kwargs)
    export_end_date = datetime.strptime(export_end_date, '%Y-%m-%d') if export_end_date is not None else None

    provider_uris = read_var('provider_uris', var_prefix, True, **kwargs)
    provider_uris = [uri.strip() for uri in provider_uris.split(',')]

    provider_uris_archival = read_var('provider_uris_archival', var_prefix, True, **kwargs)
    provider_uris_archival = [uri.strip() for uri in provider_uris_archival.split(',')]

    export_max_active_runs = read_var('export_max_active_runs', var_prefix, False, **kwargs)
    export_max_active_runs = int(export_max_active_runs) if export_max_active_runs is not None else None

    export_max_active_tasks = read_var('export_max_active_tasks', var_prefix, False, **kwargs)
    export_max_active_tasks = int(export_max_active_tasks) if export_max_active_tasks is not None else None

    vars = {
        'output_bucket': read_var('output_bucket', var_prefix, True, **kwargs),
        'export_start_date': export_start_date,
        'export_end_date': export_end_date,
        'export_schedule_interval': read_var('export_schedule_interval', var_prefix, True, **kwargs),
        'provider_uris': provider_uris,
        'provider_uris_archival': provider_uris_archival,
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
        'export_max_active_runs': export_max_active_runs,
        'export_max_active_tasks': export_max_active_tasks,
        'export_max_workers': int(read_var('export_max_workers', var_prefix, True, **kwargs)),
        'export_traces_max_workers': int(read_var('export_traces_max_workers', var_prefix, True, **kwargs)),
    }

    return vars


def read_load_dag_vars(var_prefix, **kwargs):
    """Read Airflow variables for Load DAG"""
    output_bucket = read_var('output_bucket', var_prefix, True, **kwargs)
    checkpoint_bucket = read_var('checkpoint_bucket', var_prefix, False, **kwargs)
    if not checkpoint_bucket:
        checkpoint_bucket = output_bucket
    vars = {
        'output_bucket': output_bucket,
        'checkpoint_bucket': checkpoint_bucket,
        'destination_dataset_project_id': read_var('destination_dataset_project_id', var_prefix, True, **kwargs),
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
        # 'success_notification_emails': read_var('success_notification_emails', None, False, **kwargs),
        'load_schedule_interval': read_var('load_schedule_interval', var_prefix, True, **kwargs),
        'load_all_partitions': parse_bool(read_var('load_all_partitions', var_prefix, False, **kwargs), default=None),
    }

    load_end_date = read_var('load_end_date', var_prefix, False, **kwargs)
    if load_end_date is not None:
        load_end_date = datetime.strptime(load_end_date, '%Y-%m-%d')
        vars['load_end_date'] = load_end_date

    return vars


def read_partition_dag_vars(var_prefix, **kwargs):
    vars = {
        # public_project_id arg takes its value from destination_dataset_project_id
        "public_project_id": read_var(
            "destination_dataset_project_id", var_prefix, True, **kwargs
        ),
        "partitioned_project_id": read_var(
            "partitioned_project_id", var_prefix, True, **kwargs
        ),
        "partition_schedule_interval": read_var(
            "partition_schedule_interval", var_prefix, False, **kwargs
        ),
        "notification_emails": read_var("notification_emails", None, False, **kwargs),
    }

    partition_start_date = read_var("partition_start_date", var_prefix, False, **kwargs)
    if partition_start_date is not None:
        partition_start_date = datetime.strptime(partition_start_date, "%Y-%m-%d")
        vars["partition_start_date"] = partition_start_date

    return vars


def read_parse_dag_vars(var_prefix, dataset, **kwargs):
    per_dataset_var_prefix = var_prefix + dataset + '_'
    vars = {
        # source_project_id takes its value from destination_dataset_project_id
        'source_project_id': read_var('destination_dataset_project_id', var_prefix, True, **kwargs),
        # internal_project_id takes its value from partitioned_project_id
        'internal_project_id': read_var('partitioned_project_id', var_prefix, True, **kwargs),
        'parse_destination_dataset_project_id': read_var('parse_destination_dataset_project_id', var_prefix, True, **kwargs),
        'parse_schedule_interval': read_var('parse_schedule_interval', var_prefix, True, **kwargs),
        'parse_all_partitions': parse_bool(read_var('parse_all_partitions', per_dataset_var_prefix, False), default=None),
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
    }

    parse_start_date = read_var('parse_start_date', var_prefix, False, **kwargs)
    if parse_start_date is not None:
        parse_start_date = datetime.strptime(parse_start_date, '%Y-%m-%d')
        vars['parse_start_date'] = parse_start_date

    return vars
    
def read_verify_streaming_dag_vars(var_prefix, **kwargs):
    vars = {
        'destination_dataset_project_id': read_var('destination_dataset_project_id', var_prefix, True, **kwargs),
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
    }

    max_lag_in_minutes = read_var('max_lag_in_minutes', var_prefix, False, **kwargs)
    if max_lag_in_minutes is not None:
        vars['max_lag_in_minutes'] = max_lag_in_minutes

    return vars


def read_var(var_name, var_prefix=None, required=False, **kwargs):
    """Read Airflow variable"""
    full_var_name = f'{var_prefix}{var_name}' if var_prefix is not None else var_name
    var = Variable.get(full_var_name, '')
    var = var if var != '' else None
    if var is None:
        var = kwargs.get(var_name)
    if required and var is None:
        raise ValueError(f'{full_var_name} variable is required')
    return var


def parse_bool(bool_string, default=True):
    if isinstance(bool_string, bool):
        return bool_string
    if bool_string is None or len(bool_string) == 0:
        return default
    else:
        return bool_string.lower() in ["true", "yes"]
