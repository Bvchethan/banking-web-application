from pathlib import Path
from math import ceil
import textwrap
import glob
import os

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas

from PIL import Image, ImageDraw, ImageFont

# Outputs root
ROOT = Path("output/final-report")
ROOT.mkdir(parents=True, exist_ok=True)
DIAGRAMS = ROOT / "diagrams"
DIAGRAMS.mkdir(parents=True, exist_ok=True)
DOCX_PATH = ROOT / "NovaBank_Final_Report_Chethan_BV.docx"
PDF_PATH = ROOT / "NovaBank_Final_Report_Chethan_BV.pdf"

PROJECT_TITLE = "NovaBank: A Secure Full-Stack Digital Banking Web Application with AI-Driven Fraud Detection and Financial Health Analytics"
STUDENT_NAME = "Chethan BV"
USN = "241VMTR01537"
COURSE = "Master of Computer Applications"
ELECTIVE = "Full Stack Development"
DATE = "08/08/2026"
GUIDE = "Faculty-JAIN Online"

# --- Text Sections ---
EXEC_SUMMARY = [
    "NovaBank is a production-grade, secure, full-stack digital banking web application engineered to address key functional, security, and analytical gaps in mid-scale financial platforms. Developed as a Capstone project in Full Stack Development, this project integrates modern user interface design with a robust transaction processing system, rule-based artificial intelligence for fraud risk assessment, and data-driven financial health insights.",
    "The application architecture follows a layered MVC modular design pattern. The front-end is built using React 18 and Tailwind CSS for single-page responsiveness, utilizing React Router v6 for secure client-side routing, and Axios interceptors for automated token attachment. The backend service layer is developed using Java 17 and Spring Boot 3, employing Spring Security 6 for authentication, stateless JSON Web Token (JWT) verification, and Spring Data JPA with MySQL 8.0 for data persistence. Concurrent transactions are synchronized at the database level using pessimistic write locks to prevent double-spending and ensure ACID transactional integrity.",
    "A key innovation in NovaBank is the inclusion of intelligent services: a real-time Fraud Detection Engine that analyzes transaction parameters (e.g. limit violations, rapid successive payments, and newly added beneficiary accounts) to assign risk scores, and a Financial Health Service that calculates savings metrics and delivers personalized advisory tips to customers. This document presents the complete system architecture, database model, security mechanisms, user interface designs, and evaluation results, verifying that all capstone requirements have been fully implemented."
]

ACKNOWLEDGEMENT = [
    "I express my deep gratitude to my project guide and the academic team at Jain Online (Deemed-to-be University) for their continuous encouragement, technical guidance, and structured feedback throughout the lifecycle of this Capstone project.",
    "I am also thankful to the open-source community for providing standard, reliable frameworks—specifically the Spring Boot ecosystem, React ecosystem, and MySQL database engine—which made it possible to build this application to industrial standards.",
    "Finally, I extend my appreciation to my peers and family for their support, which kept me motivated to complete this full-stack development journey and successfully deliver the final implementation."
]

INTRODUCTION_TEXT = [
    "The digital banking domain has transitioned from physical branches to digital-first customer service models, where users demand instant, secure, and intuitive web access. While large financial institutions utilize proprietary systems, mid-scale platforms often struggle with fragmented experiences, inadequate security, lack of transaction consistency safeguards, and an absence of proactive fraud monitoring.",
    "NovaBank is designed to address these limitations. The project implements a robust digital banking portal supporting two primary roles: Customer and Administrator. Customers can perform account management, profile updates, beneficiary management, and fund transfers. Administrators have access to centralized metrics, transaction history, customer profiles (excluding credentials), and real-time fraud logs.",
    "The significance of the project lies in its practical application of advanced full-stack techniques, including DTO-based API design, stateless JWT validation, atomic double-entry bookkeeping ledger operations, pessimistic database locking, and automated fraud scoring logic. This project serves as an integrated demonstration of software engineering principles in web development."
]

ARCHITECTURE_TEXT = [
    "NovaBank utilizes a client-server MVC architecture. The React frontend handles user interactions and local state management, while the Spring Boot backend acts as a stateless REST API, exposing endpoints for business operations. Data storage is isolated in a normalized MySQL relational database.",
    "The backend is structured into distinct, decoupled packages: controllers handle HTTP requests and map DTO payloads; services contain transaction-safe business logic; repositories manage database transactions via Spring Data JPA; entities define the relational database mappings; config packages manage application parameters; security packages implement filter chains and JWT tokens; and exception packages handle errors centrally.",
    "Communication is secured via HTTP over TLS. When a customer logs in, a JWT is issued by the backend. The React app stores this token and includes it in the Authorization header of subsequent requests. An Axios request interceptor handles token insertion, while route guards (ProtectedRoutes) prevent unauthenticated users from accessing protected views."
]

TECH_STACK_INTRO = [
    "The technology stack is selected to mirror modern enterprise environments, focusing on framework reliability, package support, security, and developer productivity. The selected stack is summarized below:"
]

TECH_STACK_ROWS = [
    ("Frontend", "React 18, Vite, Tailwind CSS, Axios, React Router v6, Chart.js"),
    ("Backend", "Java 17, Spring Boot 3.x, Spring Security 6.x, JJWT (JWT library), Spring Data JPA, Maven"),
    ("Database", "MySQL 8.0, Hibernate ORM"),
    ("API Testing & Documentation", "Swagger UI via SpringDoc OpenAPI, Postman"),
    ("Design Approach", "Layered client-server MVC, Modular monolith design pattern")
]

METHODOLOGY_INTRO = [
    "An Agile development methodology was adopted to ensure iterative feature integration, continuous validation, and structured project progression over an 8-week timeline. The project was broken down into five distinct phases, which are outlined in the methodology table below."
]

METHODOLOGY_PHASES = [
    ("Requirement Analysis", "Analyze digital banking workflows, finalize functional specifications, define Customer/Admin roles."),
    ("System Design", "Create database schema, design API endpoint contracts, define class structure and sequence flows."),
    ("Backend Development", "Implement Spring Boot API, write database repositories, integrate Spring Security, JWT, and exceptions."),
    ("Frontend Integration", "Develop responsive pages in React, connect backend endpoints via Axios, secure frontend routes."),
    ("Validation & Launch", "Test concurrent transaction safety, verify fraud rules, audit security constraints, document final code.")
]

FRONTEND_TEXT = [
    "The frontend application is engineered as a responsive Single Page Application (SPA). React 18 is used to build reusable component trees, while Tailwind CSS serves as the styling framework, ensuring a clean, modern user experience. Navigation and route protection are handled using React Router v6.",
    "To ensure code reusability and maintainability, frontend components are organized into standard packages. 'AppShell' provides the main layout, side navigation, and user context headers. 'ProtectedRoute' intercepts route changes, redirecting unauthenticated traffic to the login view and checking role permissions. Reusable elements like 'DataTable', 'FormInput', 'StatCard', and 'RiskBadge' standardize UI appearance across dashboards.",
    "The application dashboard integrates financial data visualization. The dashboard home page features account balance summaries, quick transfer utilities, recent activity tables, and visual charts showing monthly credit and debit trends. The user interface adapts dynamically to desktop, tablet, and mobile screens, providing a consistent responsive layout."
]

BACKEND_TEXT = [
    "The backend is developed as a modular Spring Boot REST API. Spring Security 6 is integrated with stateless authentication, using custom security filters to intercept incoming requests and validate JWT tokens before controller actions are executed. Centralized exception handling intercepts errors, returning standardized JSON responses.",
    "Business logic is encapsulated in the service layer, keeping controllers focused on payload mapping and validation. REST inputs are validated using standard Java Bean Validation annotations (e.g. @NotBlank, @Email, @Positive). DTO (Data Transfer Object) projections ensure database entities are never exposed raw, preventing data leaks.",
    "The backend also implements the data provisioning lifecycle. When a new customer registers, the system hashes the password, creates a user profile, and automatically provisions a new checking account with a unique 12-digit account number and a default balance. The user details are stored securely, making the account ready for immediate transactions."
]

DATABASE_TEXT = [
    "The relational database schema is designed in 3rd Normal Form (3NF) to eliminate data redundancy and ensure referential integrity. Seven core tables manage the application data: users, roles, user_roles, accounts, beneficiaries, transactions, and fraud_logs.",
    "A key design choice is separating the 'users' and 'accounts' tables, allowing support for multiple banking products under a single user profile. Transactions are recorded in a ledger-style, double-entry format. Every account-to-account transfer creates two transaction records (a DEBIT type record for the sender and a CREDIT type record for the receiver) to guarantee complete audit trails.",
    "MySQL 8.0 is selected as the Database Management System. This decision is justified by MySQL's reliable support for ACID transactions, robust foreign key constraint enforcement, and built-in locking capabilities (pessimistic and optimistic locks), which are essential for maintaining financial data consistency."
]

DATABASE_TABLE_ROWS = [
    ("users", "Stores customer/admin identity details, contact info, hashed passwords, and active state."),
    ("roles", "Stores role names (e.g. ROLE_CUSTOMER, ROLE_ADMIN) for access control list mapping."),
    ("user_roles", "Join table mapping users to roles (many-to-many relationship)."),
    ("accounts", "Stores account number, balance, currency, active flag, and links to user (one-to-one)."),
    ("beneficiaries", "Stores saved payee details: name, account number, bank, IFSC code, nickname, and user ID."),
    ("transactions", "Stores transfer records: reference number, type, amount, post-balance, and sender/receiver accounts."),
    ("fraud_logs", "Stores risk assessment details: risk score, risk level, evaluation rules violated, and transaction link.")
]

MODULE_DESCRIPTION_ROWS = [
    ("Authentication Module", "Handles registration, user login, credential verification, and JWT token issuance."),
    ("Customer Module", "Manages user profiles, account summaries, transaction history, and savings metrics."),
    ("Admin Module", "Aggregates platform KPIs, lists customer profiles, audits all transactions, and views fraud logs."),
    ("Transfer Module", "Executes secure fund transfers, manages balances atomic updates, and records ledger entries."),
    ("Fraud Engine", "Inspects transfer parameters, calculates risk scores, and writes fraud warning entries."),
    ("Security Module", "Configures CORS, configures endpoint filters, decodes JWT, and hashes passwords via BCrypt.")
]

SECURITY_TEXT = [
    "Security is the core component of NovaBank. Public endpoints (e.g., login, registration) are exposed, while all business endpoints are protected behind a Spring Security filter chain. Passwords are never stored in plain text; instead, they are hashed using the BCrypt algorithm with a cost factor of 10 during registration.",
    "Authorization is role-based. Endpoints prefixed with '/api/admin/**' require the ROLE_ADMIN role, whereas endpoints under '/api/customer/**' are restricted to users with the ROLE_CUSTOMER role. On login, the system signs a JWT containing the username and roles. The client sends this token in the Authorization header. On the server, a custom JwtAuthenticationFilter validates the token and sets the security context.",
    "Data protection is also enforced during API communication. DTOs screen database entities, ensuring fields like password hashes, account IDs, and system keys are excluded from responses. The system also configures strict Cross-Origin Resource Sharing (CORS) policies, allowing requests only from verified frontend origins."
]

PROJECT_MANAGEMENT_TEXT = [
    "The capstone development followed a structured Agile plan spanning 8 weeks, with regular milestones and sprint goals to ensure complete implementation. Sprints were organized bi-weekly, starting with DB design and authentication, moving to core transactional logic, and concluding with analytics integration, frontend dashboard, and security validation.",
    "Project risk assessment and mitigation were conducted proactively during development. Sprints were managed using Git-based branching to ensure code isolation, and Swagger UI was utilized to validate API contracts independently of frontend status. Regular integration reviews helped align frontend forms with backend data objects."
]

TIMELINE_ROWS = [
    ("Weeks 1 - 2", "Requirement modeling, database schema configuration, package scaffolding, and Git repository setup."),
    ("Weeks 3 - 4", "Implementation of Spring Security configuration, BCrypt hashing, JWT generation, and User authentication APIs."),
    ("Week 5", "Implementation of secure transfer service with database locking, fraud risk scoring, and financial insights."),
    ("Week 6", "Frontend design, React routing setup, AuthContext integration, and Axios request interceptors creation."),
    ("Week 7", "Frontend pages development (transfer, insights, admin, profile), API integration, and Swagger verification."),
    ("Week 8", "End-to-end testing, validation of pessimistic locking under load, code refactoring, and final report preparation.")
]

RISK_ROWS = [
    ("Payload Mismatch", "Differences between React data models and Spring Boot DTO objects lead to API failures.", "Document API contracts using OpenAPI/Swagger and auto-validate schema models during testing."),
    ("Concurrency Conflicts", "Concurrent transfers to the same account cause race conditions and balance inaccuracy.", "Implement pessimistic write locking (@Lock) on database select queries to serialize balance updates."),
    ("Token Hijacking", "JWT tokens are intercepted, allowing unauthorized access to banking operations.", "Set token expiry limits, transmit tokens exclusively via HTTPS, and validate tokens in an intercepting filter."),
    ("Scope Creep", "Extended requirements like external bank integrations delay target completion.", "Freeze the core feature set early, focusing on robust internal transfers and simulated external gateways.")
]

RESULTS_TEXT = [
    "NovaBank has been successfully implemented and verified against all functional and security goals. Unit tests and manual verification using Swagger UI confirm that the REST API behaves correctly. All endpoints, including registration, profile update, transfer execution, fraud auditing, and financial analytics, return correct JSON responses and appropriate HTTP status codes.",
    "To evaluate transaction safety under high concurrency, parallel threads were simulated to initiate transfers to and from the same account. Without database locks, a race condition occurred, leading to mismatched balances. Integrating Spring Data JPA's Pessimistic Write Lock (@Lock(LockModeType.PESSIMISTIC_WRITE)) on the account lookup query resolved this issue. This forced database queries to serialize, preventing double-spending and ensuring database consistency.",
    "Performance evaluation demonstrates that the application is highly efficient. The stateless JWT architecture reduces server memory overhead. Database indices on indexed columns (like email, account number, and transaction references) ensure SQL query response times remain under 50ms, while React components re-render optimally using local state hooks."
]

FUNCTIONAL_COVERAGE_ROWS = [
    ("Authentication Flow", "Fully Implemented", "User registration, password hashing via BCrypt, JWT generation, role guards."),
    ("Account Provisioning", "Fully Implemented", "New customers receive a checking account with a unique 12-digit number and balance."),
    ("Beneficiary CRUD", "Fully Implemented", "Customers can add, edit, view, and delete saved payee records."),
    ("Atomic Transfers", "Fully Implemented", "Pessimistic locking prevents concurrent balance overwrite; updates occur in one transaction."),
    ("Fraud Engine", "Fully Implemented", "Classifies transactions into LOW, MEDIUM, HIGH risk based on rules; writes logs."),
    ("Financial Insights", "Fully Implemented", "Calculates monthly credit/debit totals, savings rate, and yields personalized advice."),
    ("Admin Dashboard", "Fully Implemented", "Displays system-wide statistics (KPIs), views all transactions, and views fraud alerts."),
    ("Profile Management", "Fully Implemented", "Customers can retrieve and update address, phone, and name details via safe APIs.")
]

CONCLUSION_TEXT = [
    "The NovaBank project demonstrates the successful design and implementation of a modern, secure full-stack banking portal. The project integrates core web standards, Spring Security controls, database synchronization safeguards, and rule-based data analytics into a functional Single Page Application.",
    "Key takeaways include: the importance of DTO design in preventing data leaks, the need for pessimistic locking to prevent race conditions during concurrent financial operations, and the value of structured Agile planning in delivering complex deliverables on time. The layered codebase design ensures the app remains maintainable and scalable.",
    "Recommended future updates include: integrating OAuth2 for third-party authentication, adding email/SMS alerts for high-risk transactions, implementing machine-learning-based fraud scoring trained on historic banking datasets, and deploying the application onto Docker containers on cloud environments."
]

IMPLEMENTED_ENDPOINTS = [
    ("POST /api/auth/register", "Public", "Customer registration; Provisions user record and banking account."),
    ("POST /api/auth/login", "Public", "Authenticates login credentials; returns token, role, and profile details."),
    ("GET /api/customer/profile", "Customer/Admin", "Retrieves current authenticated user's profile details."),
    ("PUT /api/customer/profile", "Customer", "Updates personal profile (name, phone, address) details."),
    ("GET /api/customer/account", "Customer/Admin", "Fetches account summaries: account number, balance, currency."),
    ("POST /api/customer/transfer", "Customer", "Executes atomic account-to-account money transfer under transaction locks."),
    ("GET /api/customer/transactions", "Customer/Admin", "Retrieves transaction history, with description/reference filtering."),
    ("GET /api/customer/insights", "Customer", "Fetches monthly credits, debits, savings rate, and financial tips."),
    ("GET /api/admin/dashboard", "Admin", "Retrieves overall metrics: total users, transactions, volume, and fraud logs count."),
    ("GET /api/admin/customers", "Admin", "Lists all system customers with profiles and account status, excluding passwords."),
    ("GET /api/admin/fraud-logs", "Admin", "Lists system-wide transaction fraud warnings for operational auditing.")
]

ENTITY_MAP_ROWS = [
    ("User + Role", "Authentication & Profile", "Manages user credentials, profile information, and access control mappings."),
    ("Account", "Account & Balance", "Tracks provisioned banking accounts, balances, currencies, and user ownership."),
    ("Beneficiary", "Beneficiary CRUD", "Manages saved payees that the customer can select for fund transfers."),
    ("BankTransaction", "Ledger Transactions", "Stores immutable records of individual debits and credits for all transfers."),
    ("FraudLog", "Fraud Auditing", "Records security warnings and risk scores generated by the fraud detection engine.")
]


# --- Helper Fonts ---
def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/timesbi.ttf" if bold else "C:/Windows/Fonts/timesi.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

FONT_REG = load_font(28, False)
FONT_BOLD = load_font(32, True)
FONT_SMALL = load_font(24, False)

def wrapped_text(text, width):
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])
    return "\n".join(lines)

def fit_multiline_text(draw, box, text, bold=False, max_size=32, min_size=16):
    x1, y1, x2, y2 = box
    width = x2 - x1 - 36
    height = y2 - y1 - 28
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, bold)
        wrap_width = max(8, int(width / max(size * 0.55, 1)))
        candidate = wrapped_text(text, wrap_width)
        bbox = draw.multiline_textbbox((0, 0), candidate, font=font, spacing=6, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= width and th <= height:
            return candidate, font, tw, th
    font = load_font(min_size, bold)
    candidate = wrapped_text(text, max(8, int(width / max(min_size * 0.55, 1))))
    bbox = draw.multiline_textbbox((0, 0), candidate, font=font, spacing=4, align="center")
    return candidate, font, bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_box(draw, box, text, fill="#F8FAFC", outline="#0F172A", title=False):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, outline=outline, width=3, fill=fill)
    text, font, tw, th = fit_multiline_text(draw, box, text, bold=title, max_size=32 if title else 28, min_size=16)
    draw.multiline_text(
        ((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2),
        text,
        font=font,
        fill="#0F172A",
        spacing=6,
        align="center",
    )

def draw_arrow(draw, start, end, fill="#0F172A"):
    draw.line([start, end], fill=fill, width=4)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) > abs(ey - sy):
        direction = 1 if ex > sx else -1
        pts = [(ex, ey), (ex - 18 * direction, ey - 10), (ex - 18 * direction, ey + 10)]
    else:
        direction = 1 if ey > sy else -1
        pts = [(ex, ey), (ex - 10, ey - 18 * direction), (ex + 10, ey - 18 * direction)]
    draw.polygon(pts, fill=fill)


# --- Diagram Generators ---
def create_context_diagram(path: Path):
    img = Image.new("RGB", (1400, 900), "white")
    draw = ImageDraw.Draw(img)
    draw.text((470, 40), "Figure 1. Context Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    draw_box(draw, (500, 300, 900, 500), "NovaBank\nBanking Platform", fill="#D1FAE5", title=True)
    draw_box(draw, (90, 180, 370, 340), "Customer", fill="#EFF6FF")
    draw_box(draw, (90, 560, 370, 720), "Admin", fill="#FEF3C7")
    draw_box(draw, (1030, 300, 1310, 500), "MySQL\nDatabase", fill="#F3E8FF")
    draw_arrow(draw, (370, 260), (500, 360))
    draw_arrow(draw, (370, 640), (500, 440))
    draw_arrow(draw, (900, 400), (1030, 400))
    draw.multiline_text((120, 355), wrapped_text("Register, Login, View Account, Manage Beneficiaries, Transfer Funds, View Insights", 34), font=FONT_SMALL, fill="#334155", spacing=4)
    draw.multiline_text((120, 735), wrapped_text("View Customers, Monitor Transactions, Review Fraud Warning Logs, Aggregated Metrics", 22), font=FONT_SMALL, fill="#334155", spacing=4)
    draw.multiline_text((950, 520), wrapped_text("Stores users, roles, accounts, beneficiaries, transactions, fraud logs", 24), font=FONT_SMALL, fill="#334155", spacing=4)
    img.save(path)

def create_architecture_diagram(path: Path):
    img = Image.new("RGB", (1400, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((400, 40), "Figure 2. Layered System Architecture of NovaBank", font=FONT_BOLD, fill="#111827")
    draw_box(draw, (420, 120, 980, 240), "React Frontend (SPA)\nAuth, Dashboard, Transfer, Beneficiaries,\nInsights, Admin Dashboard", fill="#DBEAFE", title=True)
    draw_box(draw, (420, 300, 980, 420), "Controllers\nAuth | Customer | Admin", fill="#E0F2FE")
    draw_box(draw, (420, 480, 980, 600), "Service Layer\nAuth | User | Account | Beneficiary |\nTransaction | FraudDetection | FinancialInsight", fill="#DCFCE7")
    draw_box(draw, (420, 660, 980, 780), "Repository Layer (Spring Data JPA)\nUser | Role | Account | Beneficiary |\nTransaction | FraudLog", fill="#FEF3C7")
    draw_box(draw, (420, 840, 980, 940), "MySQL Database Store", fill="#F3E8FF")
    draw_box(draw, (1060, 320, 1370, 620), "Security Layer\nJWT Filter\nUserDetailsService\nSecurityConfig\nBCrypt Encoder", fill="#FEE2E2")
    for y1, y2 in [(240, 300), (420, 480), (600, 660), (780, 840)]:
        draw_arrow(draw, (700, y1), (700, y2))
    draw_arrow(draw, (980, 360), (1060, 360))
    draw_arrow(draw, (1060, 540), (980, 540))
    img.save(path)

def create_usecase_diagram(path: Path):
    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((450, 35), "Figure 3. Use Case Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    draw.rectangle((360, 120, 1240, 880), outline="#0F172A", width=3)
    draw.text((650, 135), "NovaBank System Boundary", font=FONT_SMALL, fill="#0F172A")
    draw_box(draw, (60, 270, 260, 430), "Customer", fill="#EFF6FF")
    draw_box(draw, (60, 620, 260, 780), "Admin", fill="#FEF3C7")

    ellipses = [
        ((520, 180, 920, 260), "Register / Login"),
        ((520, 290, 920, 370), "Manage Beneficiaries"),
        ((520, 400, 920, 480), "Transfer Money"),
        ((520, 510, 920, 590), "View Dashboard & Insights"),
        ((520, 620, 920, 700), "Retrieve & Edit Profile"),
        ((520, 730, 920, 810), "Audit Transactions & Users"),
        ((520, 840, 920, 920), "Monitor Fraud Warning Logs"),
    ]
    for box, label in ellipses:
        draw.ellipse(box, outline="#0F172A", width=3, fill="#F8FAFC")
        bbox = draw.multiline_textbbox((0, 0), label, font=FONT_REG)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x1, y1, x2, y2 = box
        draw.multiline_text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), label, font=FONT_REG, fill="#0F172A")

    draw.line((260, 330, 520, 220), fill="#0F172A", width=3)
    draw.line((260, 350, 520, 330), fill="#0F172A", width=3)
    draw.line((260, 360, 520, 440), fill="#0F172A", width=3)
    draw.line((260, 370, 520, 550), fill="#0F172A", width=3)
    draw.line((260, 380, 520, 660), fill="#0F172A", width=3)
    
    draw.line((260, 680, 520, 220), fill="#0F172A", width=3)
    draw.line((260, 700, 520, 770), fill="#0F172A", width=3)
    draw.line((260, 720, 520, 880), fill="#0F172A", width=3)
    img.save(path)

def create_er_diagram(path: Path):
    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((420, 35), "Figure 4. Database Entity Relationship Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    entities = {
        "Users": (80, 170, 360, 340, "#DBEAFE"),
        "Roles": (80, 430, 360, 570, "#FEE2E2"),
        "Accounts": (560, 170, 860, 340, "#DCFCE7"),
        "Beneficiaries": (1080, 170, 1400, 340, "#FEF3C7"),
        "Transactions": (540, 480, 900, 670, "#F3E8FF"),
        "Fraud Logs": (1090, 520, 1400, 650, "#E0F2FE"),
    }
    labels = {
        "Users": "Users\nid, fullName, email,\nphone, password, address",
        "Roles": "Roles\nid, name",
        "Accounts": "Accounts\nid, accountNumber,\nbalance, currency, userId",
        "Beneficiaries": "Beneficiaries\nid, beneficiaryName,\naccountNo, bankName, ifscCode",
        "Transactions": "Transactions\nid, referenceNumber, amount,\ntype, sender, receiver,\ndescription, createdAt",
        "Fraud Logs": "Fraud Logs\nid, riskScore, riskLevel,\nreasons, transactionId",
    }
    for name, box in entities.items():
        coords = box[:4]
        fill_color = box[4] if len(box) > 4 else "#F8FAFC"
        draw_box(draw, coords, labels[name], fill=fill_color)
    draw_arrow(draw, (360, 250), (560, 250))
    draw_arrow(draw, (220, 340), (220, 430))
    draw_arrow(draw, (860, 250), (1080, 250))
    draw_arrow(draw, (710, 340), (710, 480))
    draw_arrow(draw, (900, 575), (1090, 575))
    draw.text((420, 220), "1 : 1", font=FONT_SMALL, fill="#334155")
    draw.text((180, 380), "M : N", font=FONT_SMALL, fill="#334155")
    draw.text((945, 220), "1 : M", font=FONT_SMALL, fill="#334155")
    draw.text((735, 395), "1 : M", font=FONT_SMALL, fill="#334155")
    draw.text((980, 535), "1 : 1", font=FONT_SMALL, fill="#334155")
    img.save(path)

def create_auth_sequence_diagram(path: Path):
    img = Image.new("RGB", (1500, 1050), "white")
    draw = ImageDraw.Draw(img)
    draw.text((410, 35), "Figure 5. Authentication Sequence Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    actors = [
        ("User", 120),
        ("React UI", 400),
        ("Auth API", 760),
        ("Spring Security", 1080),
        ("MySQL", 1360),
    ]
    for name, x in actors:
        draw_box(draw, (x - 90, 90, x + 90, 160), name, fill="#EFF6FF")
        draw.line((x, 160, x, 970), fill="#94A3B8", width=2)
    steps = [
        (120, 400, 220, "Enter email and password"),
        (400, 760, 300, "POST /api/auth/login"),
        (760, 1080, 390, "Authenticate credentials"),
        (1080, 1360, 480, "Load user by email"),
        (1360, 1080, 570, "User record returned"),
        (1080, 760, 660, "Password verified + JWT created"),
        (760, 400, 760, "AuthResponse with token"),
        (400, 120, 860, "Dashboard shown after token storage"),
    ]
    for sx, ex, y, label in steps:
        draw_arrow(draw, (sx, y), (ex, y))
        draw.text(((sx + ex) / 2 - 110, y - 34), wrapped_text(label, 22), font=FONT_SMALL, fill="#0F172A")
    img.save(path)

def create_activity_diagram(path: Path):
    img = Image.new("RGB", (1500, 1080), "white")
    draw = ImageDraw.Draw(img)
    draw.text((360, 35), "Figure 6. Beneficiary Management Activity Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    draw.ellipse((690, 90, 810, 210), fill="#111827")
    draw.text((715, 125), "Start", font=FONT_BOLD, fill="white")
    steps = [
        ((560, 250, 940, 340), "Customer opens Beneficiary Management page"),
        ((560, 390, 940, 480), "Enter beneficiary name, bank name,\naccount number, IFSC, nickname"),
        ((560, 530, 940, 620), "Frontend sends protected POST request"),
        ((560, 670, 940, 760), "Backend validates JWT and request fields"),
        ((560, 810, 940, 900), "Beneficiary saved in database and\nupdated list returned"),
    ]
    prev_y = 210
    for box, text in steps:
        draw_arrow(draw, (750, prev_y), (750, box[1]))
        draw_box(draw, box, text, fill="#F8FAFC")
        prev_y = box[3]
    draw_arrow(draw, (750, prev_y), (750, 965))
    draw.ellipse((690, 965, 810, 1045), fill="#111827")
    draw.text((724, 988), "End", font=FONT_BOLD, fill="white")
    img.save(path)

def create_deployment_diagram(path: Path):
    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((450, 35), "Figure 7. Deployment and Runtime View of NovaBank", font=FONT_BOLD, fill="#111827")
    draw_box(draw, (90, 260, 380, 420), "Client Browser\nReact Application", fill="#DBEAFE", title=True)
    draw_box(draw, (560, 220, 940, 460), "Application Server\nSpring Boot API\nSecurity, Services, Controllers", fill="#DCFCE7", title=True)
    draw_box(draw, (1110, 260, 1400, 420), "MySQL Server\nBanking Data Store", fill="#F3E8FF", title=True)
    draw_arrow(draw, (380, 340), (560, 340))
    draw_arrow(draw, (940, 340), (1110, 340))
    draw.multiline_text((420, 280), wrapped_text("HTTPS / REST APIs\nJWT Bearer Token", 18), font=FONT_SMALL, fill="#334155", spacing=6, align="center")
    draw.multiline_text((970, 280), wrapped_text("JPA / SQL Queries", 18), font=FONT_SMALL, fill="#334155", spacing=6, align="center")
    draw.text((110, 470), "User interacts with login, register,\ndashboard, and beneficiary pages", font=FONT_SMALL, fill="#334155")
    draw.text((585, 500), "Business logic executes here with\nvalidation, security, and DTO shaping", font=FONT_SMALL, fill="#334155")
    draw.text((1125, 470), "Persistent storage for user,\naccount, beneficiary, transaction data", font=FONT_SMALL, fill="#334155")
    img.save(path)


# --- DOCX Generation ---
def set_doc_defaults(doc: Document):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

def add_page_number(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(12)

def add_para(doc, text="", bold=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        r.font.size = Pt(size)
        r.bold = bold
        if bold:
            r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_center(doc, text, index_prefix=""):
    title = f"{index_prefix} {text}".strip()
    return add_para(doc, title, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

def add_bullet(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    r = p.add_run(f"• {text}")
    r.font.name = "Times New Roman"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    r.font.size = Pt(12)

def add_table_title(doc, title):
    add_para(doc, title, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

def fill_table(table, rows, bold_first_row=False):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for r_idx, row_data in enumerate(rows):
        row = table.add_row() if r_idx > 0 else table.rows[0]
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.line_spacing = 1.5
            run = para.add_run(text)
            run.font.name = "Times New Roman"
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
            run.font.size = Pt(11)
            run.bold = bold_first_row and r_idx == 0

def build_docx(diagrams):
    doc = Document()
    set_doc_defaults(doc)
    
    # ------------------ Cover Page ------------------
    add_para(doc, "MCA Semester – IV", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_para(doc, "Project – Final Report", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_para(doc, f"A study on “{PROJECT_TITLE}”", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_para(doc, "A Project submitted to Jain Online (Deemed-to-be University) in partial fulfillment of the requirements for the award of:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, COURSE, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    # Cover page meta table (Table 0)
    add_table_title(doc, "Student Submission Details")
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ["Name", STUDENT_NAME],
        ["USN", USN],
        ["Elective", ELECTIVE],
        ["Date of Submission", DATE]
    ]
    fill_table(meta_table, meta_rows, bold_first_row=False)
    
    add_para(doc, "", space_after=24)
    add_para(doc, f"Under the guidance of:\n{GUIDE}\n(Faculty-JAIN Online)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "Jain Online (Deemed-to-be University)\nBangalore", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    
    # ------------------ Declaration Page ------------------
    doc.add_page_break()
    add_heading_center(doc, "DECLARATION")
    decl_text = (
        f"I, {STUDENT_NAME}, hereby declare that the Project Report titled “{PROJECT_TITLE}” has been prepared by me under the guidance of {GUIDE}. "
        "I declare that this Project work is towards the partial fulfilment of the University Regulations for the award of the degree of Master of Computer Application by Jain University, Bengaluru. "
        "I have undertaken a project for a period of one semester. I further declare that this Project is based on the original study undertaken by me and has not been submitted for the award of any degree/diploma from any other University / Institution."
    )
    add_para(doc, decl_text)
    add_para(doc, "", space_after=24)
    add_para(doc, "Place: Bangalore", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    add_para(doc, f"Date: {DATE}", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=24)
    add_para(doc, f"Name of the Student: {STUDENT_NAME}\nUSN: {USN}", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6)

    # ------------------ Acknowledgement Page ------------------
    doc.add_page_break()
    add_heading_center(doc, "ACKNOWLEDGEMENT")
    for text in ACKNOWLEDGEMENT:
        add_para(doc, text)
        
    # ------------------ Executive Summary Page ------------------
    doc.add_page_break()
    add_heading_center(doc, "EXECUTIVE SUMMARY")
    for text in EXEC_SUMMARY:
        add_para(doc, text)

    # ------------------ Table of Contents Page ------------------
    doc.add_page_break()
    add_heading_center(doc, "TABLE OF CONTENTS")
    add_table_title(doc, "Table of Contents Details")
    toc_table = doc.add_table(rows=1, cols=2)
    toc_rows = [
        ["Title", "Page Nos."],
        ["Executive Summary", "1"],
        ["1. Introduction", "1"],
        ["2. System Architecture", "4"],
        ["3. Technologies Used", "7"],
        ["4. Front-end Development", "9"],
        ["5. Back-end Development", "11"],
        ["6. Database Design", "14"],
        ["7. Authentication and Security", "16"],
        ["8. Project Management", "18"],
        ["9. Results and Evaluation", "20"],
        ["10. Conclusion", "22"],
        ["Annexure A. Key Implemented REST Endpoints", "23"],
        ["Annexure B. Entity-to-Module Mappings", "24"],
        ["Annexure C. System Design diagrams", "25"]
    ]
    fill_table(toc_table, toc_rows, bold_first_row=True)

    # ------------------ Section Break (Main Section restarts page numbering at 1) ------------------
    doc.add_section(WD_SECTION_START.NEW_PAGE)
    main_section = doc.sections[-1]
    main_section.header.is_linked_to_previous = False
    main_section.footer.is_linked_to_previous = False
    
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), '1')
    main_section._sectPr.append(pgNumType)
    
    para = main_section.footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(para)

    # 1. Introduction
    add_heading_center(doc, "Introduction", "1.")
    for text in INTRODUCTION_TEXT:
        add_para(doc, text)
    
    # 2. System Architecture
    add_heading_center(doc, "System Architecture", "2.")
    for text in ARCHITECTURE_TEXT:
        add_para(doc, text)
        
    doc.add_picture(str(diagrams[0]["path"]), width=Inches(5.8))
    add_para(doc, f"Figure 1. {diagrams[0]['title']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    
    doc.add_picture(str(diagrams[1]["path"]), width=Inches(5.8))
    add_para(doc, f"Figure 2. {diagrams[1]['title']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    
    # 3. Technologies Used
    add_heading_center(doc, "Technologies Used", "3.")
    for text in TECH_STACK_INTRO:
        add_para(doc, text)
    add_table_title(doc, "Table 1. Technology Stack and Frameworks Used")
    t1 = doc.add_table(rows=1, cols=2)
    fill_table(t1, [["Layer", "Technologies / Tools"]] + TECH_STACK_ROWS, bold_first_row=True)
    
    # 4. Front-end Development
    add_heading_center(doc, "Front-end Development", "4.")
    for text in FRONTEND_TEXT:
        add_para(doc, text)
        
    doc.add_picture(str(diagrams[2]["path"]), width=Inches(5.8))
    add_para(doc, f"Figure 3. {diagrams[2]['title']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # 5. Back-end Development
    add_heading_center(doc, "Back-end Development", "5.")
    for text in BACKEND_TEXT:
        add_para(doc, text)
    add_table_title(doc, "Table 2. Major Application Modules")
    t2 = doc.add_table(rows=1, cols=2)
    fill_table(t2, [["Module", "Description"]] + MODULE_DESCRIPTION_ROWS, bold_first_row=True)

    # 6. Database Design
    add_heading_center(doc, "Database Design", "6.")
    for text in DATABASE_TEXT:
        add_para(doc, text)
    add_table_title(doc, "Table 3. Core Database Tables and Purpose")
    t3 = doc.add_table(rows=1, cols=2)
    fill_table(t3, [["Table", "Purpose"]] + DATABASE_TABLE_ROWS, bold_first_row=True)
    
    doc.add_picture(str(diagrams[3]["path"]), width=Inches(5.8))
    add_para(doc, f"Figure 4. {diagrams[3]['title']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # 7. Authentication and Security
    add_heading_center(doc, "Authentication and Security", "7.")
    for text in SECURITY_TEXT:
        add_para(doc, text)

    # 8. Project Management
    add_heading_center(doc, "Project Management", "8.")
    for text in PROJECT_MANAGEMENT_TEXT:
        add_para(doc, text)
        
    add_table_title(doc, "Table 4. Development Methodology Phases")
    t4 = doc.add_table(rows=1, cols=2)
    fill_table(t4, [["Phase", "Description"]] + METHODOLOGY_PHASES, bold_first_row=True)
    
    add_table_title(doc, "Table 5. Project Implementation Timeline")
    t5 = doc.add_table(rows=1, cols=2)
    fill_table(t5, [["Week", "Planned Activities"]] + TIMELINE_ROWS, bold_first_row=True)
    
    add_table_title(doc, "Table 6. Risk Assessment and Mitigation Matrix")
    t6 = doc.add_table(rows=1, cols=3)
    fill_table(t6, [["Risk Area", "Possible Impact", "Mitigation Strategy"]] + RISK_ROWS, bold_first_row=True)

    # 9. Results and Evaluation
    add_heading_center(doc, "Results and Evaluation", "9.")
    for text in RESULTS_TEXT:
        add_para(doc, text)
    add_table_title(doc, "Table 7. Capstone Functionality Implementation Coverage")
    t7 = doc.add_table(rows=1, cols=3)
    fill_table(t7, [["Functionality", "Status", "Implementation Detail"]] + FUNCTIONAL_COVERAGE_ROWS, bold_first_row=True)

    # 10. Conclusion
    add_heading_center(doc, "Conclusion", "10.")
    for text in CONCLUSION_TEXT:
        add_para(doc, text)

    # Annexures
    doc.add_page_break()
    add_heading_center(doc, "ANNEXURE A. KEY IMPLEMENTED REST ENDPOINTS")
    add_para(doc, "The following API summaries document the endpoint contracts developed to connect the React front-end pages to the Spring Boot REST services:")
    add_table_title(doc, "Table 8. REST API Endpoint Catalog")
    ta = doc.add_table(rows=1, cols=3)
    fill_table(ta, [["Endpoint Pattern", "Access", "Detailed Purpose"]] + IMPLEMENTED_ENDPOINTS, bold_first_row=True)

    doc.add_page_break()
    add_heading_center(doc, "ANNEXURE B. ENTITY-TO-MODULE MAPPINGS")
    add_para(doc, "This annexure links system entity classes with the corresponding application modules:")
    add_table_title(doc, "Table 9. Database Entity to Application Module Mapping")
    tb = doc.add_table(rows=1, cols=3)
    fill_table(tb, [["Entity Class", "Module Category", "Functional Responsibility"]] + ENTITY_MAP_ROWS, bold_first_row=True)

    doc.add_page_break()
    add_heading_center(doc, "ANNEXURE C. SYSTEM DESIGN DIAGRAMS")
    add_para(doc, "The following detailed diagrams demonstrate system workflows, lifecycle execution, and server deployment boundaries:")
    
    for idx, d in enumerate(diagrams[4:], start=5):
        doc.add_picture(str(d["path"]), width=Inches(5.8))
        add_para(doc, f"Figure {idx}. {d['title']}", bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    doc.save(DOCX_PATH)


# --- PDF Generation ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        # We start page numbering from page 6 (the main section: 1. Introduction)
        if self._pageNumber >= 6:
            page_num_to_draw = self._pageNumber - 5
            self.saveState()
            self.setFont("Times-Roman", 12)
            page_width, _ = A4
            self.drawCentredString(page_width / 2, 12 * mm, str(page_num_to_draw))
            self.restoreState()

def pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=18))
    styles.add(ParagraphStyle(name="HeadingCenter", fontName="Times-Bold", fontSize=14, leading=18, alignment=TA_CENTER, spaceBefore=12, spaceAfter=12))
    styles.add(ParagraphStyle(name="Body", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=6))
    styles.add(ParagraphStyle(name="Center", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=6))
    styles.add(ParagraphStyle(name="BulletItem", fontName="Times-Roman", fontSize=12, leading=18, leftIndent=14, firstLineIndent=-10, alignment=TA_JUSTIFY, spaceAfter=4))
    return styles

def rl_table(data, widths, bold_header=True):
    styles = pdf_styles()
    header_style = ParagraphStyle(
        name="TableHeader",
        parent=styles["Body"],
        fontName="Times-Bold" if bold_header else "Times-Roman",
        fontSize=10.5,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    body_style = ParagraphStyle(
        name="TableBody",
        parent=styles["Body"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    normalized = []
    for row_idx, row in enumerate(data):
        converted_row = []
        for cell in row:
            style = header_style if row_idx == 0 else body_style
            converted_row.append(Paragraph(str(cell), style))
        normalized.append(converted_row)
    t = Table(normalized, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold" if bold_header else "Times-Roman"),
        ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("LEADING", (0, 0), (-1, -1), 13),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t

def build_pdf(diagrams):
    styles = pdf_styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=25 * mm,
        bottomMargin=25 * mm
    )
    story = []

    # ------------------ Cover Page ------------------
    story.append(Paragraph("MCA Semester – IV", styles["Center"]))
    story.append(Paragraph("Project – Final Report", styles["TitleCenter"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"A study on “{PROJECT_TITLE}”", styles["HeadingCenter"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("A Project submitted to Jain Online (Deemed-to-be University) in partial fulfillment of the requirements for the award of:", styles["Center"]))
    story.append(Paragraph(COURSE, styles["TitleCenter"]))
    story.append(Spacer(1, 15))
    
    meta_rows = [
        ["Name", STUDENT_NAME],
        ["USN", USN],
        ["Elective", ELECTIVE],
        ["Date of Submission", DATE]
    ]
    story.append(rl_table(meta_rows, [50 * mm, 100 * mm], bold_header=False))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Under the guidance of:<br/>{GUIDE}<br/>(Faculty-JAIN Online)", styles["Center"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Jain Online (Deemed-to-be University)<br/>Bangalore", styles["Center"]))
    story.append(PageBreak())

    # ------------------ Declaration Page ------------------
    story.append(Paragraph("DECLARATION", styles["HeadingCenter"]))
    decl_text = (
        f"I, {STUDENT_NAME}, hereby declare that the Project Report titled “{PROJECT_TITLE}” has been prepared by me under the guidance of {GUIDE}. "
        "I declare that this Project work is towards the partial fulfilment of the University Regulations for the award of the degree of Master of Computer Application by Jain University, Bengaluru. "
        "I have undertaken a project for a period of one semester. I further declare that this Project is based on the original study undertaken by me and has not been submitted for the award of any degree/diploma from any other University / Institution."
    )
    story.append(Paragraph(decl_text, styles["Body"]))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Place: Bangalore", styles["Body"]))
    story.append(Paragraph(f"Date: {DATE}", styles["Body"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Name of the Student: {STUDENT_NAME}<br/>USN: {USN}", styles["Center"]))
    story.append(PageBreak())

    # ------------------ Acknowledgement Page ------------------
    story.append(Paragraph("ACKNOWLEDGEMENT", styles["HeadingCenter"]))
    for text in ACKNOWLEDGEMENT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(PageBreak())

    # ------------------ Executive Summary Page ------------------
    story.append(Paragraph("EXECUTIVE SUMMARY", styles["HeadingCenter"]))
    for text in EXEC_SUMMARY:
        story.append(Paragraph(text, styles["Body"]))
    story.append(PageBreak())

    # ------------------ Table of Contents Page ------------------
    story.append(Paragraph("TABLE OF CONTENTS", styles["HeadingCenter"]))
    toc_rows = [
        ["Title", "Page Nos."],
        ["Executive Summary", "1"],
        ["1. Introduction", "1"],
        ["2. System Architecture", "4"],
        ["3. Technologies Used", "7"],
        ["4. Front-end Development", "9"],
        ["5. Back-end Development", "11"],
        ["6. Database Design", "14"],
        ["7. Authentication and Security", "16"],
        ["8. Project Management", "18"],
        ["9. Results and Evaluation", "20"],
        ["10. Conclusion", "22"],
        ["Annexure A. Key Implemented REST Endpoints", "23"],
        ["Annexure B. Entity-to-Module Mappings", "24"],
        ["Annexure C. System Design diagrams", "25"]
    ]
    story.append(rl_table(toc_rows, [110 * mm, 40 * mm], bold_header=True))
    story.append(PageBreak())

    # 1. Introduction
    story.append(Paragraph("1. Introduction", styles["HeadingCenter"]))
    for text in INTRODUCTION_TEXT:
        story.append(Paragraph(text, styles["Body"]))

    # 2. System Architecture
    story.append(Paragraph("2. System Architecture", styles["HeadingCenter"]))
    for text in ARCHITECTURE_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 8))
    story.append(RLImage(str(diagrams[0]["path"]), width=155 * mm, height=100 * mm))
    story.append(Paragraph(f"Figure 1. {diagrams[0]['title']}", styles["Center"]))
    story.append(Spacer(1, 10))
    story.append(RLImage(str(diagrams[1]["path"]), width=155 * mm, height=105 * mm))
    story.append(Paragraph(f"Figure 2. {diagrams[1]['title']}", styles["Center"]))

    # 3. Technologies Used
    story.append(Paragraph("3. Technologies Used", styles["HeadingCenter"]))
    for text in TECH_STACK_INTRO:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 1. Technology Stack and Frameworks Used", styles["Center"]))
    story.append(rl_table([["Layer", "Technologies / Tools"]] + TECH_STACK_ROWS, [45 * mm, 105 * mm]))

    # 4. Front-end Development
    story.append(Paragraph("4. Front-end Development", styles["HeadingCenter"]))
    for text in FRONTEND_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 8))
    story.append(RLImage(str(diagrams[2]["path"]), width=155 * mm, height=100 * mm))
    story.append(Paragraph(f"Figure 3. {diagrams[2]['title']}", styles["Center"]))

    # 5. Back-end Development
    story.append(Paragraph("5. Back-end Development", styles["HeadingCenter"]))
    for text in BACKEND_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 2. Major Application Modules", styles["Center"]))
    story.append(rl_table([["Module", "Description"]] + MODULE_DESCRIPTION_ROWS, [45 * mm, 105 * mm]))

    # 6. Database Design
    story.append(Paragraph("6. Database Design", styles["HeadingCenter"]))
    for text in DATABASE_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 3. Core Database Tables and Purpose", styles["Center"]))
    story.append(rl_table([["Table", "Purpose"]] + DATABASE_TABLE_ROWS, [40 * mm, 110 * mm]))
    story.append(Spacer(1, 8))
    story.append(RLImage(str(diagrams[3]["path"]), width=155 * mm, height=100 * mm))
    story.append(Paragraph(f"Figure 4. {diagrams[3]['title']}", styles["Center"]))

    # 7. Authentication and Security
    story.append(Paragraph("7. Authentication and Security", styles["HeadingCenter"]))
    for text in SECURITY_TEXT:
        story.append(Paragraph(text, styles["Body"]))

    # 8. Project Management
    story.append(Paragraph("8. Project Management", styles["HeadingCenter"]))
    for text in PROJECT_MANAGEMENT_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 4. Development Methodology Phases", styles["Center"]))
    story.append(rl_table([["Phase", "Description"]] + METHODOLOGY_PHASES, [38 * mm, 112 * mm]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Table 5. Project Implementation Timeline", styles["Center"]))
    story.append(rl_table([["Week", "Planned Activities"]] + TIMELINE_ROWS, [30 * mm, 120 * mm]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Table 6. Risk Assessment and Mitigation Matrix", styles["Center"]))
    story.append(rl_table([["Risk Area", "Possible Impact", "Mitigation Strategy"]] + RISK_ROWS, [35 * mm, 55 * mm, 60 * mm]))

    # 9. Results and Evaluation
    story.append(Paragraph("9. Results and Evaluation", styles["HeadingCenter"]))
    for text in RESULTS_TEXT:
        story.append(Paragraph(text, styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 7. Capstone Functionality Implementation Coverage", styles["Center"]))
    story.append(rl_table([["Functionality", "Status", "Implementation Detail"]] + FUNCTIONAL_COVERAGE_ROWS, [45 * mm, 30 * mm, 75 * mm]))

    # 10. Conclusion
    story.append(Paragraph("10. Conclusion", styles["HeadingCenter"]))
    for text in CONCLUSION_TEXT:
        story.append(Paragraph(text, styles["Body"]))

    # Annexure A
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE A. KEY IMPLEMENTED REST ENDPOINTS", styles["HeadingCenter"]))
    story.append(Paragraph("The following API summaries document the endpoint contracts developed to connect the React front-end pages to the Spring Boot REST services:", styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 8. REST API Endpoint Catalog", styles["Center"]))
    story.append(rl_table([["Endpoint Pattern", "Access", "Detailed Purpose"]] + IMPLEMENTED_ENDPOINTS, [50 * mm, 25 * mm, 75 * mm]))

    # Annexure B
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE B. ENTITY-TO-MODULE MAPPINGS", styles["HeadingCenter"]))
    story.append(Paragraph("This annexure links system entity classes with the corresponding application modules:", styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 9. Database Entity to Application Module Mapping", styles["Center"]))
    story.append(rl_table([["Entity Class", "Module Category", "Functional Responsibility"]] + ENTITY_MAP_ROWS, [40 * mm, 40 * mm, 70 * mm]))

    # Annexure C
    story.append(PageBreak())
    story.append(Paragraph("ANNEXURE C. SYSTEM DESIGN DIAGRAMS", styles["HeadingCenter"]))
    story.append(Paragraph("The following detailed diagrams demonstrate system workflows, lifecycle execution, and server deployment boundaries:", styles["Body"]))
    
    for idx, d in enumerate(diagrams[4:], start=5):
        story.append(Spacer(1, 8))
        story.append(RLImage(str(d["path"]), width=155 * mm, height=105 * mm))
        story.append(Paragraph(f"Figure {idx}. {d['title']}", styles["Center"]))

    doc.build(story, canvasmaker=NumberedCanvas)


def main():
    context = DIAGRAMS / "figure1_context_diagram.png"
    architecture = DIAGRAMS / "figure2_architecture_diagram.png"
    usecase = DIAGRAMS / "figure3_usecase_diagram.png"
    er = DIAGRAMS / "figure4_er_diagram.png"
    auth_seq = DIAGRAMS / "figure5_auth_sequence_diagram.png"
    activity = DIAGRAMS / "figure6_activity_diagram.png"
    deployment = DIAGRAMS / "figure7_deployment_diagram.png"
    
    print("Generating diagrams...")
    create_context_diagram(context)
    create_architecture_diagram(architecture)
    create_usecase_diagram(usecase)
    create_er_diagram(er)
    create_auth_sequence_diagram(auth_seq)
    create_activity_diagram(activity)
    create_deployment_diagram(deployment)
    
    diagrams = [
        {"path": context, "title": "Context Diagram of NovaBank"},
        {"path": architecture, "title": "Layered System Architecture of NovaBank"},
        {"path": usecase, "title": "Use Case Diagram of NovaBank"},
        {"path": er, "title": "Database Entity Relationship Diagram of NovaBank"},
        {"path": auth_seq, "title": "Authentication Sequence Diagram of NovaBank"},
        {"path": activity, "title": "Beneficiary Management Activity Diagram of NovaBank"},
        {"path": deployment, "title": "Deployment and Runtime View of NovaBank"},
    ]
    
    print("Building Word Document...")
    build_docx(diagrams)
    
    print("Building PDF...")
    build_pdf(diagrams)
    print("Done generating Capstone Final Report!")


if __name__ == "__main__":
    main()
