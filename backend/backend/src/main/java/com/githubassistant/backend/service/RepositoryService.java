package com.githubassistant.backend.service;

import com.githubassistant.backend.dto.GitHubRepoResponse;
import com.githubassistant.backend.dto.RepositoryRequest;
import com.githubassistant.backend.entity.RepositoryEntity;
import com.githubassistant.backend.repository.RepositoryRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class RepositoryService {

    private final RepositoryRepository repositoryRepository;
    private final GitHubService gitHubService;

    public RepositoryService(
            RepositoryRepository repositoryRepository,
            GitHubService gitHubService) {

        this.repositoryRepository = repositoryRepository;
        this.gitHubService = gitHubService;
    }

    public RepositoryEntity saveRepository(RepositoryRequest request) {

        // Avoid duplicate entries for the same URL
        List<RepositoryEntity> existing = repositoryRepository.findAll();
        for (RepositoryEntity e : existing) {
            if (request.getGithubUrl().equals(e.getGithubUrl())) {
                return e;
            }
        }

        GitHubRepoResponse githubRepo =
                gitHubService.fetchRepositoryDetails(
                        request.getGithubUrl()
                );

        RepositoryEntity repo = new RepositoryEntity();

        repo.setRepoName(githubRepo.getName());
        repo.setGithubUrl(request.getGithubUrl());
        repo.setDescription(githubRepo.getDescription());
        repo.setStars(githubRepo.getStargazersCount());
        repo.setForks(githubRepo.getForksCount());
        repo.setLanguage(githubRepo.getLanguage());

        String[] parts =
                request.getGithubUrl().split("/");

        repo.setOwner(parts[3]);

        repo.setCreatedAt(LocalDateTime.now());

        return repositoryRepository.save(repo);
    }

    public List<RepositoryEntity> getAllRepositories() {
        return repositoryRepository.findAll();
    }

    public RepositoryEntity saveRepositoryDirect(String githubUrl, String repoName) {
        // Check if already exists to avoid duplicates
        List<RepositoryEntity> existing = repositoryRepository.findAll();
        for (RepositoryEntity e : existing) {
            if (githubUrl.equals(e.getGithubUrl())) {
                return e; // already saved, skip
            }
        }

        String[] parts = githubUrl.split("/");
        String owner = parts.length > 3 ? parts[3] : "unknown";

        RepositoryEntity repo = new RepositoryEntity();
        repo.setRepoName(repoName);
        repo.setGithubUrl(githubUrl);
        repo.setOwner(owner);
        repo.setDescription("Analyzed repository");
        repo.setStars(0);
        repo.setForks(0);
        repo.setLanguage("Java");
        repo.setCreatedAt(java.time.LocalDateTime.now());

        return repositoryRepository.save(repo);
    }
}