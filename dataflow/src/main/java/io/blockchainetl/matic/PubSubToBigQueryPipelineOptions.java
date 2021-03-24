package io.blockchainetl.matic;

import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.StreamingOptions;
import org.apache.beam.sdk.options.Validation;
import org.apache.beam.sdk.options.ValueProvider;

public interface PubSubToBigQueryPipelineOptions extends PipelineOptions, StreamingOptions {
    
    @Description("JSON file containing chain configuration")
    @Validation.Required
    String getChainConfigFile();

    void setChainConfigFile(String value);

    @Description("BigQuery table to output errors to. The name should be in the format of " +
        "<project-id>:<dataset-id>.<table-name>.")
    ValueProvider<String> getOutputErrorsTable();
    void setOutputErrorsTable(ValueProvider<String> value);
}
