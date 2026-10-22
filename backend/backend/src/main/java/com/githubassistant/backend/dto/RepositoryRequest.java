package com.githubassistant.backend.dto;

public class RepositoryRequest {

    private String githubUrl;

    public RepositoryRequest() {
    }

    public String getGithubUrl() {
        return githubUrl;
    }

    public void setGithubUrl(String githubUrl) {
        this.githubUrl = githubUrl;
    }
}