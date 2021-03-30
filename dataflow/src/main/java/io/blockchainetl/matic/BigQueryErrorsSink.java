package io.blockchainetl.matic;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.api.services.bigquery.model.TableRow;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryInsertError;
import org.apache.beam.sdk.io.gcp.bigquery.InsertRetryPolicy;
import org.apache.beam.sdk.options.ValueProvider;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.PTransform;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.PDone;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Writes TableRow (serialized to json) and InsertErrors (serialized to json) in BigQueryInsertError to errors
 * table in BigQuery.
 *
 * Failed retry policy is set to always retry since this is last step in failure handling and no failure should be
 * silently ignored.
 * Throwing exception in case of any failure would prompt the runner to retry the whole bundle, and can lead to
 * duplicate inserts. So it is best to let BigQueryIO retry only the failed inserts.
 */
class BigQueryErrorsSink extends PTransform<PCollection<BigQueryInsertError>, PDone> {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    private final ValueProvider<String> errorsTable;
    private final String errorsTableJsonSchema;

    BigQueryErrorsSink(ValueProvider<String> errorsTable, String errorsTableJsonSchema) {
        this.errorsTable = errorsTable;
        this.errorsTableJsonSchema = errorsTableJsonSchema;
    }

    @Override
    public PDone expand(PCollection<BigQueryInsertError> input) {
        input.apply("ConvertErrorToTableRow", ParDo.of(new BigQueryInsertErrorToTableRow()))
            .apply("WriteErrorsToTable", BigQueryIO.writeTableRows()
                .to(errorsTable)
                .withJsonSchema(errorsTableJsonSchema)
                .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_NEVER)
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                .withFailedInsertRetryPolicy(InsertRetryPolicy.alwaysRetry()));
        return PDone.in(input.getPipeline());
    }

    static class BigQueryInsertErrorToTableRow extends DoFn<BigQueryInsertError, TableRow> {

        private static final Logger LOG = LoggerFactory.getLogger(BigQueryErrorsSink.class);

        @ProcessElement
        public void processElement(ProcessContext context) {
            BigQueryInsertError error = context.element();
            try {
                TableRow tableRow = new TableRow()
                    .set("tableRow", MAPPER.writeValueAsString(error.getRow()))
                    .set("errors", MAPPER.writeValueAsString(error.getError()));
                LOG.error(tableRow.toPrettyString());
                context.output(tableRow);
            } catch (Exception e) {
                LOG.error("Error converting BigQueryInsertError to TableRow", e);
                throw new RuntimeException(e);
            }
        }
    }
}
