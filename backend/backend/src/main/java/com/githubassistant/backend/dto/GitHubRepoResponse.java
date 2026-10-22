package com.githubassistant.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GitHubRepoResponse {

    private String name;

    private String description;

    @JsonProperty("stargazers_count")
    private Integer stargazersCount;

    @JsonProperty("forks_count")
    private Integer forksCount;

    private String language;

    public GitHubRepoResponse() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Integer getStargazersCount() {
        return stargazersCount;
    }

    public void setStargazersCount(Integer stargazersCount) {
        this.stargazersCount = stargazersCount;
    }

    public Integer getForksCount() {
        return forksCount;
    }

    public void setForksCount(Integer forksCount) {
        this.forksCount = forksCount;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }
}