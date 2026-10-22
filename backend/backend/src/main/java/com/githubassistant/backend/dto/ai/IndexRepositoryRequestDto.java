package com.githubassistant.backend.dto.ai;

import java.util.List;

public class IndexRepositoryRequestDto {

    private String repoName;
    private List<AIFileDto> files;

    public String getRepoName() {
        return repoName;
    }

    public void setRepoName(String repoName) {
        this.repoName = repoName;
    }

    public List<AIFileDto> getFiles() {
        return files;
    }

    public void setFiles(List<AIFileDto> files) {
        this.files = files;
    }
}