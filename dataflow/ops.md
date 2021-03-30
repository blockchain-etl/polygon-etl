## Operations

In some case, e.g. when BigQuery tables are recreated, the subscriptions need to be cleared.   

This can be done by rewinding subscriptions to a future date (make sure to change 2020-08-21 to some 
future date):

```bash   
PROJECT=<your_project>
for entity in blocks actions logs transaction_logs
do
    gcloud alpha pubsub subscriptions seek \
    projects/$PROJECT/subscriptions/mainnet.dataflow.bigquery.${entity} --time=2020-08-21T23:00:00.000Z
done
```