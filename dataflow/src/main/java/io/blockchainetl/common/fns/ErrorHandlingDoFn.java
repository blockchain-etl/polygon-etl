package io.blockchainetl.common.fns;

import org.apache.beam.sdk.transforms.DoFn;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public abstract class ErrorHandlingDoFn<F, T> extends DoFn<F, T> {

    private static final Logger LOG = LoggerFactory.getLogger(ErrorHandlingDoFn.class);
    
    @ProcessElement
    public void processElement(ProcessContext c) throws Exception {
        try {
            doProcessElement(c);
        } catch (Exception e) {
            // https://cloud.google.com/blog/products/gcp/handling-invalid-inputs-in-dataflow
            LOG.error("Failed to process input {}.", c.element(), e);
            // OutOfMemoryError should be retried
            if (e.getCause() instanceof OutOfMemoryError || 
                (e.getCause() != null && e.getCause().getCause() instanceof OutOfMemoryError)) {
                throw e;
            }
        }
    }

    protected abstract void doProcessElement(ProcessContext c) throws Exception;
}
