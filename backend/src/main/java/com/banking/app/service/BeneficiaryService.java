package com.banking.app.service;

import com.banking.app.dto.BeneficiaryDto;
import com.banking.app.dto.BeneficiaryRequest;
import com.banking.app.entity.Beneficiary;
import com.banking.app.entity.User;
import com.banking.app.exception.BadRequestException;
import com.banking.app.exception.ResourceNotFoundException;
import com.banking.app.repository.BeneficiaryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class BeneficiaryService {

    private final BeneficiaryRepository beneficiaryRepository;
    private final UserService userService;

    public List<BeneficiaryDto> getBeneficiaries(String email) {
        User user = userService.getUserByEmail(email);
        return beneficiaryRepository.findByUserOrderByCreatedAtDesc(user).stream().map(this::toDto).toList();
    }

    @Transactional
    public BeneficiaryDto createBeneficiary(String email, BeneficiaryRequest request) {
        User user = userService.getUserByEmail(email);
        if (beneficiaryRepository.existsByUserAndBeneficiaryAccountNumber(user, request.getBeneficiaryAccountNumber())) {
            throw new BadRequestException("Beneficiary already exists");
        }

        Beneficiary beneficiary = new Beneficiary();
        beneficiary.setUser(user);
        mapFields(beneficiary, request);
        return toDto(beneficiaryRepository.save(beneficiary));
    }

    @Transactional
    public BeneficiaryDto updateBeneficiary(String email, Long beneficiaryId, BeneficiaryRequest request) {
        Beneficiary beneficiary = findOwnedBeneficiary(email, beneficiaryId);
        mapFields(beneficiary, request);
        return toDto(beneficiaryRepository.save(beneficiary));
    }

    @Transactional
    public void deleteBeneficiary(String email, Long beneficiaryId) {
        beneficiaryRepository.delete(findOwnedBeneficiary(email, beneficiaryId));
    }

    public Beneficiary findOwnedBeneficiary(String email, Long beneficiaryId) {
        User user = userService.getUserByEmail(email);
        Beneficiary beneficiary = beneficiaryRepository.findById(beneficiaryId)
                .orElseThrow(() -> new ResourceNotFoundException("Beneficiary not found"));
        if (!beneficiary.getUser().getId().equals(user.getId())) {
            throw new BadRequestException("Beneficiary does not belong to user");
        }
        return beneficiary;
    }

    private void mapFields(Beneficiary beneficiary, BeneficiaryRequest request) {
        beneficiary.setNickname(request.getNickname());
        beneficiary.setBeneficiaryName(request.getBeneficiaryName());
        beneficiary.setBeneficiaryAccountNumber(request.getBeneficiaryAccountNumber());
        beneficiary.setBankName(request.getBankName());
        beneficiary.setIfscCode(request.getIfscCode());
    }

    private BeneficiaryDto toDto(Beneficiary beneficiary) {
        return BeneficiaryDto.builder()
                .id(beneficiary.getId())
                .nickname(beneficiary.getNickname())
                .beneficiaryName(beneficiary.getBeneficiaryName())
                .beneficiaryAccountNumber(beneficiary.getBeneficiaryAccountNumber())
                .bankName(beneficiary.getBankName())
                .ifscCode(beneficiary.getIfscCode())
                .createdAt(beneficiary.getCreatedAt())
                .build();
    }
}
