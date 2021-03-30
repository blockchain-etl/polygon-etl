package io.blockchainetl.common.fns;

import io.blockchainetl.common.utils.TimeUtils;
import org.codehaus.jackson.JsonNode;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class IsoTimestampParser implements TimestampParser {

    private DateTimeFormatter formatter;

    public IsoTimestampParser(DateTimeFormatter formatter) {
        this.formatter = formatter;
    }

    @Override
    public ZonedDateTime parse(JsonNode timestampNode) {
        String timestamp = timestampNode.getTextValue();
        return TimeUtils.convertToZonedDateTime(timestamp, formatter);
    }
}
