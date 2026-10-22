package com.githubassistant.backend.dto;

public class AskRepositoryRequest {

    private String repoName;
    private String question;

    public String getRepoName() {
        return repoName;
    }

    public void setRepoName(String repoName) {
        this.repoName = repoName;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }
}