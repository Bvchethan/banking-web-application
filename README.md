# Banking Web Application

Production-style full-stack digital banking application built with React, Spring Boot, JWT, Spring Security, JPA, Maven, and MySQL.

## Project Structure

```text
banking-web-application/
|-- backend/
|   |-- pom.xml
|   |-- src/main/java/com/banking/app/...
|   |-- src/main/resources/
|-- frontend/
|   |-- package.json
|   |-- src/
|-- database/
|   |-- schema.sql
|   |-- data.sql
|   |-- er-diagram.md
```

## Quick Start

### Backend

1. Create a MySQL database named `banking_app`.
2. Update database credentials in `backend/src/main/resources/application.yml`.
3. Run:

```bash
cd backend
mvn spring-boot:run
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.
Backend runs on `http://localhost:8080/api`.

## Default Demo Accounts

- Admin: `admin@bank.com` / `Admin@123`
- Customer: `john@bank.com` / `Customer@123`

Detailed setup, architecture, ER diagram, and APIs are included in the project files.
