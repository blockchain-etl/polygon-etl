package io.blockchainetl.common.fns;

import io.blockchainetl.eos.fns.EosConstants;

import java.util.HashMap;
import java.util.Map;

/**
 * Hack. Because in Dataflow/Beam all Fns must be serializable. Will inject in Fn only parser key. 
 */
public class TimestampParserRepository {
    
    public static final Map<String, TimestampParser> PARSERS = new HashMap<>();

    public static final String KEY_EOS = "eos";
    public static final String KEY_UNIX = "unix";

    static {
        PARSERS.put(KEY_EOS, new IsoTimestampParser(EosConstants.DATE_TIME_FORMATTER));
        PARSERS.put(KEY_UNIX, new UnixTimestampParser());
    }
}
