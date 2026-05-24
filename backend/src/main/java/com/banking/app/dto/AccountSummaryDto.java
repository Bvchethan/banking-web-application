package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@Builder
public class AccountSummaryDto {
    private Long accountId;
    private String accountNumber;
    private BigDecimal balance;
    private String currency;
}
