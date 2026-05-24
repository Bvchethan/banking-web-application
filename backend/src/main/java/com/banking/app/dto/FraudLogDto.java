package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Builder
public class FraudLogDto {
    private Long id;
    private String referenceNumber;
    private Integer riskScore;
    private String riskLevel;
    private BigDecimal evaluatedAmount;
    private String reasons;
    private LocalDateTime analyzedAt;
}
