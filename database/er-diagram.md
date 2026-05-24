# ER Diagram Structure

```mermaid
erDiagram
    USERS ||--|| ACCOUNTS : owns
    USERS ||--o{ BENEFICIARIES : manages
    USERS }o--o{ ROLES : assigned
    ACCOUNTS ||--o{ TRANSACTIONS : records
    TRANSACTIONS ||--|| FRAUD_LOGS : analyzed_by
    ROLES {
        bigint id PK
        varchar name
    }
    USERS {
        bigint id PK
        varchar full_name
        varchar email
        varchar phone
        varchar password
        varchar address
        bit active
        datetime created_at
    }
    ACCOUNTS {
        bigint id PK
        varchar account_number
        decimal balance
        varchar currency
        bit active
        datetime created_at
        bigint user_id FK
    }
    BENEFICIARIES {
        bigint id PK
        varchar nickname
        varchar beneficiary_name
        varchar beneficiary_account_number
        varchar bank_name
        varchar ifsc_code
        datetime created_at
        bigint user_id FK
    }
    TRANSACTIONS {
        bigint id PK
        varchar reference_number
        varchar type
        decimal amount
        decimal balance_after_transaction
        varchar description
        varchar beneficiary_account_number
        varchar beneficiary_name
        datetime created_at
        bigint account_id FK
    }
    FRAUD_LOGS {
        bigint id PK
        int risk_score
        varchar risk_level
        decimal evaluated_amount
        varchar reasons
        datetime analyzed_at
        bigint transaction_id FK
    }
```

## Normalization Notes

- `users`, `roles`, and `user_roles` implement a normalized many-to-many authorization model.
- `accounts` is separated from `users` to support future account product expansion.
- `beneficiaries` is independent so customers can manage reusable payees.
- `transactions` stores immutable transfer history for auditability.
- `fraud_logs` decouples AI fraud analysis from transaction storage.
