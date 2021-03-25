#!/usr/bin/env bash

mvn -Pdirect-runner compile exec:java \
-Dexec.mainClass=io.blockchainetl.matic.maticPubSubToBigQueryPipeline \
-Dexec.args="--chainConfigFile=chainConfigMaticDev.json \
--tempLocation=gs://matic-etl-dev-dataflow-0/ \
--outputErrorsTable=mainnet.errors"

