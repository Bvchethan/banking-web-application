package com.banking.app.controller;

import com.banking.app.dto.*;
import com.banking.app.service.*;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/customer")
@RequiredArgsConstructor
public class CustomerController {

    private final UserService userService;
    private final AccountService accountService;
    private final BeneficiaryService beneficiaryService;
    private final TransactionService transactionService;
    private final FraudDetectionService fraudDetectionService;
    private final FinancialInsightService financialInsightService;

    @GetMapping("/profile")
    public ResponseEntity<UserProfileDto> profile(Authentication authentication) {
        return ResponseEntity.ok(userService.getProfile(authentication.getName()));
    }

    @PutMapping("/profile")
    public ResponseEntity<UserProfileDto> updateProfile(
            Authentication authentication,
            @Valid @RequestBody ProfileUpdateRequest request
    ) {
        return ResponseEntity.ok(userService.updateProfile(authentication.getName(), request));
    }

    @GetMapping("/account")
    public ResponseEntity<AccountSummaryDto> account(Authentication authentication) {
        return ResponseEntity.ok(accountService.getAccountSummary(authentication.getName()));
    }

    @GetMapping("/beneficiaries")
    public ResponseEntity<List<BeneficiaryDto>> beneficiaries(Authentication authentication) {
        return ResponseEntity.ok(beneficiaryService.getBeneficiaries(authentication.getName()));
    }

    @PostMapping("/beneficiaries")
    public ResponseEntity<BeneficiaryDto> createBeneficiary(
            Authentication authentication,
            @Valid @RequestBody BeneficiaryRequest request
    ) {
        return ResponseEntity.ok(beneficiaryService.createBeneficiary(authentication.getName(), request));
    }

    @PutMapping("/beneficiaries/{id}")
    public ResponseEntity<BeneficiaryDto> updateBeneficiary(
            Authentication authentication,
            @PathVariable Long id,
            @Valid @RequestBody BeneficiaryRequest request
    ) {
        return ResponseEntity.ok(beneficiaryService.updateBeneficiary(authentication.getName(), id, request));
    }

    @DeleteMapping("/beneficiaries/{id}")
    public ResponseEntity<ApiResponse> deleteBeneficiary(Authentication authentication, @PathVariable Long id) {
        beneficiaryService.deleteBeneficiary(authentication.getName(), id);
        return ResponseEntity.ok(new ApiResponse("Beneficiary deleted successfully"));
    }

    @GetMapping("/transactions")
    public ResponseEntity<List<TransactionDto>> transactions(
            Authentication authentication,
            @RequestParam(required = false) String search
    ) {
        return ResponseEntity.ok(transactionService.getTransactions(authentication.getName(), search));
    }

    @PostMapping("/transfer")
    public ResponseEntity<TransactionDto> transfer(
            Authentication authentication,
            @Valid @RequestBody TransferRequest request
    ) {
        return ResponseEntity.ok(transactionService.transfer(authentication.getName(), request));
    }

    @GetMapping("/fraud-analytics")
    public ResponseEntity<List<FraudLogDto>> fraudAnalytics(Authentication authentication) {
        return ResponseEntity.ok(
                fraudDetectionService.getFraudLogs(accountService.getAccountByUserEmail(authentication.getName()))
        );
    }

    @GetMapping("/financial-insights")
    public ResponseEntity<FinancialInsightDto> financialInsights(Authentication authentication) {
        return ResponseEntity.ok(financialInsightService.getInsights(authentication.getName()));
    }
}
