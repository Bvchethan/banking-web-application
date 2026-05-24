package com.banking.app.service;

import com.banking.app.dto.FraudLogDto;
import com.banking.app.entity.*;
import com.banking.app.repository.FraudLogRepository;
import com.banking.app.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class FraudDetectionService {

    private final TransactionRepository transactionRepository;
    private final FraudLogRepository fraudLogRepository;

    @Transactional
    public FraudLog analyzeAndStore(Account account, Beneficiary beneficiary, BankTransaction transaction) {
        int score = 5;
        List<String> reasons = new ArrayList<>();

        if (transaction.getAmount().compareTo(new BigDecimal("50000")) >= 0) {
            score += 40;
            reasons.add("Large transaction amount");
        }

        long recentTransactionCount = transactionRepository.countByAccountAndCreatedAtAfter(
                account,
                LocalDateTime.now().minusMinutes(10)
        );
        if (recentTransactionCount >= 3) {
            score += 30;
            reasons.add("Multiple rapid transactions");
        }

        if (beneficiary.getCreatedAt() != null && beneficiary.getCreatedAt().isAfter(LocalDateTime.now().minusDays(2))) {
            score += 25;
            reasons.add("Transfer to new beneficiary");
        }

        RiskLevel level = score >= 70 ? RiskLevel.HIGH : score >= 35 ? RiskLevel.MEDIUM : RiskLevel.LOW;
        if (reasons.isEmpty()) {
            reasons.add("No strong fraud indicators");
        }

        FraudLog fraudLog = new FraudLog();
        fraudLog.setTransaction(transaction);
        fraudLog.setRiskScore(Math.min(score, 100));
        fraudLog.setRiskLevel(level);
        fraudLog.setEvaluatedAmount(transaction.getAmount());
        fraudLog.setReasons(String.join(", ", reasons));
        return fraudLogRepository.save(fraudLog);
    }

    public List<FraudLogDto> getFraudLogs(Account account) {
        return fraudLogRepository.findByAccountOrderByAnalyzedAtDesc(account).stream()
                .map(log -> FraudLogDto.builder()
                        .id(log.getId())
                        .referenceNumber(log.getTransaction().getReferenceNumber())
                        .riskScore(log.getRiskScore())
                        .riskLevel(log.getRiskLevel().name())
                        .evaluatedAmount(log.getEvaluatedAmount())
                        .reasons(log.getReasons())
                        .analyzedAt(log.getAnalyzedAt())
                        .build())
                .toList();
    }
}
