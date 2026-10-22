package com.githubassistant.backend.service;

import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;

@Service
public class RepositoryCloneService {

    public String cloneRepository(String githubUrl)
            throws IOException, InterruptedException {

        String repoName =
                githubUrl.substring(
                        githubUrl.lastIndexOf("/") + 1
                );

        String destination =
                "uploads/" + repoName;

        File folder = new File(destination);

        if(folder.exists()) {
            return destination;
        }

        ProcessBuilder processBuilder =
                new ProcessBuilder(
                        "git",
                        "clone",
                        githubUrl,
                        destination
                );

        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();

        int exitCode = process.waitFor();

        if(exitCode != 0) {
            throw new RuntimeException(
                    "Failed to clone repository"
            );
        }

        return destination;
    }
}