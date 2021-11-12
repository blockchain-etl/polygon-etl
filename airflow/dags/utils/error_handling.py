import json
import random
from typing import Dict

from airflow.models import Variable

from utils.discord import publish_message_to_discord


environment = Variable.get('environment', 'dev')


def handle_dag_failure(context: Dict) -> None:
    """
    This function should be set as the value of 'on_failure_callback' option in the DAG definition.

    `context` is a dictionary of the kind returned by `get_template_context`. For details see:
    https://github.com/databricks/incubator-airflow/blob/master/airflow/models.py
    """
    post_alert_to_discord(context)


def post_alert_to_discord(context: Dict) -> None:
    webhook_url = Variable.get("discord_alerts_webhook_url")
    if not webhook_url:
        return

    dag_id = context['task_instance'].dag_id
    task_id = context['task_instance'].task_id
    log_url = context['task_instance'].log_url

    default_user_id = Variable.get("discord_alerts_default_owner")
    if not default_user_id:
        raise ValueError("`discord_alerts_default_owner` must be set because `discord_alerts_webhook_url` is set.")

    override_owner_ids = json.loads(Variable.get("discord_alerts_dag_owners", "{}"))
    relevant_user_ids_string = override_owner_ids.get(dag_id, default_user_id)
    relevant_user_ids = relevant_user_ids_string.split(",")
    relevant_user_id = random.choice(relevant_user_ids)

    message = (
        f'Failed DAG **{dag_id}**\n'
        f'Task: **{task_id}**\n'
        f'Environment: **{environment}**\n'
        f'Logs: {log_url}\n'
        f'Owner: <@{relevant_user_id}>'
    )

    publish_message_to_discord(webhook_url, message)
