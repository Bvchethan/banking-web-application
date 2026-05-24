CREATE DATABASE IF NOT EXISTS banking_app;
USE banking_app;

CREATE TABLE roles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE accounts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    balance DECIMAL(19,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'INR',
    active BIT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL UNIQUE,
    CONSTRAINT fk_accounts_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE beneficiaries (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(80) NOT NULL,
    beneficiary_name VARCHAR(80) NOT NULL,
    beneficiary_account_number VARCHAR(20) NOT NULL,
    bank_name VARCHAR(20) NOT NULL,
    ifsc_code VARCHAR(15) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL,
    CONSTRAINT fk_beneficiaries_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reference_number VARCHAR(40) NOT NULL,
    type VARCHAR(15) NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    balance_after_transaction DECIMAL(19,2) NOT NULL,
    description VARCHAR(200) NOT NULL,
    beneficiary_account_number VARCHAR(20),
    beneficiary_name VARCHAR(80),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_id BIGINT NOT NULL,
    sender_account_id BIGINT NOT NULL,
    receiver_account_id BIGINT NOT NULL,
    CONSTRAINT fk_transactions_account FOREIGN KEY (account_id) REFERENCES accounts(id)
    ,
    CONSTRAINT fk_transactions_sender_account FOREIGN KEY (sender_account_id) REFERENCES accounts(id),
    CONSTRAINT fk_transactions_receiver_account FOREIGN KEY (receiver_account_id) REFERENCES accounts(id)
);

CREATE TABLE fraud_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    transaction_id BIGINT NOT NULL UNIQUE,
    risk_score INT NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    evaluated_amount DECIMAL(19,2) NOT NULL,
    reasons VARCHAR(255) NOT NULL,
    analyzed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fraud_logs_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);
