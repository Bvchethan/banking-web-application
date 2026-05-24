# Setup Instructions

## 1. Tech Stack

- Frontend: React, Tailwind CSS, Axios, React Router, Vite
- Backend: Spring Boot, Spring Security, JWT, Spring Data JPA, Maven
- Database: MySQL

## 2. Backend Structure

```text
backend/src/main/java/com/banking/app
|-- config
|-- controller
|-- dto
|-- entity
|-- exception
|-- repository
|-- security
|-- service
```

## 3. Key REST APIs

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`

### Customer

- `GET /api/customer/profile`
- `PUT /api/customer/profile`
- `GET /api/customer/account`
- `GET /api/customer/beneficiaries`
- `POST /api/customer/beneficiaries`
- `PUT /api/customer/beneficiaries/{id}`
- `DELETE /api/customer/beneficiaries/{id}`
- `GET /api/customer/transactions?search=rent`
- `POST /api/customer/transfer`
- `GET /api/customer/fraud-analytics`
- `GET /api/customer/financial-insights`

### Admin

- `GET /api/admin/dashboard`
- `GET /api/admin/customers?search=john`
- `GET /api/admin/transactions?search=salary`
- `GET /api/admin/fraud-logs`

## 4. JWT Authentication Flow

1. Customer or admin logs in through `/api/auth/login`.
2. Backend authenticates with Spring Security and BCrypt.
3. A signed JWT token is returned with embedded role claims.
4. Frontend stores the token in local storage.
5. Axios adds `Authorization: Bearer <token>` on each request.
6. `JwtAuthenticationFilter` validates the token and sets the security context.
7. Role-based routes and APIs are enforced through Spring Security.

## 5. MySQL Setup

```sql
CREATE DATABASE banking_app;
```

Then update `backend/src/main/resources/application.yml` with your MySQL username and password.

## 6. Run the Backend

```bash
cd backend
mvn clean spring-boot:run
```

Swagger UI:

- `http://localhost:8080/swagger-ui.html`

## 7. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

## 8. Demo Credentials

- Admin: `admin@bank.com` / `Admin@123`
- Customer: `john@bank.com` / `Customer@123`

## 9. Advanced Feature Logic

### AI Fraud Detection

Risk scoring rules:

- Large amount `>= 50000`
- Multiple transactions within 10 minutes
- Transfer to a newly added beneficiary

Risk levels:

- `LOW`
- `MEDIUM`
- `HIGH`

### Financial Health Score

The monthly score is calculated using:

- total credits
- total debits
- savings rate
- expense pressure against income

## 10. Suggested Next Improvements

- Add refresh tokens and logout invalidation
- Add unit and integration tests
- Add notification service for fraud alerts
- Add pagination for admin tables
