# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from pathlib import Path

import pytest
from airflow.models import DagBag, Variable

DAGS_FOLDER = f"{Path(__file__).resolve().parent.parent}/dags"

# Add to PATH to fix relative imports, like Airflow running dynamically
# https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html#built-in-pythonpath-entries-in-airflow
sys.path.append(DAGS_FOLDER)

MOCK_ENV_VARS = {
    "AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT": "google-cloud-platform://",
    "DAGS_FOLDER": DAGS_FOLDER,
}

# Airflow Variables cannot be created using env vars before version 1.10.10
MOCK_AIRFLOW_VARS = {
    "discord_alerts_dag_owners": '{"dummy_dag": "test_discord_alerts_dag_owner"}',
    "discord_alerts_default_owner": "test_discord_alerts_default_owner",
    "discord_alerts_webhook_url": "test_discord_alerts_webhook_url",
    "environment": "test_environment",
    "notification_emails": "test_notification_emails@foo.bar",
    "polygon_checkpoint_bucket": "test_polygon_checkpoint_bucket",
    "polygon_destination_dataset_project_id": "test_polygon_destination_dataset_project_id",
    "polygon_export_max_active_runs": "1",
    "polygon_export_max_workers": "30",
    "polygon_export_start_date": "1970-01-01",
    "polygon_export_traces_max_workers": "10",
    "polygon_load_all_partitions": "False",
    "polygon_max_lag_in_minutes": "30",
    "polygon_output_bucket": "test_polygon_output_bucket",
    "polygon_parse_destination_dataset_project_id": "test_polygon_parse_destination_dataset_project_id",
    "polygon_provider_uris": "test_polygon_provider_uri_0, test_polygon_provider_uri_1",
    "polygon_provider_uris_archival": "test_polygon_provider_uri_archival",
}


@pytest.fixture(autouse=True)
def env_vars_setup(monkeypatch):
    for k, v in MOCK_ENV_VARS.items():
        monkeypatch.setenv(k, v)


@pytest.fixture
def dag_bag(monkeypatch):
    monkeypatch.setattr(Variable, "get", MOCK_AIRFLOW_VARS.get)
    yield DagBag(dag_folder=DAGS_FOLDER, include_examples=False)


def test_no_import_errors(dag_bag):
    assert len(dag_bag.import_errors) == 0, "No Import Failures"


def test_dag_ids(dag_bag):
    expected_dag_ids = [
        "polygon_export_dag",
        "polygon_load_dag",
        "polygon_parse_balancer_dag",
        "polygon_parse_common_dag",
        "polygon_parse_dfyn_dag",
        "polygon_parse_instadapp_dag",
        "polygon_parse_polygon_dag",
        "polygon_parse_quickswap_dag",
        "polygon_parse_sushiswap_dag",
        "polygon_parse_uniswap_dag",
        "polygon_partition_dag",
        "polygon_verify_streaming_dag",
    ]
    assert sorted(dag_bag.dag_ids) == expected_dag_ids
