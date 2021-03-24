package io.blockchainetl.matic.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.matic.domain.Token;

public class ConvertTokensToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertTokensToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertTokensToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        Token token = JsonUtils.parseJson(element, Token.class);

        row.set("address", token.getAddress());
        row.set("symbol", token.getSymbol());
        row.set("name", token.getName());
        row.set("decimals", token.getDecimals());
        row.set("total_supply", token.getTotalSupply());
        row.set("block_number", token.getBlockNumber());
        row.set("block_hash", token.getBlockHash());
    }
}
