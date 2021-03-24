package io.blockchainetl.ethereum_partitioned;

import com.google.api.services.bigquery.model.TableRow;
import com.google.api.services.bigquery.model.TableSchema;
import io.blockchainetl.common.PubSubToBigQueryPipelineOptions;
import io.blockchainetl.common.domain.ChainConfig;
import io.blockchainetl.common.utils.FileUtils;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.common.utils.StringUtils;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.PipelineResult;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.io.gcp.bigquery.DynamicDestinations;
import org.apache.beam.sdk.io.gcp.bigquery.InsertRetryPolicy;
import org.apache.beam.sdk.io.gcp.bigquery.TableDestination;
import org.apache.beam.sdk.io.gcp.bigquery.WriteResult;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.ValueInSingleWindow;
import org.codehaus.jackson.type.TypeReference;
import org.joda.time.Duration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Constructor;
import java.nio.charset.Charset;
import java.util.List;
import java.util.Map;

public class PubSubToBigQueryPartitionedPipeline {

    private static final Logger LOG = LoggerFactory.getLogger(PubSubToBigQueryPartitionedPipeline.class);
    
    private static final String PUBSUB_ID_ATTRIBUTE = "item_id";
    
    public static final String ENTITY_LOGS = "logs";
    public static final String ENTITY_TRACES = "traces";

    public static void runPipeline(
        PubSubToBigQueryPipelineOptions options, 
        List<ChainConfig> chainConfigs,
        Map<String, Class<? extends DoFn<String, TableRow>>> entityConfigs
    ) {
        Pipeline p = Pipeline.create(options);

        if (chainConfigs.isEmpty()) {
            throw new RuntimeException("Chain configs can't be empty");
        }

        for (ChainConfig chainConfig : chainConfigs) {
            for (Map.Entry<String, Class<? extends DoFn<String, TableRow>>> entityConfig : entityConfigs.entrySet()) {
                buildPipeline(p, options, chainConfig, entityConfig);
            }
        }

        // Run pipeline

        PipelineResult pipelineResult = p.run();
        LOG.info(pipelineResult.toString());
    }

    public static void buildPipeline(Pipeline p, PubSubToBigQueryPipelineOptions options, ChainConfig chainConfig,
        Map.Entry<String, Class<? extends DoFn<String, TableRow>>> entityConfig) {
        String entityType = entityConfig.getKey();
        String transformNameSuffix = StringUtils.capitalizeFirstLetter(entityType);

        DoFn<String, TableRow> convertFn = createConvertFn(
            entityConfig.getValue(),
            chainConfig.getStartTimestamp(),
            options.getAllowedTimestampSkewSeconds(),
            chainConfig.getTransformNamePrefix() + ": ");

        buildPipeline(
            p,
            entityConfig.getKey(),
            chainConfig.getTransformNamePrefix() + transformNameSuffix,
            chainConfig.getPubSubSubscriptionPrefix() + "." + entityType,
            convertFn,
            chainConfig.getBigQueryDataset()
        );
    }

    public static PCollection<TableRow> buildPipeline(
        Pipeline p,
        String entityType,
        String namePrefix,
        String pubSubSubscription,
        DoFn<String, TableRow> convertFn,
        String bigQueryDataset
    ) {
        PCollection<String> inputFromPubSub = p.apply(namePrefix + "ReadFromPubSub",
            PubsubIO.readStrings().fromSubscription(pubSubSubscription).withIdAttribute(PUBSUB_ID_ATTRIBUTE));

        PCollection<TableRow> tableRows = buildPipeline(
            namePrefix,
            inputFromPubSub,
            convertFn
        );

        DynamicDestinations<TableRow, String> dynamicDestinations = new DynamicDestinations<TableRow, String>() {
            public String getDestination(ValueInSingleWindow<TableRow> tableRow) {
                String tableName = null;
                if (ENTITY_LOGS.equals(entityType)) {
                    tableName = buildTableNameFromLog(tableRow.getValue());
                } else {
                    tableName = buildTableNameFromTrace(tableRow.getValue());
                }
                return tableName;
            }

            public TableDestination getTable(String tableName) {
                return new TableDestination(bigQueryDataset + "." + tableName, "");
            }

            public TableSchema getSchema(String tableName) {
                return null;
            }
        };
        WriteResult writeResult = tableRows.apply(
            namePrefix + "WriteToBigQuery",
            BigQueryIO.writeTableRows()
                .withoutValidation()
                .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_NEVER)
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                .withFailedInsertRetryPolicy(InsertRetryPolicy.retryTransientErrors())
                .to(dynamicDestinations));

        // There is a limit in BigQuery of 1MB per record for streaming inserts. To handle such cases we use file loads
        // where the limit is 100MB per record.
        writeResult.getFailedInserts().apply(
            namePrefix + "TryWriteFailedRecordsToBigQuery",
            BigQueryIO.writeTableRows()
                .withoutValidation()
                .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_NEVER)
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                .withMethod(BigQueryIO.Write.Method.FILE_LOADS)
                .withNumFileShards(1)
                .withTriggeringFrequency(Duration.standardMinutes(10))
                .to(dynamicDestinations));

        return tableRows;
    }

    private static String buildTableNameFromLog(TableRow tableRow) {
        String tablePrefix = "logs_by_topic_";
        String tableSuffix = "empty";
        
        if (tableRow != null) {
            Object topics = tableRow.get("topics");
            if (topics instanceof List) {
                List<String> topicsAsStrings = (List<String>) topics;
                if (!topicsAsStrings.isEmpty()) {
                    String firstTopic = topicsAsStrings.get(0);
                    if (firstTopic != null && firstTopic.length() >= 5) {
                        String topicPrefix = firstTopic.substring(0, 5);
                        tableSuffix = topicPrefix;
                    }
                }
            }
        }
        return tablePrefix + tableSuffix;
    }

    private static String buildTableNameFromTrace(TableRow tableRow) {
        String tablePrefix = "traces_by_input_";
        String tableSuffix = "empty";
        // for logs
        if (tableRow != null) {
            Object input = tableRow.get("input");
            if (input instanceof String) {
                String inputAsString = (String) input;
                if (inputAsString.length() >= 5) {
                    String inputPrefix = inputAsString.substring(0, 5);
                    tableSuffix = inputPrefix;
                }
            }
        }
        return tablePrefix + tableSuffix;
    }

    public static PCollection<TableRow> buildPipeline(
        String namePrefix,
        PCollection<String> input,
        DoFn<String, TableRow> convertFn
    ) {
        return input.apply(namePrefix + "ConvertToTableRows", ParDo.of(convertFn));
    }

    private static DoFn<String, TableRow> createConvertFn(
        Class<? extends DoFn<String, TableRow>> clazz, String startTimestamp, Long allowedTimestampSkewSeconds,
        String logPrefix) {
        try {
            Constructor<? extends DoFn<String, TableRow>> convertFnConstructor = clazz.getConstructor(
                String.class, Long.class, String.class);

            return convertFnConstructor.newInstance(startTimestamp, allowedTimestampSkewSeconds, logPrefix);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static List<ChainConfig> readChainConfigs(String file) {
        String fileContents = FileUtils.readFile(file, Charset.forName("UTF-8"));
        List<ChainConfig> result = JsonUtils.parseJson(fileContents, new TypeReference<List<ChainConfig>>() {
        });
        return result;
    }
}
