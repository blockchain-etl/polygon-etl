package io.blockchainetl.ethereum.domain;

import com.google.common.base.Objects;
import org.apache.avro.reflect.Nullable;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.coders.DefaultCoder;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

import java.util.List;

@DefaultCoder(AvroCoder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Log {

    @Nullable
    private String type;

    @Nullable
    @JsonProperty("log_index")
    private Long logIndex;
    
    @Nullable
    @JsonProperty("transaction_hash")
    private String transactionHash;

    @Nullable
    @JsonProperty("transaction_index")
    private Long transactionIndex;

    @Nullable
    private String address;

    @Nullable
    private String data;

    @Nullable
    private List<String> topics;

    @Nullable
    @JsonProperty("block_timestamp")
    private Long blockTimestamp;

    @Nullable
    @JsonProperty("block_number")
    private Long blockNumber;

    @Nullable
    @JsonProperty("block_hash")
    private String blockHash;
    
    public Log() {}

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Long getLogIndex() {
        return logIndex;
    }

    public void setLogIndex(Long logIndex) {
        this.logIndex = logIndex;
    }

    public String getTransactionHash() {
        return transactionHash;
    }

    public void setTransactionHash(String transactionHash) {
        this.transactionHash = transactionHash;
    }

    public Long getTransactionIndex() {
        return transactionIndex;
    }

    public void setTransactionIndex(Long transactionIndex) {
        this.transactionIndex = transactionIndex;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public List<String> getTopics() {
        return topics;
    }

    public void setTopics(List<String> topics) {
        this.topics = topics;
    }

    public Long getBlockTimestamp() {
        return blockTimestamp;
    }

    public void setBlockTimestamp(Long blockTimestamp) {
        this.blockTimestamp = blockTimestamp;
    }

    public Long getBlockNumber() {
        return blockNumber;
    }

    public void setBlockNumber(Long blockNumber) {
        this.blockNumber = blockNumber;
    }

    public String getBlockHash() {
        return blockHash;
    }

    public void setBlockHash(String blockHash) {
        this.blockHash = blockHash;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Log log = (Log) o;
        return Objects.equal(type, log.type) &&
            Objects.equal(logIndex, log.logIndex) &&
            Objects.equal(transactionHash, log.transactionHash) &&
            Objects.equal(transactionIndex, log.transactionIndex) &&
            Objects.equal(address, log.address) &&
            Objects.equal(data, log.data) &&
            Objects.equal(topics, log.topics) &&
            Objects.equal(blockTimestamp, log.blockTimestamp) &&
            Objects.equal(blockNumber, log.blockNumber) &&
            Objects.equal(blockHash, log.blockHash);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(type, logIndex, transactionHash, transactionIndex, address, data, topics,
            blockTimestamp,
            blockNumber, blockHash);
    }

    @Override
    public String toString() {
        return Objects.toStringHelper(this)
            .add("type", type)
            .add("logIndex", logIndex)
            .add("transactionHash", transactionHash)
            .add("transactionIndex", transactionIndex)
            .add("address", address)
            .add("data", data)
            .add("topics", topics)
            .add("blockTimestamp", blockTimestamp)
            .add("blockNumber", blockNumber)
            .add("blockHash", blockHash)
            .toString();
    }

}
