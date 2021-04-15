package io.blockchainetl.polygon;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.PubSubToBigQueryPipelineOptions;
import io.blockchainetl.common.domain.ChainConfig;
import io.blockchainetl.polygon.fns.ConvertBlocksToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertContractsToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertLogsToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTokenTransfersToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTokensToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTracesToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTransactionsToTableRowsFn;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.DoFn;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static io.blockchainetl.common.PubSubToBigQueryPipeline.readChainConfigs;
import static io.blockchainetl.common.PubSubToBigQueryPipeline.runPipeline;


public class PolygonPubSubToBigQueryPipeline {

    public static void main(String[] args) throws IOException, InterruptedException {
        PubSubToBigQueryPipelineOptions options =
            PipelineOptionsFactory.fromArgs(args).withValidation().as(PubSubToBigQueryPipelineOptions.class);

        runpolygonPipeline(options);
    }

    static void runpolygonPipeline(PubSubToBigQueryPipelineOptions options) {
        List<ChainConfig> chainConfigs = readChainConfigs(options.getChainConfigFile());

        Map<String, Class<? extends DoFn<String, TableRow>>> entityConfigs = new HashMap<>();
        entityConfigs.put("blocks", ConvertBlocksToTableRowsFn.class);
        entityConfigs.put("transactions", ConvertTransactionsToTableRowsFn.class);
        entityConfigs.put("logs", ConvertLogsToTableRowsFn.class);
        entityConfigs.put("token_transfers", ConvertTokenTransfersToTableRowsFn.class);
        entityConfigs.put("traces", ConvertTracesToTableRowsFn.class);
        entityConfigs.put("contracts", ConvertContractsToTableRowsFn.class);
        entityConfigs.put("tokens", ConvertTokensToTableRowsFn.class);
        runPipeline(options,chainConfigs, entityConfigs);
    }
}
