package io.blockchainetl.common.fns;

import org.codehaus.jackson.JsonNode;

import java.time.ZonedDateTime;

public interface TimestampParser {
    ZonedDateTime parse(JsonNode timestampNode);
}
