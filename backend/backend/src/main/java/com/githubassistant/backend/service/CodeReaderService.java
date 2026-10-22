package com.githubassistant.backend.service;

import com.githubassistant.backend.dto.CodeFile;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Service
public class CodeReaderService {

    public List<CodeFile> readCodeFiles(String repoPath)
            throws IOException {

        List<CodeFile> files = new ArrayList<>();

        Files.walk(Path.of(repoPath))
                .filter(Files::isRegularFile)

                // Ignore unnecessary folders
                .filter(path -> {
                    String p = path.toString();

                    return !p.contains("node_modules")
                            && !p.contains(".git")
                            && !p.contains("target")
                            && !p.contains("build")
                            && !p.contains("dist");
                })

                // Supported file types
                .filter(path -> {
                    String file = path.toString().toLowerCase();

                    return file.endsWith(".java")
                            || file.endsWith(".js")
                            || file.endsWith(".jsx")
                            || file.endsWith(".ts")
                            || file.endsWith(".tsx")
                            || file.endsWith(".html")
                            || file.endsWith(".css")
                            || file.endsWith(".py")
                            || file.endsWith(".cpp")
                            || file.endsWith(".c")
                            || file.endsWith(".h")
                            || file.endsWith(".hpp")
                            || file.endsWith(".go")
                            || file.endsWith(".rs")
                            || file.endsWith(".php")
                            || file.endsWith(".json")
                            || file.endsWith(".xml")
                            || file.endsWith(".yaml")
                            || file.endsWith(".yml")
                            || file.endsWith(".sql")
                            || file.endsWith(".md");
                })

                .forEach(path -> {

                    try {

                        String content =
                                Files.readString(path);

                        files.add(
                                new CodeFile(
                                        path.toString(),
                                        content
                                )
                        );

                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                });

        return files;
    }
}