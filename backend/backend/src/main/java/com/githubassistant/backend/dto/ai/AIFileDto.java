package com.githubassistant.backend.dto.ai;

public class AIFileDto {

    private String fileName;
    private String content;

    public AIFileDto() {
    }

    public AIFileDto(String fileName, String content) {
        this.fileName = fileName;
        this.content = content;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}