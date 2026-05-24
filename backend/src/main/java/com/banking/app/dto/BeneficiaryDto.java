package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class BeneficiaryDto {
    private Long id;
    private String nickname;
    private String beneficiaryName;
    private String beneficiaryAccountNumber;
    private String bankName;
    private String ifscCode;
    private LocalDateTime createdAt;
}
