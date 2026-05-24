package com.banking.app.dto;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class UserProfileDto {
    private Long id;
    private String fullName;
    private String email;
    private String phone;
    private String address;
    private LocalDateTime createdAt;
    private List<String> roles;
}
