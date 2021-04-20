# polygon ETL Dataflow

[Apache Beam](https://beam.apache.org/) pipeline for moving polygon data from Pub/Sub to BigQuery.
Deployed in [Google Dataflow](https://cloud.google.com/dataflow).

## Setting Up

1. Create a GCS bucket used for staging and temp location:

   ```bash
   gcloud config set project <your_gcp_project>
   PROJECT=$(gcloud config get-value project 2> /dev/null)
   ENVIRONMENT_INDEX=0
   BUCKET=${PROJECT}-dataflow-${ENVIRONMENT_INDEX} && echo "${BUCKET}"
   gsutil mb gs://${BUCKET}/
   ```

2. Copy `exampleChainConfig.json` to `chainConfig.json` and update `chainConfig.json` with your values.

3. Start the Dataflow job in:

   ```bash
   mvn -e -Pdataflow-runner compile exec:java \
   -Dexec.mainClass=io.blockchainetl.polygon.PolygonPubSubToBigQueryPipeline \
   -Dexec.args="--chainConfigFile=chainConfig.json \
   --tempLocation=gs://${BUCKET}/temp \
   --project=${PROJECT} \
   --runner=DataflowRunner \
   --jobName=polygon-pubsub-to-bigquery-`date +"%Y%m%d-%H%M%S"` \
   --workerMachineType=n1-standard-1 \
   --maxNumWorkers=1 \
   --diskSizeGb=30 \
   --region=us-central1 \
   --zone=us-central1-a \
   "
   ```

### Creating a Cloud Source Repository for Configuration Files

Below are the commands for creating a Cloud Source Repository to hold chainConfig.json:

```bash
REPO_NAME=${PROJECT}-dataflow-config-${ENVIRONMENT_INDEX} && echo "Repo name ${REPO_NAME}"
gcloud source repos create ${REPO_NAME}
gcloud source repos clone ${REPO_NAME} && cd ${REPO_NAME}

# Put chainConfig.json to the root of the repo

git add chainConfig.json && git commit -m "Initial commit"
git push
```

Check a [separate file](ops.md) for operations.
