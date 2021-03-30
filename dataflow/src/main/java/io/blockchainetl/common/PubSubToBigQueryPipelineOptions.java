package io.blockchainetl.common;

import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.SdkHarnessOptions;
import org.apache.beam.sdk.options.StreamingOptions;
import org.apache.beam.sdk.options.Validation;

public interface PubSubToBigQueryPipelineOptions extends PipelineOptions, StreamingOptions, SdkHarnessOptions {
    
    @Description("JSON file containing chain configuration")
    @Validation.Required
    String getChainConfigFile();

    void setChainConfigFile(String value);

    @Description("Timestamp skew for blocks and transactions, messages older than this will be rejected")
    Long getAllowedTimestampSkewSeconds();

    void setAllowedTimestampSkewSeconds(Long allowedTimestampSkewSeconds);
}
