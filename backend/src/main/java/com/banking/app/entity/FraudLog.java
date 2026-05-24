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
@Table(name = "fraud_logs")
public class FraudLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    @JoinColumn(name = "transaction_id", nullable = false, unique = true)
    private BankTransaction transaction;

    @Column(nullable = false)
    private Integer riskScore;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 10)
    private RiskLevel riskLevel;

    @Column(nullable = false, precision = 19, scale = 2)
    private BigDecimal evaluatedAmount;

    @Column(nullable = false, length = 255)
    private String reasons;

    @Column(nullable = false)
    private LocalDateTime analyzedAt;

    @PrePersist
    public void onCreate() {
        this.analyzedAt = LocalDateTime.now();
    }
}
