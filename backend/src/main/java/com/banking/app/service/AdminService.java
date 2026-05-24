package com.banking.app.service;

import com.banking.app.dto.AdminDashboardDto;
import com.banking.app.dto.FraudLogDto;
import com.banking.app.dto.TransactionDto;
import com.banking.app.dto.UserProfileDto;
import com.banking.app.entity.RiskLevel;
import com.banking.app.entity.User;
import com.banking.app.repository.FraudLogRepository;
import com.banking.app.repository.TransactionRepository;
import com.banking.app.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AdminService {

    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;
    private final FraudLogRepository fraudLogRepository;
    private final TransactionService transactionService;

    public AdminDashboardDto getDashboard() {
        long highRiskTransactions = fraudLogRepository.findAll().stream()
                .filter(log -> log.getRiskLevel() == RiskLevel.HIGH)
                .count();

        return AdminDashboardDto.builder()
                .totalCustomers(userRepository.findAll().stream()
                        .filter(user -> user.getRoles().stream().anyMatch(role -> role.getName().name().equals("ROLE_CUSTOMER")))
                        .count())
                .totalTransactions(transactionRepository.count())
                .highRiskTransactions(highRiskTransactions)
                .totalVolume(transactionService.getTotalVolume().toPlainString())
                .build();
    }

    public List<UserProfileDto> getCustomers(String search) {
        List<User> users = (search == null || search.isBlank())
                ? userRepository.findAll()
                : userRepository.findByFullNameContainingIgnoreCaseOrEmailContainingIgnoreCase(search, search);

        return users.stream()
                .filter(user -> user.getRoles().stream().anyMatch(role -> role.getName().name().equals("ROLE_CUSTOMER")))
                .map(user -> UserProfileDto.builder()
                        .id(user.getId())
                        .fullName(user.getFullName())
                        .email(user.getEmail())
                        .phone(user.getPhone())
                        .address(user.getAddress())
                        .createdAt(user.getCreatedAt())
                        .roles(user.getRoles().stream().map(role -> role.getName().name()).toList())
                        .build())
                .toList();
    }

    public List<TransactionDto> getAllTransactions(String search) {
        return ((search == null || search.isBlank())
                ? transactionRepository.findAll()
                : transactionRepository.findByDescriptionContainingIgnoreCaseOrReferenceNumberContainingIgnoreCaseOrderByCreatedAtDesc(search, search))
                .stream()
                .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
                .map(this::toDto)
                .toList();
    }

    public List<FraudLogDto> getAllFraudLogs() {
        return fraudLogRepository.findAll().stream()
                .sorted((a, b) -> b.getAnalyzedAt().compareTo(a.getAnalyzedAt()))
                .map(log -> FraudLogDto.builder()
                        .id(log.getId())
                        .referenceNumber(log.getTransaction().getReferenceNumber())
                        .riskScore(log.getRiskScore())
                        .riskLevel(log.getRiskLevel().name())
                        .evaluatedAmount(log.getEvaluatedAmount())
                        .reasons(log.getReasons())
                        .analyzedAt(log.getAnalyzedAt())
                        .build())
                .toList();
    }

    private TransactionDto toDto(com.banking.app.entity.BankTransaction transaction) {
        var senderAccount = transaction.getSenderAccount() != null ? transaction.getSenderAccount() : transaction.getAccount();
        var receiverAccount = transaction.getReceiverAccount() != null ? transaction.getReceiverAccount() : transaction.getAccount();

        return TransactionDto.builder()
                .id(transaction.getId())
                .referenceNumber(transaction.getReferenceNumber())
                .type(transaction.getType().name())
                .amount(transaction.getAmount())
                .balanceAfterTransaction(transaction.getBalanceAfterTransaction())
                .description(transaction.getDescription())
                .accountNumber(transaction.getAccount().getAccountNumber())
                .senderAccountNumber(senderAccount.getAccountNumber())
                .senderName(senderAccount.getUser().getFullName())
                .receiverAccountNumber(receiverAccount.getAccountNumber())
                .receiverName(receiverAccount.getUser().getFullName())
                .beneficiaryAccountNumber(transaction.getBeneficiaryAccountNumber())
                .beneficiaryName(transaction.getBeneficiaryName())
                .createdAt(transaction.getCreatedAt())
                .build();
    }
}
