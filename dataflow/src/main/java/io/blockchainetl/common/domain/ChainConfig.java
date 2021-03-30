package io.blockchainetl.common.domain;

public class ChainConfig {
    
    private String transformNamePrefix;
    private String pubSubSubscriptionPrefix;
    private String bigQueryDataset;
    private String startTimestamp;

    public String getTransformNamePrefix() {
        return transformNamePrefix;
    }

    public void setTransformNamePrefix(String transformNamePrefix) {
        this.transformNamePrefix = transformNamePrefix;
    }

    public String getPubSubSubscriptionPrefix() {
        return pubSubSubscriptionPrefix;
    }

    public void setPubSubSubscriptionPrefix(String pubSubSubscriptionPrefix) {
        this.pubSubSubscriptionPrefix = pubSubSubscriptionPrefix;
    }

    public String getBigQueryDataset() {
        return bigQueryDataset;
    }

    public void setBigQueryDataset(String bigQueryDataset) {
        this.bigQueryDataset = bigQueryDataset;
    }

    public String getStartTimestamp() {
        return startTimestamp;
    }

    public void setStartTimestamp(String startTimestamp) {
        this.startTimestamp = startTimestamp;
    }
}
