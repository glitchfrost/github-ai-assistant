package com.githubassistant.backend.service;

import com.githubassistant.backend.dto.GitHubRepoResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class GitHubService {

    private final RestTemplate restTemplate;

    public GitHubService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public GitHubRepoResponse fetchRepositoryDetails(String githubUrl) {

        String[] repoInfo = extractOwnerAndRepo(githubUrl);

        String owner = repoInfo[0];
        String repo = repoInfo[1];

        String apiUrl =
                "https://api.github.com/repos/" + owner + "/" + repo;

        return restTemplate.getForObject(
                apiUrl,
                GitHubRepoResponse.class
        );
    }

    private String[] extractOwnerAndRepo(String githubUrl) {

        String[] parts = githubUrl.split("/");

        String owner = parts[3];
        String repo = parts[4];

        return new String[]{owner, repo};
    }
}