package com.banking.app.service;

import com.banking.app.dto.AccountSummaryDto;
import com.banking.app.entity.Account;
import com.banking.app.exception.ResourceNotFoundException;
import com.banking.app.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AccountService {

    private final AccountRepository accountRepository;
    private final UserService userService;

    public Account getAccountByUserEmail(String email) {
        return accountRepository.findByUser(userService.getUserByEmail(email))
                .orElseThrow(() -> new ResourceNotFoundException("Account not found"));
    }

    public AccountSummaryDto getAccountSummary(String email) {
        Account account = getAccountByUserEmail(email);
        return AccountSummaryDto.builder()
                .accountId(account.getId())
                .accountNumber(account.getAccountNumber())
                .balance(account.getBalance())
                .currency(account.getCurrency())
                .build();
    }
}
