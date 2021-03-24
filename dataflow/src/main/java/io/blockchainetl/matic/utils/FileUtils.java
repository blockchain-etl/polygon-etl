package io.blockchainetl.matic.utils;

import java.io.IOException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class FileUtils {

    public static String readFile(String path) {
        byte[] encoded;
        try {
            encoded = Files.readAllBytes(Paths.get(path));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return new String(encoded, StandardCharsets.UTF_8);
    }

    public static String readFileFromClasspath(String path) {
        URL resource = FileUtils.class.getClassLoader().getResource(path);
        if (resource == null) {
            throw new IllegalArgumentException("Resource not found: " + path);
        }
        return readFile(resource.getPath());
    }
}
