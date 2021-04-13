package io.blockchainetl.polygon.domain;

import com.google.common.base.MoreObjects;
import com.google.common.base.Objects;
import org.apache.avro.reflect.Nullable;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.coders.DefaultCoder;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

import java.math.BigInteger;

@DefaultCoder(AvroCoder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Block {

    @Nullable
    private String type;

    @Nullable
    private Long number;
    
    @Nullable
    private String hash;

    @Nullable
    @JsonProperty("parent_hash")
    private String parentHash;

    @Nullable
    private String nonce;

    @Nullable
    @JsonProperty("sha3_uncles")
    private String sha3Uncles;

    @Nullable
    @JsonProperty("logs_bloom")
    private String logsBloom;

    @Nullable
    @JsonProperty("transactions_root")
    private String transactionsRoot;

    @Nullable
    @JsonProperty("state_root")
    private String stateRoot;

    @Nullable
    @JsonProperty("receipts_root")
    private String receiptsRoot;

    @Nullable
    private String miner;

    @Nullable
    private BigInteger difficulty;

    @Nullable
    @JsonProperty("total_difficulty")
    private BigInteger totalDifficulty;

    @Nullable
    private Long size;

    @Nullable
    @JsonProperty("extra_data")
    private String extraData;

    @Nullable
    @JsonProperty("gas_limit")
    private Long gasLimit;

    @Nullable
    @JsonProperty("gas_used")
    private Long gasUsed;

    @Nullable
    @JsonProperty("timestamp")
    private Long timestamp;

    @Nullable
    @JsonProperty("transaction_count")
    private Long transactionCount;

    public Block() {}

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Long getNumber() {
        return number;
    }

    public void setNumber(Long number) {
        this.number = number;
    }

    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public String getParentHash() {
        return parentHash;
    }

    public void setParentHash(String parentHash) {
        this.parentHash = parentHash;
    }

    public String getNonce() {
        return nonce;
    }

    public void setNonce(String nonce) {
        this.nonce = nonce;
    }

    public String getSha3Uncles() {
        return sha3Uncles;
    }

    public void setSha3Uncles(String sha3Uncles) {
        this.sha3Uncles = sha3Uncles;
    }

    public String getLogsBloom() {
        return logsBloom;
    }

    public void setLogsBloom(String logsBloom) {
        this.logsBloom = logsBloom;
    }

    public String getTransactionsRoot() {
        return transactionsRoot;
    }

    public void setTransactionsRoot(String transactionsRoot) {
        this.transactionsRoot = transactionsRoot;
    }

    public String getStateRoot() {
        return stateRoot;
    }

    public void setStateRoot(String stateRoot) {
        this.stateRoot = stateRoot;
    }

    public String getReceiptsRoot() {
        return receiptsRoot;
    }

    public void setReceiptsRoot(String receiptsRoot) {
        this.receiptsRoot = receiptsRoot;
    }

    public String getMiner() {
        return miner;
    }

    public void setMiner(String miner) {
        this.miner = miner;
    }

    public BigInteger getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(BigInteger difficulty) {
        this.difficulty = difficulty;
    }

    public BigInteger getTotalDifficulty() {
        return totalDifficulty;
    }

    public void setTotalDifficulty(BigInteger totalDifficulty) {
        this.totalDifficulty = totalDifficulty;
    }

    public Long getSize() {
        return size;
    }

    public void setSize(Long size) {
        this.size = size;
    }

    public String getExtraData() {
        return extraData;
    }

    public void setExtraData(String extraData) {
        this.extraData = extraData;
    }

    public Long getGasLimit() {
        return gasLimit;
    }

    public void setGasLimit(Long gasLimit) {
        this.gasLimit = gasLimit;
    }

    public Long getGasUsed() {
        return gasUsed;
    }

    public void setGasUsed(Long gasUsed) {
        this.gasUsed = gasUsed;
    }

    public Long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Long timestamp) {
        this.timestamp = timestamp;
    }

    public Long getTransactionCount() {
        return transactionCount;
    }

    public void setTransactionCount(Long transactionCount) {
        this.transactionCount = transactionCount;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Block block = (Block) o;
        return Objects.equal(type, block.type) &&
            Objects.equal(number, block.number) &&
            Objects.equal(hash, block.hash) &&
            Objects.equal(parentHash, block.parentHash) &&
            Objects.equal(nonce, block.nonce) &&
            Objects.equal(sha3Uncles, block.sha3Uncles) &&
            Objects.equal(logsBloom, block.logsBloom) &&
            Objects.equal(transactionsRoot, block.transactionsRoot) &&
            Objects.equal(stateRoot, block.stateRoot) &&
            Objects.equal(receiptsRoot, block.receiptsRoot) &&
            Objects.equal(miner, block.miner) &&
            Objects.equal(difficulty, block.difficulty) &&
            Objects.equal(totalDifficulty, block.totalDifficulty) &&
            Objects.equal(size, block.size) &&
            Objects.equal(extraData, block.extraData) &&
            Objects.equal(gasLimit, block.gasLimit) &&
            Objects.equal(gasUsed, block.gasUsed) &&
            Objects.equal(timestamp, block.timestamp) &&
            Objects.equal(transactionCount, block.transactionCount);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(type, number, hash, parentHash, nonce, sha3Uncles, logsBloom, transactionsRoot,
            stateRoot,
            receiptsRoot, miner, difficulty, totalDifficulty, size, extraData, gasLimit, gasUsed, timestamp,
            transactionCount);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
            .add("type", type)
            .add("number", number)
            .add("hash", hash)
            .add("parentHash", parentHash)
            .add("nonce", nonce)
            .add("sha3Uncles", sha3Uncles)
            .add("logsBloom", logsBloom)
            .add("transactionsRoot", transactionsRoot)
            .add("stateRoot", stateRoot)
            .add("receiptsRoot", receiptsRoot)
            .add("miner", miner)
            .add("difficulty", difficulty)
            .add("totalDifficulty", totalDifficulty)
            .add("size", size)
            .add("extraData", extraData)
            .add("gasLimit", gasLimit)
            .add("gasUsed", gasUsed)
            .add("timestamp", timestamp)
            .add("transactionCount", transactionCount)
            .toString();
    }
}
