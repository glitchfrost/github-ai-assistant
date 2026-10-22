package com.githubassistant.backend.service;

import com.githubassistant.backend.dto.RepositoryStats;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

@Service
public class RepositoryScannerService {

    public RepositoryStats scanRepository(String repoPath)
            throws IOException {

        RepositoryStats stats = new RepositoryStats();

        try (Stream<Path> paths = Files.walk(Path.of(repoPath))) {

            paths.filter(Files::isRegularFile)
                    .forEach(file -> {

                        stats.setTotalFiles(
                                stats.getTotalFiles() + 1
                        );

                        String name =
                                file.getFileName()
                                        .toString()
                                        .toLowerCase();

                        if(name.endsWith(".java")) {
                            stats.setJavaFiles(
                                    stats.getJavaFiles() + 1
                            );
                        }

                        if(name.endsWith(".js")) {
                            stats.setJsFiles(
                                    stats.getJsFiles() + 1
                            );
                        }

                        if(name.endsWith(".py")) {
                            stats.setPyFiles(
                                    stats.getPyFiles() + 1
                            );
                        }

                        if(name.endsWith(".md")) {
                            stats.setMdFiles(
                                    stats.getMdFiles() + 1
                            );
                        }
                    });
        }

        return stats;
    }
}