# Polygon-etl

## Overview

Polygon ETL allows you to setup an ETL pipeline in Google Cloud Platform for ingesting Polygon blockchain data 
into BigQuery and Pub/Sub. It comes with [CLI tools](/cli) for exporting Polygon data into convenient formats like CSVs and relational databases.

## Architecture


1. The nodes are run in a Kubernetes cluster. 

2. [Airflow DAGs](https://airflow.apache.org/) export and load Polygon data to BigQuery daily. 
    Refer to [Polygon ETL Airflow](/airflow) for deployment instructions.
  
3. Polygon data is polled periodically from the nodes and pushed to Google Pub/Sub. 
    Refer to [Polygon ETL Streaming](/streaming) for deployment instructions.  
  
4. Polygon data is pulled from Pub/Sub, transformed and streamed to BigQuery. 
    Refer to [Polygon ETL Dataflow](/dataflow) for deployment instructions.  
 
## Setting Up

1. Follow the instructions in [Polygon ETL Airflow](/airflow) to deploy a Cloud Composer cluster for 
    exporting and loading historical Polygon data. It may take several days for the export DAG to catch up. During this
    time "load" and "verify_streaming" DAGs will fail. 

3. Follow the instructions in [Polygon ETL Streaming](/streaming) to deploy the Streamer component. For the value in 
    `last_synced_block.txt` specify the last block number of the previous day. You can query it in BigQuery:
    `SELECT block FROM crypto_polygon.blocks ORDER BY blocks DESC LIMIT 1`.

4. Follow the instructions in [Polygon ETL Dataflow](/dataflow) to deploy the Dataflow component. Monitor 
    "verify_streaming" DAG in Airflow console, once the Dataflow job catches up the latest block, the DAG will succeed.

