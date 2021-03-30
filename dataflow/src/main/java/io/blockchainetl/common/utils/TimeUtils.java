package io.blockchainetl.common.utils;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class TimeUtils {

    private static final ZoneId UTC = ZoneId.of("UTC");

    private static final DateTimeFormatter TIMESTAMP_FORMATTER = DateTimeFormatter
        .ofPattern("yyyy-MM-dd'T'HH:mm:ss[.SSS]'Z'").withZone(UTC);
    private static final DateTimeFormatter TIMESTAMP_MONTH_FORMATTER = DateTimeFormatter
        .ofPattern("yyyy-MM-dd").withZone(ZoneId.of("UTC"));
    
    
    public static ZonedDateTime convertToZonedDateTime(Long unixTimestamp) {
        Instant blockInstant = Instant.ofEpochSecond(unixTimestamp);
        return ZonedDateTime.from(blockInstant.atZone(UTC));
    }

    public static ZonedDateTime convertToZonedDateTime(String timestamp, DateTimeFormatter formatter) {
        return ZonedDateTime.parse(timestamp, formatter.withZone(UTC));
    }
    
    public static String formatTimestamp(ZonedDateTime dateTime) {
        return TIMESTAMP_FORMATTER.format(dateTime); 
    }

    public static String formatDate(ZonedDateTime dateTime) {
        return TIMESTAMP_MONTH_FORMATTER.format(dateTime);
    }
    
    public static ZonedDateTime parseDateTime(String str) {
        return ZonedDateTime.parse(str, TIMESTAMP_FORMATTER);
    }
}
