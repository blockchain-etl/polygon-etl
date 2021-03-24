package io.blockchainetl.ethereum.domain;

import com.google.common.base.Objects;
import org.apache.avro.reflect.Nullable;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.coders.DefaultCoder;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

@DefaultCoder(AvroCoder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Token {

    @Nullable
    private String type;

    @Nullable
    private String address;

    @Nullable
    private String symbol;

    @Nullable
    private String name;

    @Nullable
    private String decimals;


    @Nullable
    @JsonProperty("total_supply")
    private String totalSupply;
    
    @Nullable
    @JsonProperty("block_timestamp")
    private Long blockTimestamp;

    @Nullable
    @JsonProperty("block_number")
    private Long blockNumber;

    @Nullable
    @JsonProperty("block_hash")
    private String blockHash;
    
    public Token() {}

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDecimals() {
        return decimals;
    }

    public void setDecimals(String decimals) {
        this.decimals = decimals;
    }

    public String getTotalSupply() {
        return totalSupply;
    }

    public void setTotalSupply(String totalSupply) {
        this.totalSupply = totalSupply;
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
        Token token = (Token) o;
        return Objects.equal(type, token.type) &&
            Objects.equal(address, token.address) &&
            Objects.equal(symbol, token.symbol) &&
            Objects.equal(name, token.name) &&
            Objects.equal(decimals, token.decimals) &&
            Objects.equal(totalSupply, token.totalSupply) &&
            Objects.equal(blockTimestamp, token.blockTimestamp) &&
            Objects.equal(blockNumber, token.blockNumber) &&
            Objects.equal(blockHash, token.blockHash);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(type, address, symbol, name, decimals, totalSupply, blockTimestamp, blockNumber,
            blockHash);
    }

    @Override
    public String toString() {
        return Objects.toStringHelper(this)
            .add("type", type)
            .add("address", address)
            .add("symbol", symbol)
            .add("name", name)
            .add("decimals", decimals)
            .add("totalSupply", totalSupply)
            .add("blockTimestamp", blockTimestamp)
            .add("blockNumber", blockNumber)
            .add("blockHash", blockHash)
            .toString();
    }
}
