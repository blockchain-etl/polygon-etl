import logging
import requests

def publish_message_to_slack(
    webhook_url, message
) -> None:
    try:
        requests.post(webhook_url, json={"text": message})
    except Exception as e:
        logging.error(f"Failed to post alert to Slack: {e}")