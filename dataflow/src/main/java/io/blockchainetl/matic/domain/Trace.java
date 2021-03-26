package io.blockchainetl.matic.domain;

import com.google.common.base.MoreObjects;
import com.google.common.base.Objects;
import org.apache.avro.reflect.Nullable;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.coders.DefaultCoder;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

import java.math.BigInteger;
import java.util.List;

@DefaultCoder(AvroCoder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Trace {

    @Nullable
    @JsonProperty("transaction_hash")
    private String transactionHash;

    @Nullable
    @JsonProperty("transaction_index")
    private Long transactionIndex;

    @Nullable
    @JsonProperty("from_address")
    private String fromAddress;

    @Nullable
    @JsonProperty("to_address")
    private String toAddress;

    @Nullable
    private BigInteger value;

    @Nullable
    private String input;

    @Nullable
    private String output;

    @Nullable
    @JsonProperty("trace_type")
    private String traceType;

    @Nullable
    @JsonProperty("call_type")
    private String callType;

    @Nullable
    @JsonProperty("reward_type")
    private String rewardType;

    @Nullable
    private Long gas;

    @Nullable
    @JsonProperty("gas_used")
    private Long gasUsed;

    @Nullable
    private Long subtraces;

    @Nullable
    @JsonProperty("trace_address")
    private List<Long> traceAddress;

    @Nullable
    private String error;

    @Nullable
    private Long status;

    @Nullable
    @JsonProperty("trace_id")
    private String traceId;

    @Nullable
    @JsonProperty("block_timestamp")
    private Long blockTimestamp;

    @Nullable
    @JsonProperty("block_number")
    private Long blockNumber;

    @Nullable
    @JsonProperty("block_hash")
    private String blockHash;
    
    public Trace() {}

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

    public String getFromAddress() {
        return fromAddress;
    }

    public void setFromAddress(String fromAddress) {
        this.fromAddress = fromAddress;
    }

    public String getToAddress() {
        return toAddress;
    }

    public void setToAddress(String toAddress) {
        this.toAddress = toAddress;
    }

    public BigInteger getValue() {
        return value;
    }

    public void setValue(BigInteger value) {
        this.value = value;
    }

    public String getInput() {
        return input;
    }

    public void setInput(String input) {
        this.input = input;
    }

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }

    public String getTraceType() {
        return traceType;
    }

    public void setTraceType(String traceType) {
        this.traceType = traceType;
    }

    public String getCallType() {
        return callType;
    }

    public void setCallType(String callType) {
        this.callType = callType;
    }

    public String getRewardType() {
        return rewardType;
    }

    public void setRewardType(String rewardType) {
        this.rewardType = rewardType;
    }

    public Long getGas() {
        return gas;
    }

    public void setGas(Long gas) {
        this.gas = gas;
    }

    public Long getGasUsed() {
        return gasUsed;
    }

    public void setGasUsed(Long gasUsed) {
        this.gasUsed = gasUsed;
    }

    public Long getSubtraces() {
        return subtraces;
    }

    public void setSubtraces(Long subtraces) {
        this.subtraces = subtraces;
    }

    public List<Long> getTraceAddress() {
        return traceAddress;
    }

    public void setTraceAddress(List<Long> traceAddress) {
        this.traceAddress = traceAddress;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public Long getStatus() {
        return status;
    }

    public void setStatus(Long status) {
        this.status = status;
    }

    public String getTraceId() {
        return traceId;
    }

    public void setTraceId(String traceId) {
        this.traceId = traceId;
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
        Trace trace = (Trace) o;
        return Objects.equal(transactionHash, trace.transactionHash) &&
            Objects.equal(transactionIndex, trace.transactionIndex) &&
            Objects.equal(fromAddress, trace.fromAddress) &&
            Objects.equal(toAddress, trace.toAddress) &&
            Objects.equal(value, trace.value) &&
            Objects.equal(input, trace.input) &&
            Objects.equal(output, trace.output) &&
            Objects.equal(traceType, trace.traceType) &&
            Objects.equal(callType, trace.callType) &&
            Objects.equal(rewardType, trace.rewardType) &&
            Objects.equal(gas, trace.gas) &&
            Objects.equal(gasUsed, trace.gasUsed) &&
            Objects.equal(subtraces, trace.subtraces) &&
            Objects.equal(traceAddress, trace.traceAddress) &&
            Objects.equal(error, trace.error) &&
            Objects.equal(status, trace.status) &&
            Objects.equal(traceId, trace.traceId) &&
            Objects.equal(blockTimestamp, trace.blockTimestamp) &&
            Objects.equal(blockNumber, trace.blockNumber) &&
            Objects.equal(blockHash, trace.blockHash);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(transactionHash, transactionIndex, fromAddress, toAddress, value,
            input, output, traceType, callType, rewardType, gas, gasUsed, subtraces, traceAddress, error, status,
            traceId,
            blockTimestamp, blockNumber, blockHash);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
            .add("transactionHash", transactionHash)
            .add("transactionIndex", transactionIndex)
            .add("fromAddress", fromAddress)
            .add("toAddress", toAddress)
            .add("value", value)
            .add("input", input)
            .add("output", output)
            .add("traceType", traceType)
            .add("callType", callType)
            .add("rewardType", rewardType)
            .add("gas", gas)
            .add("gasUsed", gasUsed)
            .add("subtraces", subtraces)
            .add("traceAddress", traceAddress)
            .add("error", error)
            .add("status", status)
            .add("traceId", traceId)
            .add("blockTimestamp", blockTimestamp)
            .add("blockNumber", blockNumber)
            .add("blockHash", blockHash)
            .toString();
    }
}
