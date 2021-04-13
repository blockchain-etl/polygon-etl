package io.blockchainetl;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.PubSubToBigQueryPipeline;
import io.blockchainetl.common.TableRowsToStringsFn;
import io.blockchainetl.common.TestUtils;
import io.blockchainetl.polygon.fns.ConvertBlocksToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertContractsToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertLogsToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTokenTransfersToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTokensToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTracesToTableRowsFn;
import io.blockchainetl.polygon.fns.ConvertTransactionsToTableRowsFn;
import org.apache.beam.sdk.testing.PAssert;
import org.apache.beam.sdk.testing.TestPipeline;
import org.apache.beam.sdk.testing.ValidatesRunner;
import org.apache.beam.sdk.transforms.Create;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.junit.Rule;
import org.junit.Test;
import org.junit.experimental.categories.Category;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import java.io.IOException;
import java.util.List;


@RunWith(JUnit4.class)
public class polygonPubSubToBigQueryPipelineTest {

    @Rule
    public TestPipeline p = TestPipeline.create();
    
    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonBlocks() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000Expected.json",
            new ConvertBlocksToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonTransactions() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000Transactions.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000TransactionsExpected.json",
            new ConvertTransactionsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonLogs() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000Logs.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1000000LogsExpected.json",
            new ConvertLogsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonTokenTransfers() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1755634TokenTransfers.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock1755634TokenTransfersExpected.json",
            new ConvertTokenTransfersToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonTraces() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234Traces.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234TracesExpected.json",
            new ConvertTracesToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonContracts() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234Contracts.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234ContractsExpected.json",
            new ConvertContractsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testpolygonTokens() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234Tokens.json",
            "testdata/PubSubToBigQueryPipelineTest/polygon/polygonBlock2112234TokensExpected.json",
            new ConvertTokensToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }
    
    private void testTemplate(String inputFile, String outputFile, DoFn<String, TableRow> convertFn) throws IOException {
        List<String> blockchainData = TestUtils.readLines(inputFile);
        PCollection<String> collection = p.apply("Input", Create.of(blockchainData));

        PCollection<TableRow> tableRows = PubSubToBigQueryPipeline.buildPipeline(
            "polygonEntities",
            collection,
            convertFn
        );

        TestUtils.logPCollection(tableRows);

        PAssert.that(tableRows.apply("TableRowsToStringsFn", ParDo.of(new TableRowsToStringsFn())))
            .containsInAnyOrder(TestUtils.readLines(outputFile));

        p.run().waitUntilFinish();  
    }
}
