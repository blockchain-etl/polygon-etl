import json
import logging
from typing import Dict

from airflow.models import Variable

from utils.discord import publish_message_to_discord
from utils.slack import publish_message_to_slack


environment = Variable.get('environment', 'dev')


def handle_dag_failure(context: Dict) -> None:
    """
    This function should be set as the value of 'on_failure_callback' option in the DAG definition.

    `context` is a dictionary of the kind returned by `get_template_context`. For details see:
    https://github.com/databricks/incubator-airflow/blob/master/airflow/models.py
    """
    dag_id = context["task_instance"].dag_id
    task_id = context["task_instance"].task_id
    log_url = context["task_instance"].log_url

    logging.info(
        f"Handling DAG failure: dag_id: {dag_id},"
        f"task_id: {task_id}, log_url: {log_url}, context: {context}",
    )

    platform = Variable.get(f"alert_platform", "discord")

    webhook_url = Variable.get(f"{platform}_alerts_webhook_url")
    if not webhook_url:
        return

    default_user_id = Variable.get(f"{platform}_alerts_default_owner")
    if not default_user_id:
        raise ValueError(f"`{platform}_alerts_default_owner` must be set because `{platform}_alerts_webhook_url` is set.")

    override_owner_ids = json.loads(Variable.get(f"{platform}_alerts_dag_owners", "{}"))
    relevant_user_ids_string = override_owner_ids.get(dag_id, default_user_id)
    relevant_user_ids = relevant_user_ids_string.split(",")
    owner_tags = [f"<@{relevant_user_id}>" for relevant_user_id in relevant_user_ids]
    owner_text = owner_tags.join(", ")

    message = (
        f'Failed DAG **{dag_id}**\n'
        f'Task: **{task_id}**\n'
        f'Environment: **{environment}**\n'
        f'Logs: {log_url}\n'
        f'Owner: {owner_text}'
    )

    if platform == "discord":
        publish_message_to_discord(webhook_url, message)
    elif platform == "slack":
        publish_message_to_slack(webhook_url, message)
    else:
        raise ValueError(f"Allowed values for `alert_platform` are `discord` and `slack`.")