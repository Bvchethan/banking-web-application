package com.banking.app.service;

import com.banking.app.dto.AuthResponse;
import com.banking.app.dto.LoginRequest;
import com.banking.app.dto.RegisterRequest;
import com.banking.app.entity.Account;
import com.banking.app.entity.Role;
import com.banking.app.entity.RoleName;
import com.banking.app.entity.User;
import com.banking.app.exception.BadRequestException;
import com.banking.app.repository.AccountRepository;
import com.banking.app.repository.RoleRepository;
import com.banking.app.repository.UserRepository;
import com.banking.app.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Set;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final AccountRepository accountRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already registered");
        }
        if (userRepository.existsByPhone(request.getPhone())) {
            throw new BadRequestException("Phone already registered");
        }

        Role customerRole = roleRepository.findByName(RoleName.ROLE_CUSTOMER)
                .orElseThrow(() -> new BadRequestException("Customer role not configured"));

        User user = new User();
        user.setFullName(request.getFullName());
        user.setEmail(request.getEmail());
        user.setPhone(request.getPhone());
        user.setAddress(request.getAddress());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setRoles(Set.of(customerRole));

        User savedUser = userRepository.save(user);

        Account account = new Account();
        account.setUser(savedUser);
        account.setBalance(new BigDecimal("5000.00"));
        account.setAccountNumber("AC" + (100000000L + savedUser.getId()));
        accountRepository.save(account);

        UserDetails principal = org.springframework.security.core.userdetails.User
                .withUsername(savedUser.getEmail())
                .password(savedUser.getPassword())
                .authorities("ROLE_CUSTOMER")
                .build();

        return AuthResponse.builder()
                .token(jwtService.generateToken(principal))
                .tokenType("Bearer")
                .userId(savedUser.getId())
                .fullName(savedUser.getFullName())
                .email(savedUser.getEmail())
                .roles(List.of("ROLE_CUSTOMER"))
                .build();
    }

    public AuthResponse login(LoginRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );

        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new BadRequestException("Invalid credentials"));

        UserDetails principal = org.springframework.security.core.userdetails.User
                .withUsername(user.getEmail())
                .password(user.getPassword())
                .authorities(user.getRoles().stream().map(role -> role.getName().name()).toArray(String[]::new))
                .build();

        return AuthResponse.builder()
                .token(jwtService.generateToken(principal))
                .tokenType("Bearer")
                .userId(user.getId())
                .fullName(user.getFullName())
                .email(user.getEmail())
                .roles(user.getRoles().stream().map(role -> role.getName().name()).toList())
                .build();
    }
}
