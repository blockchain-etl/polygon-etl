package io.blockchainetl.matic.domain;

import com.google.common.base.Objects;
import org.apache.avro.reflect.Nullable;
import org.apache.beam.sdk.coders.AvroCoder;
import org.apache.beam.sdk.coders.DefaultCoder;
import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

import java.util.List;

@DefaultCoder(AvroCoder.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Contract {

    @Nullable
    private String type;

    @Nullable
    private String address;

    @Nullable
    private String bytecode;

    @Nullable
    @JsonProperty("function_sighashes")
    private List<String> functionSighashes;

    @Nullable
    @JsonProperty("is_erc20")
    private Boolean isErc20;

    @Nullable
    @JsonProperty("is_erc721")
    private Boolean isErc721;
    
    @Nullable
    @JsonProperty("block_timestamp")
    private Long blockTimestamp;

    @Nullable
    @JsonProperty("block_number")
    private Long blockNumber;

    @Nullable
    @JsonProperty("block_hash")
    private String blockHash;
    
    public Contract() {}

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

    public String getBytecode() {
        return bytecode;
    }

    public void setBytecode(String bytecode) {
        this.bytecode = bytecode;
    }

    public List<String> getFunctionSighashes() {
        return functionSighashes;
    }

    public void setFunctionSighashes(List<String> functionSighashes) {
        this.functionSighashes = functionSighashes;
    }

    public Boolean getErc20() {
        return isErc20;
    }

    public void setErc20(Boolean erc20) {
        isErc20 = erc20;
    }

    public Boolean getErc721() {
        return isErc721;
    }

    public void setErc721(Boolean erc721) {
        isErc721 = erc721;
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
        Contract contract = (Contract) o;
        return Objects.equal(type, contract.type) &&
            Objects.equal(address, contract.address) &&
            Objects.equal(bytecode, contract.bytecode) &&
            Objects.equal(functionSighashes, contract.functionSighashes) &&
            Objects.equal(isErc20, contract.isErc20) &&
            Objects.equal(isErc721, contract.isErc721) &&
            Objects.equal(blockTimestamp, contract.blockTimestamp) &&
            Objects.equal(blockNumber, contract.blockNumber) &&
            Objects.equal(blockHash, contract.blockHash);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(type, address, bytecode, functionSighashes, isErc20, isErc721, blockTimestamp,
            blockNumber,
            blockHash);
    }

    @Override
    public String toString() {
        return Objects.toStringHelper(this)
            .add("type", type)
            .add("address", address)
            .add("bytecode", bytecode)
            .add("functionSighashes", functionSighashes)
            .add("isErc20", isErc20)
            .add("isErc721", isErc721)
            .add("blockTimestamp", blockTimestamp)
            .add("blockNumber", blockNumber)
            .add("blockHash", blockHash)
            .toString();
    }
}
