package com.banking.app.service;

import com.banking.app.dto.FinancialInsightDto;
import com.banking.app.dto.MonthlyTrendDto;
import com.banking.app.entity.Account;
import com.banking.app.entity.BankTransaction;
import com.banking.app.entity.TransactionType;
import com.banking.app.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.YearMonth;
import java.time.format.TextStyle;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Service
@RequiredArgsConstructor
public class FinancialInsightService {

    private final AccountService accountService;
    private final TransactionRepository transactionRepository;

    public FinancialInsightDto getInsights(String email) {
        Account account = accountService.getAccountByUserEmail(email);
        List<BankTransaction> transactions = transactionRepository.findByAccountOrderByCreatedAtDesc(account);

        BigDecimal totalCredits = transactions.stream()
                .filter(tx -> tx.getType() == TransactionType.CREDIT)
                .map(BankTransaction::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal totalDebits = transactions.stream()
                .filter(tx -> tx.getType() != TransactionType.CREDIT)
                .map(BankTransaction::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        BigDecimal savingsRate = totalCredits.compareTo(BigDecimal.ZERO) > 0
                ? totalCredits.subtract(totalDebits).max(BigDecimal.ZERO)
                .divide(totalCredits, 2, RoundingMode.HALF_UP)
                .multiply(new BigDecimal("100"))
                : BigDecimal.ZERO;

        int healthScore = buildHealthScore(totalCredits, totalDebits, savingsRate);
        List<String> suggestions = buildSuggestions(savingsRate, totalDebits, totalCredits);

        return FinancialInsightDto.builder()
                .financialHealthScore(healthScore)
                .totalCredits(totalCredits)
                .totalDebits(totalDebits)
                .savingsRate(savingsRate)
                .monthlyTrends(buildMonthlyTrends(transactions))
                .smartSuggestions(suggestions)
                .build();
    }

    private int buildHealthScore(BigDecimal credits, BigDecimal debits, BigDecimal savingsRate) {
        int score = 50;
        if (credits.compareTo(BigDecimal.ZERO) > 0) {
            score += 15;
        }
        if (savingsRate.compareTo(new BigDecimal("30")) >= 0) {
            score += 25;
        } else if (savingsRate.compareTo(new BigDecimal("15")) >= 0) {
            score += 15;
        } else {
            score -= 10;
        }
        if (debits.compareTo(credits.multiply(new BigDecimal("0.85"))) > 0) {
            score -= 15;
        }
        return Math.max(0, Math.min(100, score));
    }

    private List<String> buildSuggestions(BigDecimal savingsRate, BigDecimal debits, BigDecimal credits) {
        List<String> suggestions = new ArrayList<>();
        if (savingsRate.compareTo(new BigDecimal("20")) < 0) {
            suggestions.add("Increase monthly savings by setting an automatic transfer to a savings pocket.");
        }
        if (credits.compareTo(BigDecimal.ZERO) > 0 && debits.compareTo(credits.multiply(new BigDecimal("0.80"))) > 0) {
            suggestions.add("Your spending is close to your income. Consider tightening variable expenses.");
        }
        if (suggestions.isEmpty()) {
            suggestions.add("Your finances look healthy. Maintain your current savings discipline.");
        }
        return suggestions;
    }

    private List<MonthlyTrendDto> buildMonthlyTrends(List<BankTransaction> transactions) {
        List<MonthlyTrendDto> trends = new ArrayList<>();
        for (int i = 5; i >= 0; i--) {
            YearMonth targetMonth = YearMonth.now().minusMonths(i);
            BigDecimal credit = BigDecimal.ZERO;
            BigDecimal debit = BigDecimal.ZERO;

            for (BankTransaction transaction : transactions) {
                YearMonth transactionMonth = YearMonth.from(transaction.getCreatedAt());
                if (targetMonth.equals(transactionMonth)) {
                    if (transaction.getType() == TransactionType.CREDIT) {
                        credit = credit.add(transaction.getAmount());
                    } else {
                        debit = debit.add(transaction.getAmount());
                    }
                }
            }

            trends.add(new MonthlyTrendDto(
                    targetMonth.getMonth().getDisplayName(TextStyle.SHORT, Locale.ENGLISH),
                    credit,
                    debit
            ));
        }
        return trends;
    }
}
