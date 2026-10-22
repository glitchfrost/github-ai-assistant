package com.githubassistant.backend.dto;

public class AnalyzeRepositoryRequest {

    private String githubUrl;

    public String getGithubUrl() {
        return githubUrl;
    }

    public void setGithubUrl(String githubUrl) {
        this.githubUrl = githubUrl;
    }
}