package com.githubassistant.backend.dto;

public class RepositoryStats {

    private int totalFiles;
    private int javaFiles;
    private int jsFiles;
    private int pyFiles;
    private int mdFiles;

    public int getTotalFiles() {
        return totalFiles;
    }

    public void setTotalFiles(int totalFiles) {
        this.totalFiles = totalFiles;
    }

    public int getJavaFiles() {
        return javaFiles;
    }

    public void setJavaFiles(int javaFiles) {
        this.javaFiles = javaFiles;
    }

    public int getJsFiles() {
        return jsFiles;
    }

    public void setJsFiles(int jsFiles) {
        this.jsFiles = jsFiles;
    }

    public int getPyFiles() {
        return pyFiles;
    }

    public void setPyFiles(int pyFiles) {
        this.pyFiles = pyFiles;
    }

    public int getMdFiles() {
        return mdFiles;
    }

    public void setMdFiles(int mdFiles) {
        this.mdFiles = mdFiles;
    }
}