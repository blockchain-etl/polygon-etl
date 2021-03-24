package io.blockchainetl.common.fns;

import io.blockchainetl.common.utils.TimeUtils;
import org.codehaus.jackson.JsonNode;

import java.time.ZonedDateTime;

public class UnixTimestampParser implements TimestampParser {
    
    @Override
    public ZonedDateTime parse(JsonNode timestampNode) {
        long timestamp = timestampNode.getLongValue();
        return TimeUtils.convertToZonedDateTime(timestamp);
    }
}
