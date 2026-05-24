package com.banking.app.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class TransferRequest {

    @NotNull
    private Long beneficiaryId;

    @NotNull
    @DecimalMin(value = "1.00", message = "Amount must be at least 1")
    private BigDecimal amount;

    @NotBlank
    @Size(min = 5, max = 200)
    private String description;
}
