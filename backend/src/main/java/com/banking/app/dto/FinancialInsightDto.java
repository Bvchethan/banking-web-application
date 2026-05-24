package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.math.BigDecimal;
import java.util.List;

@Getter
@Builder
public class FinancialInsightDto {
    private int financialHealthScore;
    private BigDecimal totalDebits;
    private BigDecimal totalCredits;
    private BigDecimal savingsRate;
    private List<MonthlyTrendDto> monthlyTrends;
    private List<String> smartSuggestions;
}
