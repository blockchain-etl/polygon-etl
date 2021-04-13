package io.blockchainetl.polygon.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.polygon.domain.Log;

public class ConvertLogsToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertLogsToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertLogsToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        Log log = JsonUtils.parseJson(element, Log.class);

        row.set("log_index", log.getLogIndex());
        row.set("transaction_hash", log.getTransactionHash());
        row.set("transaction_index", log.getTransactionIndex());
        row.set("address", log.getAddress());
        row.set("data", log.getData());
        row.set("topics", log.getTopics());
        row.set("block_number", log.getBlockNumber());
        row.set("block_hash", log.getBlockHash());
    }
}
