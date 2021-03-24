package io.blockchainetl.matic.fns;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.api.services.bigquery.model.TableRow;
import org.apache.beam.sdk.transforms.SerializableFunction;
import org.slf4j.Logger;

/**
 * Converts entity json string to TableRow.
 */
public class EntityJsonToTableRow implements SerializableFunction<String, TableRow> {

    private static final Logger LOG = org.slf4j.LoggerFactory.getLogger(EntityJsonToTableRow.class);
    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Override
    public TableRow apply(String json) {
        try {
            TableRow tableRow = MAPPER.readValue(json, TableRow.class);
            LOG.trace("Table Row: {}", tableRow.toPrettyString());
            return tableRow;
        } catch (Exception e) {
            LOG.error("Error converting json to TableRow. Json: " + json, e);
            throw new IllegalArgumentException("Error converting json to TableRow", e);
        }
    }
}
