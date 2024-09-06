package com.moody.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.moody.domain.BookEntity;

@Repository
public interface BookRepository extends JpaRepository<BookEntity, String> {
}
