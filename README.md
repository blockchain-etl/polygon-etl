# Polygon-etl

## Overview

Polygon ETL allows you to setup an ETL pipeline in Google Cloud Platform for ingesting Polygon blockchain data
into BigQuery and Pub/Sub. It comes with [CLI tools](/cli) for exporting Polygon data into convenient formats like CSVs and relational databases.


## Status Update (2024-08-29)

### This repo
- Nansen has decided to step back from its role as major contributor to this repo.
- Nansen would like to thank all contributors to this repo, with best wishes for the future.

### Raw data
- Polygon continues to batch load daily to BigQuery dataset `public-data-finance.crypto_polygon`.
- However, streaming to this dataset is currently disabled in Polygon's GCP infra.
- Nansen will no longer be maintaining this dataset; it's up to Polygon what happens next.

### Parsed data
- This repo's [table_definitions folder](./airflow/dags/resources/stages/parse/table_definitions) is now archived. Please do not add table definitions there!
- Nansen continues to batch load daily to BigQuery datasets `blockchain-etl.polygon_*`.
- Nansen will be maintaining this dataset for the foreseeable future.
- If you wish to contribute table definitions, please raise PRs in [nansen-ai/evm-table-definitions](https://github.com/nansen-ai/evm-table-definitions).


## Architecture

![polygon_etl_architecture.svg](polygon_etl_architecture.svg)

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

2. Follow the instructions in [Polygon ETL Streaming](/streaming) to deploy the Streamer component. For the value in
   `last_synced_block.txt` specify the last block number of the previous day. You can query it in BigQuery:
   `SELECT number FROM crypto_polygon.blocks ORDER BY number DESC LIMIT 1`.

3. Follow the instructions in [Polygon ETL Dataflow](/dataflow) to deploy the Dataflow component. Monitor
   "verify_streaming" DAG in Airflow console, once the Dataflow job catches up the latest block, the DAG will succeed.

## Code quality

Over time, we intend to format python files in this repo using isort and black.
At the moment, we are *only formatting any changed or added files*

We have not implemented any sort of automation (e.g. pre-commit), but a requirements_dev.txt is provided for contributors to use.

## Testing

Various tests are implemented (`airflow/tests`, `cli/tests` and `./tests`).
As part of an effort towards consistency, they all source the same requirements_test.txt.
