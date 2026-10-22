package com.githubassistant.backend.controller;

import com.githubassistant.backend.dto.RepositoryStats;
import com.githubassistant.backend.service.RepositoryScannerService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ScanController {

    private final RepositoryScannerService scannerService;

    public ScanController(
            RepositoryScannerService scannerService) {

        this.scannerService = scannerService;
    }

    @GetMapping("/scan")
    public RepositoryStats scan(
            @RequestParam String path)
            throws Exception {

        return scannerService.scanRepository(path);
    }
}