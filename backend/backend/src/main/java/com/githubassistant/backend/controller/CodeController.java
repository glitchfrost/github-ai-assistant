package com.githubassistant.backend.controller;

import com.githubassistant.backend.dto.CodeFile;
import com.githubassistant.backend.service.CodeReaderService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class CodeController {

    private final CodeReaderService codeReaderService;

    public CodeController(
            CodeReaderService codeReaderService) {

        this.codeReaderService = codeReaderService;
    }

    @GetMapping("/code")
    public List<CodeFile> getCode(
            @RequestParam String path)
            throws Exception {

        return codeReaderService.readCodeFiles(path);
    }
}