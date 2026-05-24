package com.banking.app.repository;

import com.banking.app.entity.Account;
import com.banking.app.entity.FraudLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface FraudLogRepository extends JpaRepository<FraudLog, Long> {
    @Query("select f from FraudLog f where f.transaction.account = :account order by f.analyzedAt desc")
    List<FraudLog> findByAccountOrderByAnalyzedAtDesc(@Param("account") Account account);
}
