package com.banking.app.service;

import com.banking.app.dto.ProfileUpdateRequest;
import com.banking.app.dto.UserProfileDto;
import com.banking.app.entity.User;
import com.banking.app.exception.BadRequestException;
import com.banking.app.exception.ResourceNotFoundException;
import com.banking.app.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public User getUserByEmail(String email) {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    public UserProfileDto getProfile(String email) {
        User user = getUserByEmail(email);
        return mapToDto(user);
    }

    @Transactional
    public UserProfileDto updateProfile(String email, ProfileUpdateRequest request) {
        User user = getUserByEmail(email);
        userRepository.findByPhone(request.getPhone())
                .filter(existing -> !existing.getId().equals(user.getId()))
                .ifPresent(existing -> {
                    throw new BadRequestException("Phone already in use");
                });

        user.setFullName(request.getFullName());
        user.setPhone(request.getPhone());
        user.setAddress(request.getAddress());
        return mapToDto(userRepository.save(user));
    }

    private UserProfileDto mapToDto(User user) {
        return UserProfileDto.builder()
                .id(user.getId())
                .fullName(user.getFullName())
                .email(user.getEmail())
                .phone(user.getPhone())
                .address(user.getAddress())
                .createdAt(user.getCreatedAt())
                .roles(user.getRoles().stream().map(role -> role.getName().name()).toList())
                .build();
    }
}
