## Cloud Build

In order to automate deployment of Airflow DAGs to the Cloud Composer bucket, perform the following steps:

- Navigate to Cloud Build Triggers console https://console.cloud.google.com/cloud-build/triggers.
- Click **Connect repository** button. Select **GitHub (Cloud Build GitHub App)**.
- Select `matic-etl` (if necessary click **Edit repositories on GitHub** and add permissions to read `matic-etl`).
- Click **Connect repository** button.
- Click **Create push trigger** button.
- Click **Edit** in the context menu for the `default-push-trigger-1` trigger.
- Specify the following configuration options for the trigger:
    - Event: `Push to a branch`
    - Source: `^master$`
    - Build configuration: `Cloud Build configuration file (yaml or json)`
    - Cloud Build configuration file location: `/airflow/cloudbuild.yaml`
    - Substitution variables (you can get the Cloud Composer bucket by running 
      `gcloud composer environments describe ${ENVIRONMENT_NAME} --location us-central1` and getting 
      the `dagGcsPrefix` config value, 
      where `${ENVIRONMENT_NAME}` is your Cloud Composer environment name):
        - `_BUCKET`: `<put_your_cloud_composer_bucket_here>`, e.g. `_BUCKET`: `us-central1-bigquery-test0--2dedb4dd-bucket`