package com.githubassistant.backend.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class AIChatService {

    private final RestTemplate restTemplate;

    public AIChatService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public Object askQuestion(
            String repoName,
            String question) {

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, String> body = Map.of(
                "repoName", repoName,
                "question", question
        );

        HttpEntity<Map<String, String>> entity =
                new HttpEntity<>(body, headers);

        return restTemplate.postForObject(
                "http://localhost:8000/ask",
                entity,
                Object.class
        );
    }
}