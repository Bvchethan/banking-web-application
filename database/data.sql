USE banking_app;

INSERT INTO roles (id, name) VALUES
    (1, 'ROLE_ADMIN'),
    (2, 'ROLE_CUSTOMER')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO users (id, full_name, email, phone, password, address, active, created_at) VALUES
    (1, 'System Admin', 'admin@bank.com', '9999999999', '$2a$10$QmLnZqJ8DYG8j2M7W2M7ueODRj7M0m89YI7DiIP9N6byN1Nsx3RpW', 'Head Office, Mumbai', 1, NOW()),
    (2, 'John Carter', 'john@bank.com', '8888888888', '$2a$10$L8e/zNf0z1eW3NVTm1601ew6/XQ0YJY9Vc3rroWAt4EvsC0BpvyE6', 'Bengaluru, Karnataka', 1, NOW()),
    (3, 'Jane Doe', 'jane@bank.com', '7777777777', '$2a$10$L8e/zNf0z1eW3NVTm1601ew6/XQ0YJY9Vc3rroWAt4EvsC0BpvyE6', 'Hyderabad, Telangana', 1, NOW())
ON DUPLICATE KEY UPDATE email = VALUES(email);

INSERT INTO user_roles (user_id, role_id) VALUES
    (1, 1),
    (2, 2),
    (3, 2)
ON DUPLICATE KEY UPDATE user_id = VALUES(user_id);

INSERT INTO accounts (id, account_number, balance, currency, active, created_at, user_id) VALUES
    (1, 'AC100000002', 125000.00, 'INR', 1, NOW(), 2),
    (2, 'AC100000003', 45000.00, 'INR', 1, NOW(), 3)
ON DUPLICATE KEY UPDATE balance = VALUES(balance);

INSERT INTO beneficiaries (id, nickname, beneficiary_name, beneficiary_account_number, bank_name, ifsc_code, created_at, user_id) VALUES
    (1, 'Jane', 'Jane Doe', 'AC100000003', 'NovaBank', 'NOVA0001234', NOW(), 2),
    (2, 'John', 'John Carter', 'AC100000002', 'NovaBank', 'NOVA0001234', NOW(), 3)
ON DUPLICATE KEY UPDATE nickname = VALUES(nickname);

INSERT INTO transactions (id, reference_number, type, amount, balance_after_transaction, description, beneficiary_account_number, beneficiary_name, created_at, account_id, sender_account_id, receiver_account_id) VALUES
    (1, 'SALARYCREDIT1', 'CREDIT', 150000.00, 150000.00, 'Monthly salary credit', 'AC100000002', 'John Carter', NOW() - INTERVAL 15 DAY, 1, 1, 1),
    (2, 'BILLPAYMENT01', 'DEBIT', 25000.00, 125000.00, 'Essentials and rent', 'AC100000002', 'John Carter', NOW() - INTERVAL 10 DAY, 1, 1, 1)
ON DUPLICATE KEY UPDATE description = VALUES(description);
