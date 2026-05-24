package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AdminDashboardDto {
    private long totalCustomers;
    private long totalTransactions;
    private long highRiskTransactions;
    private String totalVolume;
}
