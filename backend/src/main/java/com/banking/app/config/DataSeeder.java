package com.banking.app.config;

import com.banking.app.entity.*;
import com.banking.app.repository.AccountRepository;
import com.banking.app.repository.BeneficiaryRepository;
import com.banking.app.repository.RoleRepository;
import com.banking.app.repository.TransactionRepository;
import com.banking.app.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.Set;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final AccountRepository accountRepository;
    private final BeneficiaryRepository beneficiaryRepository;
    private final TransactionRepository transactionRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        Role adminRole = roleRepository.findByName(RoleName.ROLE_ADMIN).orElseGet(() -> {
            Role role = new Role();
            role.setName(RoleName.ROLE_ADMIN);
            return roleRepository.save(role);
        });

        Role customerRole = roleRepository.findByName(RoleName.ROLE_CUSTOMER).orElseGet(() -> {
            Role role = new Role();
            role.setName(RoleName.ROLE_CUSTOMER);
            return roleRepository.save(role);
        });

        if (!userRepository.existsByEmail("admin@bank.com")) {
            User admin = new User();
            admin.setFullName("System Admin");
            admin.setEmail("admin@bank.com");
            admin.setPhone("9999999999");
            admin.setAddress("Head Office, Mumbai");
            admin.setPassword(passwordEncoder.encode("Admin@123"));
            admin.setRoles(Set.of(adminRole));
            userRepository.save(admin);
        }

        if (!userRepository.existsByEmail("john@bank.com")) {
            User customer = new User();
            customer.setFullName("John Carter");
            customer.setEmail("john@bank.com");
            customer.setPhone("8888888888");
            customer.setAddress("Bengaluru, Karnataka");
            customer.setPassword(passwordEncoder.encode("Customer@123"));
            customer.setRoles(Set.of(customerRole));
            userRepository.save(customer);
        }

        if (!userRepository.existsByEmail("jane@bank.com")) {
            User customer = new User();
            customer.setFullName("Jane Doe");
            customer.setEmail("jane@bank.com");
            customer.setPhone("7777777777");
            customer.setAddress("Hyderabad, Telangana");
            customer.setPassword(passwordEncoder.encode("Customer@123"));
            customer.setRoles(Set.of(customerRole));
            userRepository.save(customer);
        }

        seedDemoAccountData("john@bank.com", "AC100000002", new BigDecimal("125000.00"));
        seedDemoAccountData("jane@bank.com", "AC100000003", new BigDecimal("45000.00"));
        seedBeneficiary("john@bank.com", "jane@bank.com", "Jane");
        seedBeneficiary("jane@bank.com", "john@bank.com", "John");
    }

    private void seedDemoAccountData(String email, String accountNumber, BigDecimal balance) {
        User user = userRepository.findByEmail(email).orElseThrow();
        Account account = accountRepository.findByUser(user)
                .or(() -> accountRepository.findByAccountNumber(accountNumber))
                .map(existingAccount -> {
                    existingAccount.setUser(user);
                    if (existingAccount.getAccountNumber() == null || existingAccount.getAccountNumber().isBlank()) {
                        existingAccount.setAccountNumber(accountNumber);
                    }
                    if (existingAccount.getBalance() == null || existingAccount.getBalance().compareTo(BigDecimal.ZERO) == 0) {
                        existingAccount.setBalance(balance);
                    }
                    return accountRepository.save(existingAccount);
                })
                .orElseGet(() -> {
                    Account newAccount = new Account();
                    newAccount.setUser(user);
                    newAccount.setAccountNumber(accountNumber);
                    newAccount.setBalance(balance);
                    return accountRepository.save(newAccount);
                });

        if (transactionRepository.findByAccountOrderByCreatedAtDesc(account).isEmpty()) {
            BankTransaction salary = new BankTransaction();
            salary.setAccount(account);
            salary.setSenderAccount(account);
            salary.setReceiverAccount(account);
            salary.setReferenceNumber(UUID.randomUUID().toString().substring(0, 12).toUpperCase());
            salary.setType(TransactionType.CREDIT);
            salary.setAmount(new BigDecimal("150000.00"));
            salary.setBalanceAfterTransaction(new BigDecimal("150000.00"));
            salary.setDescription("Monthly salary credit");
            salary.setBeneficiaryName(user.getFullName());
            salary.setBeneficiaryAccountNumber(account.getAccountNumber());
            transactionRepository.save(salary);

            BankTransaction grocery = new BankTransaction();
            grocery.setAccount(account);
            grocery.setSenderAccount(account);
            grocery.setReceiverAccount(account);
            grocery.setReferenceNumber(UUID.randomUUID().toString().substring(0, 12).toUpperCase());
            grocery.setType(TransactionType.DEBIT);
            grocery.setAmount(new BigDecimal("25000.00"));
            grocery.setBalanceAfterTransaction(balance);
            grocery.setDescription("Essentials and rent");
            grocery.setBeneficiaryName(user.getFullName());
            grocery.setBeneficiaryAccountNumber(account.getAccountNumber());
            transactionRepository.save(grocery);
        }
    }

    private void seedBeneficiary(String ownerEmail, String targetEmail, String nickname) {
        User owner = userRepository.findByEmail(ownerEmail).orElseThrow();
        Account targetAccount = accountRepository.findByUser(userRepository.findByEmail(targetEmail).orElseThrow()).orElseThrow();

        if (!beneficiaryRepository.existsByUserAndBeneficiaryAccountNumber(owner, targetAccount.getAccountNumber())) {
            Beneficiary beneficiary = new Beneficiary();
            beneficiary.setUser(owner);
            beneficiary.setNickname(nickname);
            beneficiary.setBeneficiaryName(targetAccount.getUser().getFullName());
            beneficiary.setBeneficiaryAccountNumber(targetAccount.getAccountNumber());
            beneficiary.setBankName("NovaBank");
            beneficiary.setIfscCode("NOVA0001234");
            beneficiaryRepository.save(beneficiary);
        }
    }
}
