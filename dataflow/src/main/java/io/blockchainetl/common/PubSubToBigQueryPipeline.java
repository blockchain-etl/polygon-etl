package io.blockchainetl.common;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.domain.ChainConfig;
import io.blockchainetl.common.utils.FileUtils;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.common.utils.StringUtils;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.PipelineResult;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.io.gcp.bigquery.InsertRetryPolicy;
import org.apache.beam.sdk.io.gcp.bigquery.WriteResult;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.codehaus.jackson.type.TypeReference;
import org.joda.time.Duration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Constructor;
import java.nio.charset.Charset;
import java.util.List;
import java.util.Map;


public class PubSubToBigQueryPipeline {

    private static final Logger LOG = LoggerFactory.getLogger(PubSubToBigQueryPipeline.class);
    
    private static final String PUBSUB_ID_ATTRIBUTE = "item_id";

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
            chainConfig.getTransformNamePrefix() + transformNameSuffix,
            chainConfig.getPubSubSubscriptionPrefix() + "." + entityType,
            convertFn,
            chainConfig.getBigQueryDataset() + "." + entityType
        );
    }

    public static PCollection<TableRow> buildPipeline(
        Pipeline p,
        String namePrefix,
        String pubSubSubscription,
        DoFn<String, TableRow> convertFn,
        String bigQueryTable
    ) {
        PCollection<String> inputFromPubSub = p.apply(namePrefix + "ReadFromPubSub",
            PubsubIO.readStrings().fromSubscription(pubSubSubscription).withIdAttribute(PUBSUB_ID_ATTRIBUTE));

        PCollection<TableRow> tableRows = buildPipeline(
            namePrefix,
            inputFromPubSub,
            convertFn
        );

        WriteResult writeResult = tableRows.apply(
            namePrefix + "WriteToBigQuery",
            BigQueryIO.writeTableRows()
                .withoutValidation()
                .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_NEVER)
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                .withFailedInsertRetryPolicy(InsertRetryPolicy.retryTransientErrors())
                .to(bigQueryTable));

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
                .to(bigQueryTable));

        return tableRows;
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
