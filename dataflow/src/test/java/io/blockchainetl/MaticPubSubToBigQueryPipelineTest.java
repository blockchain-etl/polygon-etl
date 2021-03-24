package io.blockchainetl;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.PubSubToBigQueryPipeline;
import io.blockchainetl.common.TableRowsToStringsFn;
import io.blockchainetl.common.TestUtils;
import io.blockchainetl.matic.fns.ConvertBlocksToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertContractsToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertLogsToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertTokenTransfersToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertTokensToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertTracesToTableRowsFn;
import io.blockchainetl.matic.fns.ConvertTransactionsToTableRowsFn;
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
public class maticPubSubToBigQueryPipelineTest {

    @Rule
    public TestPipeline p = TestPipeline.create();
    
    @Test
    @Category(ValidatesRunner.class)
    public void testmaticBlocks() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000Expected.json",
            new ConvertBlocksToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticTransactions() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000Transactions.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000TransactionsExpected.json",
            new ConvertTransactionsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticLogs() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000Logs.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1000000LogsExpected.json",
            new ConvertLogsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticTokenTransfers() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1755634TokenTransfers.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock1755634TokenTransfersExpected.json",
            new ConvertTokenTransfersToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticTraces() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234Traces.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234TracesExpected.json",
            new ConvertTracesToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticContracts() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234Contracts.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234ContractsExpected.json",
            new ConvertContractsToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }

    @Test
    @Category(ValidatesRunner.class)
    public void testmaticTokens() throws Exception {
        testTemplate(
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234Tokens.json",
            "testdata/PubSubToBigQueryPipelineTest/matic/maticBlock2112234TokensExpected.json",
            new ConvertTokensToTableRowsFn("2015-01-01T00:00:00Z", Long.MAX_VALUE)
        );
    }
    
    private void testTemplate(String inputFile, String outputFile, DoFn<String, TableRow> convertFn) throws IOException {
        List<String> blockchainData = TestUtils.readLines(inputFile);
        PCollection<String> collection = p.apply("Input", Create.of(blockchainData));

        PCollection<TableRow> tableRows = PubSubToBigQueryPipeline.buildPipeline(
            "maticEntities",
            collection,
            convertFn
        );

        TestUtils.logPCollection(tableRows);

        PAssert.that(tableRows.apply("TableRowsToStringsFn", ParDo.of(new TableRowsToStringsFn())))
            .containsInAnyOrder(TestUtils.readLines(outputFile));

        p.run().waitUntilFinish();  
    }
}
