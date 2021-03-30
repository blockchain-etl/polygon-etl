package io.blockchainetl.common;

import com.google.common.collect.Lists;
import org.apache.beam.sdk.testing.PAssert;
import org.apache.beam.sdk.values.PCollection;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class TestUtils {

    private static final Logger LOG = LoggerFactory.getLogger(TestUtils.class);

    public static List<String> readLines(String fileName) throws IOException {
        ClassLoader classLoader = TestUtils.class.getClassLoader();
        URL resource = classLoader.getResource(fileName);
        if (resource == null) {
            throw new IllegalArgumentException("The file " + fileName + " doesn't exist.");
        }
        File file = new File(resource.getFile());

        List<String> result = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                result.add(line);
            }
        }
        return result;
    }

    public static void logPCollection(PCollection<?> collection) {
        PAssert.that(collection).satisfies(result -> {
            ArrayList list = Lists.newArrayList(result);
            LOG.info("Output: ");
            LOG.info(list.toString());
            return null;
        });
    }
}
