package com.banking.app.controller;

import com.banking.app.dto.AdminDashboardDto;
import com.banking.app.dto.FraudLogDto;
import com.banking.app.dto.TransactionDto;
import com.banking.app.dto.UserProfileDto;
import com.banking.app.service.AdminService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final AdminService adminService;

    @GetMapping("/dashboard")
    public ResponseEntity<AdminDashboardDto> dashboard() {
        return ResponseEntity.ok(adminService.getDashboard());
    }

    @GetMapping("/customers")
    public ResponseEntity<List<UserProfileDto>> customers(@RequestParam(required = false) String search) {
        return ResponseEntity.ok(adminService.getCustomers(search));
    }

    @GetMapping("/transactions")
    public ResponseEntity<List<TransactionDto>> transactions(@RequestParam(required = false) String search) {
        return ResponseEntity.ok(adminService.getAllTransactions(search));
    }

    @GetMapping("/fraud-logs")
    public ResponseEntity<List<FraudLogDto>> fraudLogs() {
        return ResponseEntity.ok(adminService.getAllFraudLogs());
    }
}
