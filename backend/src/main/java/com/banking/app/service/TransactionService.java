package com.banking.app.service;

import com.banking.app.dto.TransactionDto;
import com.banking.app.dto.TransferRequest;
import com.banking.app.entity.*;
import com.banking.app.exception.BadRequestException;
import com.banking.app.repository.AccountRepository;
import com.banking.app.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final AccountService accountService;
    private final BeneficiaryService beneficiaryService;
    private final AccountRepository accountRepository;
    private final FraudDetectionService fraudDetectionService;

    public List<TransactionDto> getTransactions(String email, String search) {
        Account account = accountService.getAccountByUserEmail(email);
        List<BankTransaction> transactions = (search == null || search.isBlank())
                ? transactionRepository.findByAccountOrderByCreatedAtDesc(account)
                : transactionRepository.findByAccountOrderByCreatedAtDesc(account).stream()
                .filter(tx -> tx.getDescription().toLowerCase().contains(search.toLowerCase())
                        || tx.getReferenceNumber().toLowerCase().contains(search.toLowerCase())
                        || tx.getReceiverAccount().getUser().getFullName().toLowerCase().contains(search.toLowerCase())
                        || tx.getSenderAccount().getUser().getFullName().toLowerCase().contains(search.toLowerCase()))
                .toList();

        return transactions.stream().map(this::toDto).toList();
    }

    @Transactional
    public TransactionDto transfer(String email, TransferRequest request) {
        Account senderAccount = accountService.getAccountByUserEmail(email);
        Beneficiary beneficiary = beneficiaryService.findOwnedBeneficiary(email, request.getBeneficiaryId());
        Account receiverAccount = accountRepository.findByAccountNumberForUpdate(beneficiary.getBeneficiaryAccountNumber())
                .orElseThrow(() -> new BadRequestException("Receiver account not found for selected beneficiary"));

        senderAccount = accountRepository.findByIdForUpdate(senderAccount.getId())
                .orElseThrow(() -> new BadRequestException("Sender account not found"));

        if (!senderAccount.isActive()) {
            throw new BadRequestException("Sender account is inactive");
        }
        if (!receiverAccount.isActive()) {
            throw new BadRequestException("Receiver account is inactive");
        }
        if (senderAccount.getId().equals(receiverAccount.getId())) {
            throw new BadRequestException("Sender and receiver accounts cannot be the same");
        }
        if (request.getAmount().compareTo(senderAccount.getBalance()) > 0) {
            throw new BadRequestException("Insufficient balance");
        }

        senderAccount.setBalance(senderAccount.getBalance().subtract(request.getAmount()));
        receiverAccount.setBalance(receiverAccount.getBalance().add(request.getAmount()));
        accountRepository.save(senderAccount);
        accountRepository.save(receiverAccount);

        String referenceNumber = "TXN-" + UUID.randomUUID().toString().substring(0, 10).toUpperCase();

        BankTransaction senderTransaction = buildTransaction(
                senderAccount,
                senderAccount,
                receiverAccount,
                referenceNumber,
                TransactionType.DEBIT,
                request.getAmount(),
                senderAccount.getBalance(),
                request.getDescription(),
                beneficiary.getBeneficiaryName(),
                beneficiary.getBeneficiaryAccountNumber()
        );

        BankTransaction receiverTransaction = buildTransaction(
                receiverAccount,
                senderAccount,
                receiverAccount,
                referenceNumber,
                TransactionType.CREDIT,
                request.getAmount(),
                receiverAccount.getBalance(),
                "Incoming transfer: " + request.getDescription(),
                senderAccount.getUser().getFullName(),
                senderAccount.getAccountNumber()
        );

        BankTransaction savedSenderTransaction = transactionRepository.save(senderTransaction);
        transactionRepository.save(receiverTransaction);
        fraudDetectionService.analyzeAndStore(senderAccount, beneficiary, savedSenderTransaction);
        return toDto(savedSenderTransaction);
    }

    public BigDecimal getTotalVolume() {
        return transactionRepository.findAll().stream()
                .map(BankTransaction::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    private TransactionDto toDto(BankTransaction transaction) {
        Account senderAccount = transaction.getSenderAccount() != null ? transaction.getSenderAccount() : transaction.getAccount();
        Account receiverAccount = transaction.getReceiverAccount() != null ? transaction.getReceiverAccount() : transaction.getAccount();

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

    private BankTransaction buildTransaction(
            Account ledgerAccount,
            Account senderAccount,
            Account receiverAccount,
            String referenceNumber,
            TransactionType type,
            BigDecimal amount,
            BigDecimal balanceAfterTransaction,
            String description,
            String beneficiaryName,
            String beneficiaryAccountNumber
    ) {
        BankTransaction transaction = new BankTransaction();
        transaction.setAccount(ledgerAccount);
        transaction.setSenderAccount(senderAccount);
        transaction.setReceiverAccount(receiverAccount);
        transaction.setReferenceNumber(referenceNumber);
        transaction.setType(type);
        transaction.setAmount(amount);
        transaction.setBalanceAfterTransaction(balanceAfterTransaction);
        transaction.setDescription(description);
        transaction.setBeneficiaryName(beneficiaryName);
        transaction.setBeneficiaryAccountNumber(beneficiaryAccountNumber);
        return transaction;
    }
}
