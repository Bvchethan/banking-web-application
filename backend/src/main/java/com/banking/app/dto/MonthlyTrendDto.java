package com.banking.app.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
@AllArgsConstructor
public class MonthlyTrendDto {
    private String month;
    private BigDecimal credit;
    private BigDecimal debit;
}
