#!/usr/bin/env bash

# mvn -Pdirect-runner compile exec:java \
# -Dexec.mainClass=io.blockchainetl.matic.MaticPubSubToBigQueryPipeline \
# -Dexec.args="--chainConfigFile=chainConfig.json \
# --tempLocation=gs://matic-etl-dev-dataflow-0/ \
# --outputErrorsTable=mainnet.errors" 
# -X

mvn -Pdirect-runner compile exec:java \
-Dexec.mainClass=io.blockchainetl.matic.MaticPubSubToBigQueryPipeline \
-Dexec.args="--chainConfigFile=chainConfig.json --allowedTimestampSkewSeconds=36000 --defaultSdkHarnessLogLevel=DEBUG \
--tempLocation=gs://nansen-dev/dataflow"
