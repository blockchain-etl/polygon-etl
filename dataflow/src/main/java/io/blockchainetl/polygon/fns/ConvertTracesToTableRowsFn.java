package io.blockchainetl.polygon.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.polygon.domain.Trace;

import java.util.List;
import java.util.stream.Collectors;

public class ConvertTracesToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertTracesToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertTracesToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        Trace trace = JsonUtils.parseJson(element, Trace.class);

        row.set("transaction_hash", trace.getTransactionHash());
        row.set("transaction_index", trace.getTransactionIndex());
        row.set("from_address", trace.getFromAddress());
        row.set("to_address", trace.getToAddress());
        row.set("value", trace.getValue() != null ? trace.getValue().toString() : null);
        row.set("input", trace.getInput());
        row.set("output", trace.getOutput());
        row.set("trace_type", trace.getTraceType());
        row.set("call_type", trace.getCallType());
        row.set("reward_type", trace.getRewardType());
        row.set("gas", trace.getGas());
        row.set("gas_used", trace.getGasUsed());
        row.set("subtraces", trace.getSubtraces());
        row.set("trace_address", convertTraceAddressToString(trace.getTraceAddress()));
        row.set("error", trace.getError());
        row.set("status", trace.getStatus());
        row.set("trace_id", trace.getTraceId());
        row.set("block_number", trace.getBlockNumber());
        row.set("block_hash", trace.getBlockHash());
    }
    
    private String convertTraceAddressToString(List<Long> traceAddress) {
        List<String> strings = traceAddress.stream().map(String::valueOf).collect(Collectors.toList());
        return String.join(",", strings);
    }
}
