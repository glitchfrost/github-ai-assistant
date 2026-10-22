package com.githubassistant.backend.controller;

import com.githubassistant.backend.dto.AnalyzeRepositoryRequest;
import com.githubassistant.backend.dto.AskRepositoryRequest;
import com.githubassistant.backend.service.AIChatService;
import com.githubassistant.backend.dto.CodeFile;
import com.githubassistant.backend.dto.RepositoryRequest;
import com.githubassistant.backend.entity.RepositoryEntity;
import com.githubassistant.backend.service.*;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/repositories")
public class RepositoryController {

    private final RepositoryService repositoryService;
    private final RepositoryCloneService cloneService;
    private final CodeReaderService codeReaderService;
    private final AIIndexingService aiIndexingService;
    private final AIChatService aiChatService;


    public RepositoryController(
            RepositoryService repositoryService,
            RepositoryCloneService cloneService,
            CodeReaderService codeReaderService,
            AIIndexingService aiIndexingService,
            AIChatService aiChatService) {

        this.repositoryService = repositoryService;
        this.cloneService = cloneService;
        this.codeReaderService = codeReaderService;
        this.aiIndexingService = aiIndexingService;
        this.aiChatService = aiChatService;
    }

    @PostMapping
    public RepositoryEntity createRepository(
            @RequestBody RepositoryRequest request) {

        return repositoryService.saveRepository(request);
    }

    @GetMapping
    public List<RepositoryEntity> getAllRepositories() {

        return repositoryService.getAllRepositories();
    }

    @PostMapping("/chat")
    public Object chat(
            @RequestBody AskRepositoryRequest request) {

        return aiChatService.askQuestion(
                request.getRepoName(),
                request.getQuestion()
        );
    }

    @PostMapping("/analyze")
    public String analyzeRepository(
            @RequestBody AnalyzeRepositoryRequest request)
            throws Exception {

        // 1. Clone the repository locally
        String repoPath =
                cloneService.cloneRepository(
                        request.getGithubUrl()
                );

        // 2. Read all Java source files
        List<CodeFile> files =
                codeReaderService.readCodeFiles(repoPath);

        // 3. Extract repo name from URL
        String repoName =
                request.getGithubUrl()
                        .substring(
                                request.getGithubUrl()
                                        .lastIndexOf("/") + 1
                        );

        // 4. Index code into ChromaDB via AI service
        aiIndexingService.indexRepository(
                repoName,
                files
        );

        // 5. Save repository metadata to MySQL so it appears on the dashboard
        //    Wrapped in try-catch: if GitHub API is rate-limited or unavailable,
        //    we still save basic info so the repo appears in the list.
        try {
            RepositoryRequest saveRequest = new RepositoryRequest();
            saveRequest.setGithubUrl(request.getGithubUrl());
            repositoryService.saveRepository(saveRequest);
        } catch (Exception saveEx) {
            // Fallback: save minimal info directly without GitHub API
            repositoryService.saveRepositoryDirect(request.getGithubUrl(), repoName);
        }

        return "Repository \"" + repoName + "\" indexed and saved successfully. " +
               files.size() + " files processed.";
    }
}