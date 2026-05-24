package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Builder
public class TransactionDto {
    private Long id;
    private String referenceNumber;
    private String type;
    private BigDecimal amount;
    private BigDecimal balanceAfterTransaction;
    private String description;
    private String accountNumber;
    private String senderAccountNumber;
    private String senderName;
    private String receiverAccountNumber;
    private String receiverName;
    private String beneficiaryAccountNumber;
    private String beneficiaryName;
    private LocalDateTime createdAt;
}
