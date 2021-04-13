package io.blockchainetl.polygon.fns;

import com.google.api.services.bigquery.model.TableRow;
import io.blockchainetl.common.fns.ConvertEntitiesToTableRowsFn;
import io.blockchainetl.common.utils.JsonUtils;
import io.blockchainetl.polygon.domain.Contract;

public class ConvertContractsToTableRowsFn extends ConvertEntitiesToTableRowsFn {

    public ConvertContractsToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds) {
        super(startTimestamp, allowedTimestampSkewSeconds, "", false);
    }

    public ConvertContractsToTableRowsFn(String startTimestamp, Long allowedTimestampSkewSeconds, String logPrefix) {
        super(startTimestamp, allowedTimestampSkewSeconds, logPrefix, false);
    }

    @Override
    protected void populateTableRowFields(TableRow row, String element) {
        Contract contract = JsonUtils.parseJson(element, Contract.class);

        row.set("address", contract.getAddress());
        row.set("bytecode", contract.getBytecode());
        row.set("function_sighashes", contract.getFunctionSighashes());
        row.set("is_erc20", contract.getErc20());
        row.set("is_erc721", contract.getErc721());
        row.set("block_number", contract.getBlockNumber());
        row.set("block_hash", contract.getBlockHash());
    }
}
