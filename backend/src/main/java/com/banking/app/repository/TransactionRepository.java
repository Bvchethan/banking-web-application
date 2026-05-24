package com.banking.app.repository;

import com.banking.app.entity.Account;
import com.banking.app.entity.BankTransaction;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDateTime;
import java.util.List;

public interface TransactionRepository extends JpaRepository<BankTransaction, Long> {
    List<BankTransaction> findByAccountOrderByCreatedAtDesc(Account account);
    List<BankTransaction> findByCreatedAtBetweenOrderByCreatedAtDesc(LocalDateTime from, LocalDateTime to);
    long countByAccountAndCreatedAtAfter(Account account, LocalDateTime createdAt);
    List<BankTransaction> findByDescriptionContainingIgnoreCaseOrReferenceNumberContainingIgnoreCaseOrderByCreatedAtDesc(
            String description, String referenceNumber
    );
}
