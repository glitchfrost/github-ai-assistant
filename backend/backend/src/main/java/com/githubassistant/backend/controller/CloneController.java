package com.githubassistant.backend.controller;

import com.githubassistant.backend.service.RepositoryCloneService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CloneController {

    private final RepositoryCloneService cloneService;

    public CloneController(
            RepositoryCloneService cloneService) {

        this.cloneService = cloneService;
    }

    @GetMapping("/clone")
    public String cloneRepo(
            @RequestParam String url)
            throws Exception {

        return cloneService.cloneRepository(url);
    }
}