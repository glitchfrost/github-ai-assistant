package com.githubassistant.backend.repository;

import com.githubassistant.backend.entity.RepositoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepositoryRepository
        extends JpaRepository<RepositoryEntity, Long> {
}