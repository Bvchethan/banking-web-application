package com.banking.app.repository;

import com.banking.app.entity.Beneficiary;
import com.banking.app.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BeneficiaryRepository extends JpaRepository<Beneficiary, Long> {
    List<Beneficiary> findByUserOrderByCreatedAtDesc(User user);
    boolean existsByUserAndBeneficiaryAccountNumber(User user, String beneficiaryAccountNumber);
}
