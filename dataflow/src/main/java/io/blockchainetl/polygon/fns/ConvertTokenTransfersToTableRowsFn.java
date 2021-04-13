package io.blockchainetl.polygon.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.polygon.domain.TokenTransfer;

public class ConvertTokenTransfersToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertTokenTransfersToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertTokenTransfersToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        TokenTransfer tokenTransfer = JsonUtils.parseJson(element, TokenTransfer.class);

        row.set("token_address", tokenTransfer.getTokenAddress());
        row.set("from_address", tokenTransfer.getFromAddress());
        row.set("to_address", tokenTransfer.getToAddress());
        row.set("value", tokenTransfer.getValue() != null ? tokenTransfer.getValue().toString() : null);
        row.set("transaction_hash", tokenTransfer.getTransactionHash());
        row.set("log_index", tokenTransfer.getLogIndex());
        row.set("block_number", tokenTransfer.getBlockNumber());
        row.set("block_hash", tokenTransfer.getBlockHash());
    }
}
