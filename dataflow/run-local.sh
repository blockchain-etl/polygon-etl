#!/usr/bin/env bash


mvn -Pdirect-runner compile exec:java \
-Dexec.mainClass=io.blockchainetl.polygon.PolygonPubSubToBigQueryPipeline \
-Dexec.args="--chainConfigFile=chainConfig.json --allowedTimestampSkewSeconds=36000 --defaultSdkHarnessLogLevel=DEBUG \
--tempLocation=gs://nansen-dev/dataflow"
