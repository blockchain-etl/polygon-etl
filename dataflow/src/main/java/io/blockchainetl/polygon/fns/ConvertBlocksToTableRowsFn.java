package io.blockchainetl.polygon.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.polygon.domain.Block;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;

public class ConvertBlocksToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertBlocksToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertBlocksToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        Block block = JsonUtils.parseJson(element, Block.class);

        row.set("number", block.getNumber());
        row.set("hash", block.getHash());
        row.set("parent_hash", block.getParentHash());
        row.set("nonce", block.getNonce());
        row.set("sha3_uncles", block.getSha3Uncles());
        row.set("nonce", block.getNonce());
        row.set("sha3_uncles", block.getSha3Uncles());
        row.set("logs_bloom", block.getLogsBloom());
        row.set("transactions_root", block.getTransactionsRoot());
        row.set("state_root", block.getStateRoot());
        row.set("receipts_root", block.getReceiptsRoot());
        row.set("miner", block.getMiner());
        row.set("difficulty", block.getDifficulty());
        row.set("total_difficulty", block.getTotalDifficulty());
        row.set("size", block.getSize());
        row.set("extra_data", block.getExtraData());
        row.set("gas_limit", block.getGasLimit());
        row.set("gas_used", block.getGasUsed());
        row.set("transaction_count", block.getTransactionCount());
    }
}
