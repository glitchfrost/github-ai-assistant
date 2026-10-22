package com.githubassistant.backend.service;

import com.githubassistant.backend.dto.CodeFile;
import com.githubassistant.backend.dto.ai.AIFileDto;
import com.githubassistant.backend.dto.ai.IndexRepositoryRequestDto;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service
public class AIIndexingService {

    private final RestTemplate restTemplate;

    public AIIndexingService(
            RestTemplate restTemplate) {

        this.restTemplate = restTemplate;
    }

    public void indexRepository(
            String repoName,
            List<CodeFile> codeFiles) {

        List<AIFileDto> files =
                new ArrayList<>();

        for(CodeFile file : codeFiles) {

            files.add(
                    new AIFileDto(
                            file.getFileName(),
                            file.getContent()
                    )
            );
        }

        IndexRepositoryRequestDto request =
                new IndexRepositoryRequestDto();

        request.setRepoName(repoName);
        request.setFiles(files);

        HttpHeaders headers =
                new HttpHeaders();

        headers.setContentType(
                MediaType.APPLICATION_JSON
        );

        HttpEntity<IndexRepositoryRequestDto>
                entity =
                new HttpEntity<>(
                        request,
                        headers
                );

        restTemplate.postForObject(
                "http://localhost:8000/index-repository",
                entity,
                String.class
        );
    }
}