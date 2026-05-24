package com.banking.app.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "transactions")
public class BankTransaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Shared transfer reference. One transfer can create both a debit and a credit ledger row.
    @Column(nullable = false, length = 40)
    private String referenceNumber;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 15)
    private TransactionType type;

    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal amount;

    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal balanceAfterTransaction;

    @Column(nullable = false, length = 200)
    private String description;

    @Column(length = 20)
    private String beneficiaryAccountNumber;

    @Column(length = 80)
    private String beneficiaryName;

    @ManyToOne
    @JoinColumn(name = "sender_account_id")
    private Account senderAccount;

    @ManyToOne
    @JoinColumn(name = "receiver_account_id")
    private Account receiverAccount;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    // Ledger owner account. Each transfer creates one sender-side row and one receiver-side row.
    @ManyToOne(optional = false)
    @JoinColumn(name = "account_id", nullable = false)
    private Account account;

    @PrePersist
    public void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}
