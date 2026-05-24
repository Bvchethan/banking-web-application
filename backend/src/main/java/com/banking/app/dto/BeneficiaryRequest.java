package com.banking.app.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BeneficiaryRequest {

    @NotBlank
    @Size(min = 2, max = 80)
    private String nickname;

    @NotBlank
    @Size(min = 3, max = 80)
    private String beneficiaryName;

    @NotBlank
    @Size(min = 8, max = 20)
    private String beneficiaryAccountNumber;

    @NotBlank
    @Size(min = 2, max = 20)
    private String bankName;

    @NotBlank
    @Size(min = 6, max = 15)
    private String ifscCode;
}
