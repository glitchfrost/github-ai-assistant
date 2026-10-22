package com.githubassistant.backend.controller;

import org.springframework.web.client.RestTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AITestController {

    @GetMapping("/ai-test")
    public String test() {

        RestTemplate restTemplate =
                new RestTemplate();

        return restTemplate.getForObject(
                "http://localhost:8000/",
                String.class
        );
    }
}