package io.blockchainetl.common;

import com.google.api.services.bigquery.model.TableRow;
import org.apache.beam.sdk.transforms.DoFn;

public class TableRowsToStringsFn extends DoFn<TableRow, String> {

    @ProcessElement
    public void processElement(ProcessContext c) throws Exception {
        c.output(c.element().toString());
    }
}
