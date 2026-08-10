from pathlib import Path
from math import ceil
import textwrap

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.shared import RGBColor

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

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("output/interim-report")
ROOT.mkdir(parents=True, exist_ok=True)
DIAGRAMS = ROOT / "diagrams"
DIAGRAMS.mkdir(parents=True, exist_ok=True)
DOCX_PATH = ROOT / "NovaBank_Interim_Report_v4.docx"
PDF_PATH = ROOT / "NovaBank_Interim_Report_v4.pdf"


TITLE = "NovaBank: Interim Report"
PROJECT_TITLE = "NovaBank: A Secure Full-Stack Digital Banking Web Application with AI-Inspired Fraud Detection and Financial Health Analytics"
STUDENT_NAME = "Chethan BV"
USN = "241VMTR01537"
COURSE = "Master of Computer Applications"
ELECTIVE = "Full Stack Development"
DATE = "29/06/2026"
GUIDE = "[Faculty Name - JAIN Online]"


EXEC_SUMMARY = [
    "NovaBank is a full-stack digital banking web application being developed as a capstone project in Full Stack Development. The project focuses on delivering a secure, role-based banking platform where customers can register, log in, manage beneficiaries, view account details, and perform protected banking operations, while administrators can monitor customer information and platform-wide activity through a dedicated dashboard.",
    "The project uses React, Tailwind CSS, Axios, and React Router on the frontend, with Java Spring Boot, Spring Security, JWT authentication, Spring Data JPA, and MySQL on the backend. During the interim phase, the core authentication flow has been implemented, beneficiary management is operational, and the admin module can retrieve customer details without exposing sensitive fields such as passwords. Additional modules such as secure transfer processing, fraud analytics, transaction history, and financial health insights have also been scaffolded and largely implemented, placing the project ahead of the minimum interim requirement baseline.",
    "This interim report documents the current project scope, methodology, architecture, progress achieved, remaining tasks, and the planned timeline for completion. It also provides evidence that the mandatory interim submission features are functional and aligned with the capstone rubric.",
]

BACKGROUND_REVIEW = [
    "Digital banking systems have become central to modern financial service delivery because they reduce dependence on physical branches and enable always-available customer interaction. In the Full Stack Development domain, banking projects are particularly useful academic case studies because they require secure authentication, reliable state handling, database consistency, user-role separation, and responsive user interfaces within one integrated application.",
    "Traditional academic mini-projects often stop at CRUD interfaces, but a banking system requires more than simple data entry. It must protect sensitive user information, maintain auditable transaction records, separate admin and customer privileges, and preserve correctness in financial operations. This makes NovaBank relevant not only as a software product but also as a demonstration of applied software engineering principles.",
    "The project also aligns with broader industry practices in which frontend applications communicate with backend REST APIs using stateless tokens. This pattern is widely used in fintech and SaaS systems because it supports scalable architecture and clear separation between presentation, business logic, and persistence layers. By using React on the frontend and Spring Boot on the backend, the project mirrors a professional stack used in many enterprise applications.",
    "From an academic perspective, the project is significant because it integrates multiple competencies expected from a full stack learner: frontend development, backend design, API design, security, database normalization, documentation, and report-based communication. The interim report therefore serves not only as a status update but also as evidence that the project is being developed according to a methodical and technically sound plan.",
]


INTRODUCTION = [
    "The banking domain has rapidly evolved from branch-centric operations to digital-first customer service models. Users now expect seamless access to banking functions such as account management, fund transfer, transaction visibility, and fraud monitoring through secure web-based systems. In response to these expectations, NovaBank is proposed as a secure full-stack digital banking application that demonstrates how modern frontend and backend technologies can be integrated to deliver a production-style banking workflow.",
    "The primary goal of the project is to build a role-based application supporting two actors: Customer and Admin. Customers should be able to register, log in, manage beneficiary payees, access account information, and use banking services through an intuitive interface. Admin users should be able to monitor customer details and platform activity without accessing sensitive information such as passwords. The project is significant because it combines secure authentication, domain modeling, REST API design, relational database implementation, and responsive user interface development within one coherent full-stack system.",
    "From a Full Stack Development perspective, the project is relevant because it demonstrates the complete path from requirement analysis and database design to frontend integration and API security. It also introduces applied concerns such as stateless JWT authentication, layered architecture, DTO-based API design, transactional consistency, and analytics-oriented service modules.",
]


SCOPE_TEXT = [
    "The scope of the interim phase is focused on establishing the secure foundation of the banking platform and implementing the minimum functional requirements mandated for evaluation. The report therefore concentrates on the authentication workflow, beneficiary management, and admin-side customer visibility, while also documenting the broader architecture that supports later modules.",
    "Within the current scope, the project covers customer registration and login, JWT-based session handling, role-protected routing, customer beneficiary creation and retrieval, and admin access to customer details via safe DTO responses. The broader project architecture also includes account summary, transaction history, fund transfer, fraud analytics, and financial insight modules, although the interim assessment emphasizes the earlier milestone features.",
    "The main scope boundary is that the current project remains a web application and does not include native mobile apps, inter-bank payment gateway integration, or a machine-learning-based fraud engine. The current implementation of beneficiary management stores beneficiary name, bank name, account number, IFSC code, and nickname. A configurable per-beneficiary max limit can be treated as a planned refinement for final-phase alignment with extended banking specifications.",
]

FUNCTIONAL_REQUIREMENTS = [
    "User authentication through register and login workflows.",
    "Role-based access control for Customer and Admin users.",
    "Customer profile and account summary retrieval.",
    "Customer beneficiary creation, update, deletion, and listing.",
    "Admin view of customer records excluding sensitive password data.",
    "Transaction and transfer modules prepared for secure banking operations.",
    "Fraud analytics and financial health insight services prepared for final stage completion.",
]

NON_FUNCTIONAL_REQUIREMENTS = [
    "Security: passwords must be stored using BCrypt hashing and protected APIs must require valid JWT tokens.",
    "Reliability: database operations related to financial activity should use transactional integrity.",
    "Maintainability: code should remain modular through layered architecture and DTO-based API contracts.",
    "Usability: the frontend should remain responsive and easy to navigate for both customer and admin roles.",
    "Performance: API responses should remain lightweight and avoid exposing unnecessary relational data.",
]


OBJECTIVES = [
    "Implement a secure customer registration and login workflow using Spring Security, BCrypt, JWT, and React-based authentication state handling.",
    "Allow customers to add and manage beneficiaries with core payee details required for future banking transactions.",
    "Allow administrators to view customer details through protected APIs without exposing sensitive fields such as passwords.",
    "Establish a scalable layered backend architecture using controller, service, repository, dto, entity, config, security, and exception packages.",
    "Prepare the platform for advanced modules such as transfer processing, transaction history, fraud analytics, and financial health insights in subsequent milestones.",
]


METHODOLOGY = [
    "The project follows an Agile and iterative development methodology. The implementation has been divided into logical increments so that each sprint or milestone establishes a stable feature set before the next one is integrated. This approach is particularly suitable for capstone development because it allows authentication, role-based access, beneficiary management, and admin monitoring to be validated early, while more advanced features are added progressively.",
    "The backend is developed using Java Spring Boot with Spring Security, JWT, Spring Data JPA, and Maven. Spring Boot is used to expose REST APIs, Spring Security enforces authentication and authorization, and JPA simplifies relational data persistence. MySQL is used as the normalized relational database. On the frontend, React with Vite is used to create a responsive Single Page Application. Tailwind CSS is used for styling, Axios for API consumption, and React Router for navigation and route protection.",
    "The development process also follows layered architecture principles. Controllers handle HTTP requests, services contain business logic, repositories manage data access, DTOs define API payloads, and security classes handle token validation and authentication flow. This structure improves maintainability, readability, and testability.",
]

METHODOLOGY_PHASES = [
    ("Requirement Analysis", "Study digital banking workflows, identify interim deliverables, and define customer/admin user roles."),
    ("System Design", "Design database schema, package structure, frontend routes, and security workflow."),
    ("Implementation", "Develop APIs, frontend pages, authentication flow, DTOs, and beneficiary/admin features."),
    ("Validation", "Test registration, login, beneficiary management, and admin visibility using API and UI checks."),
    ("Documentation", "Prepare synopsis, interim report, diagrams, screenshots, and project presentation artefacts."),
]


ARCHITECTURE_TEXT = [
    "NovaBank follows a client-server architecture in which the React frontend communicates with a Spring Boot REST backend over HTTP. The backend uses a layered design to separate concerns across controller, service, repository, dto, and security layers. This design improves maintainability and helps ensure that sensitive business logic, such as authentication and transfer processing, is not mixed with presentation concerns.",
    "The chosen architectural pattern is a modular monolith with enterprise-style layering. This is appropriate for a capstone project because it keeps deployment and reasoning manageable while still demonstrating secure, scalable, and professional software structure. JWT-based stateless authentication is used so that the frontend can call protected backend APIs without relying on server-side sessions.",
    "Key design principles used in the project include separation of concerns, principle of least privilege, DTO-based response shaping, stateless authentication, atomic database transactions for financial operations, and reusable component design on the frontend.",
]

DATABASE_TEXT = [
    "The application uses MySQL as a normalized relational database. The main entities are users, roles, accounts, beneficiaries, transactions, and fraud_logs. These entities are mapped through JPA models and linked using one-to-one, many-to-one, and many-to-many relationships as required by the domain model.",
    "At interim stage, the most relevant database flow concerns user creation, role assignment, account provisioning, beneficiary persistence, and admin-safe retrieval of customer records. The design avoids exposing raw entity structures directly to the frontend and instead uses DTOs to return only the required fields.",
    "The database design is intentionally extensible. Although the interim review focuses on login, registration, beneficiary creation, and admin visibility, the same schema already supports transaction recording, transfer processing, and fraud analytics in subsequent phases.",
]

DATABASE_TABLE_ROWS = [
    ("users", "Stores customer/admin identity, contact details, hashed password, and status fields."),
    ("roles", "Stores role definitions such as ROLE_ADMIN and ROLE_CUSTOMER."),
    ("user_roles", "Maps users to roles using a normalized many-to-many relation."),
    ("accounts", "Stores account number, balance, currency, and user linkage."),
    ("beneficiaries", "Stores payee information such as beneficiary name, account number, bank name, IFSC, and nickname."),
    ("transactions", "Stores ledger-style debit/credit transaction records with sender and receiver account references."),
    ("fraud_logs", "Stores risk score, risk level, and evaluation reasons linked to transfer events."),
]

MODULE_DESCRIPTION_ROWS = [
    ("Authentication Module", "Handles registration, login, password hashing, token issuance, and protected API access."),
    ("Customer Module", "Supports profile access, account summary, beneficiary management, and customer-facing operations."),
    ("Admin Module", "Provides admin dashboard access and customer listing using safe DTO responses."),
    ("Beneficiary Module", "Stores and validates beneficiary information required for future transfers."),
    ("Security Module", "Includes JWT filter, custom user details service, CORS setup, and Spring Security configuration."),
    ("Persistence Module", "Uses JPA repositories and entities to manage MySQL access in a layered way."),
]

SECURITY_TEXT = [
    "Security is a central design concern in NovaBank. Authentication is implemented using Spring Security and JWT so that public endpoints such as registration and login remain separate from protected customer and admin operations. BCrypt password hashing is used to ensure that plain-text passwords are never stored in the database.",
    "The frontend stores the authenticated session payload locally and sends the JWT in the Authorization header on subsequent requests through an Axios interceptor. On the backend, a custom JWT authentication filter validates the token, extracts the username, loads the associated user details, and populates the Spring Security context before controller execution.",
    "Role-based authorization ensures that only admins can access admin endpoints, while customers and admins can access permitted customer routes according to the configured rules. In addition, safe DTOs prevent sensitive entity fields from being exposed accidentally through API responses.",
]


PROGRESS_TEXT = [
    "During the interim period, the project has moved beyond basic setup and now includes a functioning authentication pipeline, customer-facing beneficiary management, and admin visibility into customer data. The implemented codebase contains the full project structure for controllers, services, repositories, entities, DTOs, and security configuration, along with a responsive React frontend and MySQL persistence layer.",
    "The mandatory interim features have been implemented as follows: login is available through the authentication API and React login page, customer registration is available through the registration API and frontend signup page, customer beneficiary creation is implemented through a protected beneficiary creation API and management page, and admin customer viewing is implemented through a protected admin customer listing API that returns only safe profile information. Passwords are excluded because admin responses use DTOs rather than exposing the User entity directly.",
    "Additional progress includes profile management, account summary, transaction history endpoints, dashboard routes, transfer processing logic, fraud log generation, and financial insight calculations. This means the project already has a stronger functional base than the minimum interim checklist, although not all features need to be emphasized equally during interim evaluation.",
    "The main challenge encountered so far has been aligning the banking data model with safe transactional behavior while still keeping the architecture simple enough for academic presentation. Another challenge has been schema evolution during iterative development, especially when changes in transfer ledger design required corresponding updates in database constraints.",
]

CHALLENGE_ROWS = [
    ("Schema evolution", "Changes in transfer ledger design required care when aligning entity structure and database constraints."),
    ("Role-safe API design", "Customer details had to be exposed to admin users without leaking password or internal entity information."),
    ("State synchronization", "Frontend auth state, route protection, and backend token validation had to remain consistent."),
    ("Documentation alignment", "The report and diagrams needed to reflect implemented scope honestly while remaining academically complete."),
]

TESTING_TEXT = [
    "During the interim phase, validation has focused on functionality testing and API correctness rather than full automated test coverage. The registration and login flows have been tested through the frontend pages as well as REST endpoint validation. Beneficiary creation and retrieval have been verified as protected customer operations, and the admin customer listing has been checked to ensure that password fields are not returned.",
    "Swagger UI and application-level verification have been used as practical evidence tools during development. Error handling paths such as duplicate email or phone registration and unauthorized route access have also been considered in the backend design through validation annotations and centralized exception handling.",
]

UI_EVIDENCE_TEXT = [
    "The interim frontend already includes distinct pages for login, registration, customer dashboard, beneficiary management, transaction history, transfer, fraud analytics, financial insights, and admin dashboard routing. For interim assessment, the most relevant user-interface evidence lies in the login page, register page, beneficiary management page, and admin customer visibility page.",
    "The UI design uses React components and Tailwind CSS to provide a modern and responsive layout. Route protection on the frontend complements backend authorization by ensuring that unauthenticated users are redirected to login and that role-based navigation remains user-friendly.",
]


FUTURE_WORK_TEXT = [
    "The remaining work for project completion is centered on final stabilization, broader testing, UI refinement, and documentation polish. The secure transfer workflow, analytics modules, and admin dashboard foundation are already in place, but the final phase should focus on validation, completeness, and presentation readiness.",
    "Potential risks during the remaining phase include integration defects between modules, database migration mismatches when entity structures evolve, user interface edge cases on smaller devices, and incomplete audit of all protected route scenarios. Another practical risk is time compression near final submission, which can reduce the attention given to testing and report quality unless managed carefully.",
    "To mitigate these risks, the remaining work should prioritize regression testing, schema verification, focused bug fixing, and documentation synchronization between the codebase and final report artefacts.",
]

RISK_ROWS = [
    ("Integration inconsistency", "Mismatch between frontend payloads and backend DTO expectations", "Keep API contracts documented and revalidate key screens after every backend update."),
    ("Schema mismatch", "Database constraints may lag behind entity changes", "Review schema after entity changes and test high-risk flows such as transfer and beneficiary operations."),
    ("Security gap", "Protected routes may not be uniformly validated across modules", "Retest JWT flow and role restrictions for all customer/admin endpoints."),
    ("Time pressure", "Documentation and testing may be rushed near final submission", "Freeze feature scope and reserve dedicated time for final polishing and verification."),
]


CONCLUSION_TEXT = [
    "The interim phase of NovaBank demonstrates meaningful progress toward a full-stack banking platform. The project now includes the core security and role-management foundation required for a digital banking application, and it satisfies the central interim deliverables of registration, login, beneficiary creation, and admin-side customer visibility.",
    "Important lessons learned so far include the value of DTO-based API design for security, the importance of maintaining clean service-layer boundaries, and the need to keep database evolution synchronized with business logic. Adjustments have also been made in the transaction model to better reflect sender-receiver ledger behavior and to preserve consistency during fund transfer operations.",
    "The next steps are to complete final validation of remaining modules, finish documentation and presentation artefacts, and strengthen the overall polish of the project. By the end of the capstone, NovaBank is expected to stand as a coherent, secure, and professionally structured full-stack banking application.",
]


TECH_STACK_ROWS = [
    ("Frontend", "React 18, Vite, Tailwind CSS, Axios, React Router"),
    ("Backend", "Java 17, Spring Boot 3, Spring Security, JWT, Spring Data JPA, Maven"),
    ("Database", "MySQL"),
    ("Documentation & API Testing", "Swagger UI via SpringDoc OpenAPI"),
    ("Design Approach", "Layered client-server architecture with modular monolith packaging"),
]

PROGRESS_ROWS = [
    ("Project scaffolding and repository setup", "Completed", "Backend and frontend structures initialized with clear package separation."),
    ("User registration", "Completed", "Public registration API creates customer user and account."),
    ("User login with JWT", "Completed", "Spring Security and React auth flow are operational."),
    ("Customer beneficiary addition", "Completed", "Protected create/list/update/delete beneficiary APIs implemented."),
    ("Admin view customer details", "Completed", "Protected admin customer API returns safe profile DTOs without password exposure."),
    ("Account summary and profile module", "Completed", "Customer profile and account endpoints implemented."),
    ("Transfer and transaction modules", "In progress / advanced build", "Core logic implemented; final validation and reporting alignment ongoing."),
    ("Fraud analytics and financial insights", "In progress / advanced build", "Service and UI modules prepared for final polish."),
]

TIMELINE_ROWS = [
    ("Week 1", "Requirement analysis, project planning, repo setup, initial backend and frontend scaffolding"),
    ("Week 2", "Database schema design, entity modeling, repository creation, datasource configuration"),
    ("Week 3", "Authentication module, JWT flow, role-based security, registration and login pages"),
    ("Week 4", "Beneficiary module, account/profile APIs, admin customer listing, exception handling"),
    ("Week 5", "Transaction processing, atomic update design, fraud log integration"),
    ("Week 6", "Frontend integration, dashboards, protected routing, transaction views"),
    ("Week 7", "Testing, bug fixing, responsiveness review, diagram and report refinement"),
    ("Week 8", "Final stabilization, viva preparation, final report and presentation submission"),
]

IMPLEMENTED_ENDPOINTS = [
    ("POST /api/auth/register", "Public customer registration"),
    ("POST /api/auth/login", "Authentication and JWT token issuance"),
    ("POST /api/customer/beneficiaries", "Add beneficiary for logged-in customer"),
    ("GET /api/customer/beneficiaries", "View beneficiary list for logged-in customer"),
    ("GET /api/admin/customers", "Admin view of customer details using safe DTOs"),
]

API_SUMMARY_ROWS = [
    ("POST /api/auth/register", "Public", "Customer signup and account provisioning"),
    ("POST /api/auth/login", "Public", "Credential verification and JWT token generation"),
    ("GET /api/customer/profile", "Customer/Admin", "Fetch user profile details"),
    ("GET /api/customer/account", "Customer/Admin", "Fetch customer account summary"),
    ("POST /api/customer/beneficiaries", "Customer/Admin", "Create a new beneficiary"),
    ("GET /api/customer/beneficiaries", "Customer/Admin", "List saved beneficiaries"),
    ("GET /api/admin/customers", "Admin", "View customer details without sensitive password data"),
]


def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/timesbi.ttf" if bold else "C:/Windows/Fonts/timesi.ttf",
    ]
    for path in candidates:
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


def create_context_diagram(path: Path):
    img = Image.new("RGB", (1400, 900), "white")
    draw = ImageDraw.Draw(img)
    draw.text((490, 40), "Figure 1. Context Diagram of NovaBank", font=FONT_BOLD, fill="#111827")
    draw_box(draw, (500, 300, 900, 500), "NovaBank\nBanking Platform", fill="#D1FAE5", title=True)
    draw_box(draw, (90, 180, 370, 340), "Customer", fill="#EFF6FF")
    draw_box(draw, (90, 560, 370, 720), "Admin", fill="#FEF3C7")
    draw_box(draw, (1030, 300, 1310, 500), "MySQL\nDatabase", fill="#F3E8FF")
    draw_arrow(draw, (370, 260), (500, 360))
    draw_arrow(draw, (370, 640), (500, 440))
    draw_arrow(draw, (900, 400), (1030, 400))
    draw.multiline_text((120, 355), wrapped_text("Register, Login, View Account, Manage Beneficiaries, Transfer Funds", 34), font=FONT_SMALL, fill="#334155", spacing=4)
    draw.multiline_text((120, 735), wrapped_text("View Customers, Monitor Transactions, Review Fraud Logs", 22), font=FONT_SMALL, fill="#334155", spacing=4)
    draw.multiline_text((950, 520), wrapped_text("Stores users, roles, accounts, beneficiaries, transactions, fraud logs", 24), font=FONT_SMALL, fill="#334155", spacing=4)
    img.save(path)


def create_architecture_diagram(path: Path):
    img = Image.new("RGB", (1400, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((420, 40), "Figure 2. Layered System Architecture", font=FONT_BOLD, fill="#111827")
    draw_box(draw, (420, 120, 980, 240), "React Frontend\nAuth, Dashboard, Beneficiaries,\nAdmin UI", fill="#DBEAFE", title=True)
    draw_box(draw, (420, 300, 980, 420), "Controllers\nAuth | Customer | Admin", fill="#E0F2FE")
    draw_box(draw, (420, 480, 980, 600), "Service Layer\nAuth | User | Account |\nBeneficiary | Transaction | Admin", fill="#DCFCE7")
    draw_box(draw, (420, 660, 980, 780), "Repository Layer\nUser | Role | Account |\nBeneficiary | Transaction", fill="#FEF3C7")
    draw_box(draw, (420, 840, 980, 940), "MySQL Database", fill="#F3E8FF")
    draw_box(draw, (1060, 320, 1370, 620), "Security Layer\nJWT Filter\nUserDetailsService\nSecurityConfig\nBCrypt Encoder", fill="#FEE2E2")
    for y1, y2 in [(240, 300), (420, 480), (600, 660), (780, 840)]:
        draw_arrow(draw, (700, y1), (700, y2))
    draw_arrow(draw, (980, 360), (1060, 360))
    draw_arrow(draw, (1060, 540), (980, 540))
    img.save(path)


def create_usecase_diagram(path: Path):
    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((420, 35), "Figure 3. Interim Use Case Diagram", font=FONT_BOLD, fill="#111827")
    draw.rectangle((360, 120, 1240, 860), outline="#0F172A", width=3)
    draw.text((650, 130), "NovaBank System Boundary", font=FONT_SMALL, fill="#0F172A")
    draw_box(draw, (60, 270, 260, 430), "Customer", fill="#EFF6FF")
    draw_box(draw, (60, 620, 260, 780), "Admin", fill="#FEF3C7")

    ellipses = [
        ((520, 210, 920, 300), "Register"),
        ((520, 340, 920, 430), "Login"),
        ((520, 470, 920, 560), "Add Beneficiary"),
        ((520, 600, 920, 690), "View Account / Profile"),
        ((520, 730, 920, 820), "View Customer Details"),
    ]
    for box, label in ellipses:
        draw.ellipse(box, outline="#0F172A", width=3, fill="#F8FAFC")
        bbox = draw.multiline_textbbox((0, 0), label, font=FONT_REG)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x1, y1, x2, y2 = box
        draw.multiline_text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2), label, font=FONT_REG, fill="#0F172A")

    draw.line((260, 330, 520, 255), fill="#0F172A", width=3)
    draw.line((260, 350, 520, 385), fill="#0F172A", width=3)
    draw.line((260, 370, 520, 515), fill="#0F172A", width=3)
    draw.line((260, 390, 520, 645), fill="#0F172A", width=3)
    draw.line((260, 700, 520, 775), fill="#0F172A", width=3)
    draw.line((260, 680, 520, 385), fill="#0F172A", width=3)
    img.save(path)


def create_er_diagram(path: Path):
    img = Image.new("RGB", (1500, 980), "white")
    draw = ImageDraw.Draw(img)
    draw.text((500, 35), "Figure 4. Database Entity Relationship View", font=FONT_BOLD, fill="#111827")
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
    draw.text((430, 35), "Figure 5. Authentication Sequence Diagram", font=FONT_BOLD, fill="#111827")
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
    draw.text((430, 35), "Figure 6. Beneficiary Management Activity Diagram", font=FONT_BOLD, fill="#111827")
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
    draw.text((450, 35), "Figure 7. Deployment / Runtime View", font=FONT_BOLD, fill="#111827")
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


def add_footer(section):
    footer = section.footer
    para = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(para)


def add_para(doc, text="", bold=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    r.font.size = Pt(size)
    r.bold = bold
    if bold:
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_heading(doc, text, level_number):
    return add_para(doc, f"{level_number}. {text}", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=8)


def add_bullet(doc, text):
    p = doc.add_paragraph(style=None)
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
    add_footer(doc.sections[0])

    add_para(doc, "MCA Semester – IV", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_para(doc, "Interim Report", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_para(doc, PROJECT_TITLE, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_para(doc, "Research Project submitted to Jain Online (Deemed-to-be University) in partial fulfillment of the requirements for the award of:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, COURSE, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_para(doc, f"Submitted by\n{STUDENT_NAME}\nUSN: {USN}\nElective: {ELECTIVE}", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_para(doc, f"Under the guidance of\n{GUIDE}", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_para(doc, f"Date of Submission: {DATE}", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    doc.add_page_break()
    add_para(doc, "DECLARATION", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    declaration = (
        f"I, {STUDENT_NAME}, hereby declare that this Interim Report has been prepared by me under the guidance of {GUIDE}. "
        "I declare that this report is submitted towards the partial fulfillment of the credit requirement for the course "
        "“Capstone Project,” which is part of the Master of Computer Applications programme offered by Jain Online. "
        "I further declare that the work documented in this report is original in nature and reflects my own contribution."
    )
    add_para(doc, declaration)
    add_para(doc, "Place: ____________________", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    add_para(doc, f"Date: {DATE}", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    add_para(doc, f"Name of the Student: {STUDENT_NAME}\nUSN: {USN}", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)

    doc.add_page_break()
    add_para(doc, "EXECUTIVE SUMMARY", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    for paragraph in EXEC_SUMMARY:
        add_para(doc, paragraph)

    doc.add_page_break()
    add_para(doc, "TABLE OF CONTENTS", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    toc_items = [
        "1. Introduction",
        "2. Project Scope and Objectives",
        "3. Methodology",
        "4. System Architecture and Design",
        "5. Progress and Accomplishments",
        "6. Future Work and Timeline",
        "Annexure A. Key Implemented Endpoints",
        "Annexure B. API Summary and Database Overview",
        "Annexure C. Additional Design Diagrams",
        "7. Conclusion",
    ]
    for item in toc_items:
        add_para(doc, item, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4)

    doc.add_page_break()
    add_heading(doc, "Introduction", 1)
    for paragraph in INTRODUCTION:
        add_para(doc, paragraph)
    add_para(doc, "Background and Relevance", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for paragraph in BACKGROUND_REVIEW:
        add_para(doc, paragraph)

    add_heading(doc, "Project Scope and Objectives", 2)
    for paragraph in SCOPE_TEXT:
        add_para(doc, paragraph)
    add_para(doc, "Functional Requirements", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for item in FUNCTIONAL_REQUIREMENTS:
        add_bullet(doc, item)
    add_para(doc, "Non-Functional Requirements", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for item in NON_FUNCTIONAL_REQUIREMENTS:
        add_bullet(doc, item)
    add_para(doc, "Project Objectives", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for item in OBJECTIVES:
        add_bullet(doc, item)

    add_heading(doc, "Methodology", 3)
    for paragraph in METHODOLOGY:
        add_para(doc, paragraph)
    add_table_title(doc, "Table 1. Technology Stack and Frameworks Used")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Layer", "Technologies / Tools"]] + list(TECH_STACK_ROWS), bold_first_row=True)
    add_table_title(doc, "Table 2. Development Methodology Phases")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Phase", "Description"]] + list(METHODOLOGY_PHASES), bold_first_row=True)

    add_heading(doc, "System Architecture and Design", 4)
    for paragraph in ARCHITECTURE_TEXT:
        add_para(doc, paragraph)
    add_para(doc, "Database Design Overview", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for paragraph in DATABASE_TEXT:
        add_para(doc, paragraph)
    add_table_title(doc, "Table 3. Core Database Tables and Purpose")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Table", "Purpose"]] + list(DATABASE_TABLE_ROWS), bold_first_row=True)
    add_table_title(doc, "Table 4. Major Application Modules")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Module", "Description"]] + list(MODULE_DESCRIPTION_ROWS), bold_first_row=True)
    add_para(doc, "Security Design Considerations", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for paragraph in SECURITY_TEXT:
        add_para(doc, paragraph)
    for idx, diagram in enumerate(diagrams, start=1):
        doc.add_picture(str(diagram["path"]), width=Inches(6.1))
        caption = f"Figure {idx}. {diagram['title']}"
        add_para(doc, caption, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    add_heading(doc, "Progress and Accomplishments", 5)
    for paragraph in PROGRESS_TEXT:
        add_para(doc, paragraph)
    add_table_title(doc, "Table 2. Interim Progress Matrix")
    table = doc.add_table(rows=1, cols=3)
    fill_table(table, [["Milestone", "Status", "Remarks"]] + list(PROGRESS_ROWS), bold_first_row=True)
    add_table_title(doc, "Table 3. Mandatory Interim Functionality Coverage")
    table = doc.add_table(rows=1, cols=3)
    coverage_rows = [
        ("Login", "Implemented", "Available through /api/auth/login and React Login page."),
        ("Register / Signup", "Implemented", "Available through /api/auth/register and React Register page."),
        ("Customer can add beneficiaries", "Implemented", "Protected beneficiary API and management page are operational."),
        ("Admin can view customer details excluding password", "Implemented", "Admin uses UserProfileDto and does not receive password data."),
    ]
    fill_table(table, [["Functionality", "Coverage", "Evidence"]] + coverage_rows, bold_first_row=True)
    add_para(doc, "Testing and Validation Evidence", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for paragraph in TESTING_TEXT:
        add_para(doc, paragraph)
    add_para(doc, "User Interface Evidence", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    for paragraph in UI_EVIDENCE_TEXT:
        add_para(doc, paragraph)
    add_table_title(doc, "Table 4. Challenges Encountered During Interim Phase")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Challenge", "Observation"]] + list(CHALLENGE_ROWS), bold_first_row=True)

    add_heading(doc, "Future Work and Timeline", 6)
    for paragraph in FUTURE_WORK_TEXT:
        add_para(doc, paragraph)
    add_table_title(doc, "Table 5. Remaining Work Timeline")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Week", "Planned Activities"]] + list(TIMELINE_ROWS), bold_first_row=True)
    add_table_title(doc, "Table 6. Risk Assessment for Remaining Phase")
    table = doc.add_table(rows=1, cols=3)
    fill_table(table, [["Risk", "Possible Impact", "Mitigation"]] + list(RISK_ROWS), bold_first_row=True)

    doc.add_page_break()
    add_para(doc, "ANNEXURE A. KEY IMPLEMENTED ENDPOINTS", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "The following endpoints provide concise evidence of the minimum interim functionality that has been implemented in the current project version.")
    add_table_title(doc, "Table 7. Key Implemented REST Endpoints")
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Endpoint", "Purpose"]] + list(IMPLEMENTED_ENDPOINTS), bold_first_row=True)

    doc.add_page_break()
    add_para(doc, "ANNEXURE B. API SUMMARY AND DATABASE OVERVIEW", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "This annexure summarizes key API routes and database mappings that support the implemented interim functionality.")
    add_table_title(doc, "Table 8. API Summary")
    table = doc.add_table(rows=1, cols=3)
    fill_table(table, [["Endpoint", "Access", "Purpose"]] + list(API_SUMMARY_ROWS), bold_first_row=True)
    add_table_title(doc, "Table 9. Entity-to-Module Mapping")
    entity_map_rows = [
        ("User + Role", "Authentication and Authorization"),
        ("Account", "Profile and Account Summary"),
        ("Beneficiary", "Beneficiary Management"),
        ("Transaction", "Transfer and History Modules"),
        ("FraudLog", "Fraud Analytics"),
    ]
    table = doc.add_table(rows=1, cols=2)
    fill_table(table, [["Entity Group", "Mapped Module"]] + entity_map_rows, bold_first_row=True)

    doc.add_page_break()
    add_para(doc, "ANNEXURE C. ADDITIONAL DESIGN DIAGRAMS", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "The following diagrams provide additional technical explanation for database relationships, authentication flow, user activity, and deployment view.")
    for idx, diagram in enumerate(diagrams[3:], start=4):
        doc.add_picture(str(diagram["path"]), width=Inches(6.1))
        caption = f"Figure {idx}. {diagram['title']}"
        add_para(doc, caption, bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    doc.add_page_break()
    add_heading(doc, "Conclusion", 7)
    for paragraph in CONCLUSION_TEXT:
        add_para(doc, paragraph)

    doc.save(DOCX_PATH)


def pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", fontName="Times-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="Heading", fontName="Times-Bold", fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=8))
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
    doc = SimpleDocTemplate(str(PDF_PATH), pagesize=A4, leftMargin=25 * mm, rightMargin=25 * mm, topMargin=25 * mm, bottomMargin=25 * mm)
    story = []

    story.append(Paragraph("MCA Semester – IV", styles["Center"]))
    story.append(Paragraph("Interim Report", styles["TitleCenter"]))
    story.append(Paragraph(PROJECT_TITLE, styles["Heading"]))
    story.append(Paragraph("Research Project submitted to Jain Online (Deemed-to-be University) in partial fulfillment of the requirements for the award of:", styles["Center"]))
    story.append(Paragraph(COURSE, styles["TitleCenter"]))
    story.append(Paragraph(f"Submitted by<br/>{STUDENT_NAME}<br/>USN: {USN}<br/>Elective: {ELECTIVE}", styles["Center"]))
    story.append(Paragraph(f"Under the guidance of<br/>{GUIDE}", styles["Center"]))
    story.append(Paragraph(f"Date of Submission: {DATE}", styles["Center"]))
    story.append(PageBreak())

    story.append(Paragraph("DECLARATION", styles["TitleCenter"]))
    story.append(Paragraph(
        f"I, {STUDENT_NAME}, hereby declare that this Interim Report has been prepared by me under the guidance of {GUIDE}. "
        "I declare that this report is submitted towards the partial fulfillment of the credit requirement for the course "
        "“Capstone Project,” which is part of the Master of Computer Applications programme offered by Jain Online. "
        "I further declare that the work documented in this report is original in nature and reflects my own contribution.",
        styles["Body"],
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Place: ____________________", styles["Body"]))
    story.append(Paragraph(f"Date: {DATE}", styles["Body"]))
    story.append(Paragraph(f"Name of the Student: {STUDENT_NAME}<br/>USN: {USN}", styles["Body"]))
    story.append(PageBreak())

    story.append(Paragraph("EXECUTIVE SUMMARY", styles["TitleCenter"]))
    for p in EXEC_SUMMARY:
        story.append(Paragraph(p, styles["Body"]))
    story.append(PageBreak())

    story.append(Paragraph("TABLE OF CONTENTS", styles["TitleCenter"]))
    for item in [
        "1. Introduction",
        "2. Project Scope and Objectives",
        "3. Methodology",
        "4. System Architecture and Design",
        "5. Progress and Accomplishments",
        "6. Future Work and Timeline",
        "Annexure A. Key Implemented Endpoints",
        "Annexure B. API Summary and Database Overview",
        "Annexure C. Additional Design Diagrams",
        "7. Conclusion",
    ]:
        story.append(Paragraph(item, styles["Body"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Introduction", styles["Heading"]))
    for p in INTRODUCTION:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Background and Relevance", styles["Body"]))
    for p in BACKGROUND_REVIEW:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("2. Project Scope and Objectives", styles["Heading"]))
    for p in SCOPE_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Functional Requirements", styles["Body"]))
    for item in FUNCTIONAL_REQUIREMENTS:
        story.append(Paragraph(f"- {item}", styles["BulletItem"]))
    story.append(Paragraph("Non-Functional Requirements", styles["Body"]))
    for item in NON_FUNCTIONAL_REQUIREMENTS:
        story.append(Paragraph(f"- {item}", styles["BulletItem"]))
    story.append(Paragraph("Project Objectives", styles["Body"]))
    for item in OBJECTIVES:
        story.append(Paragraph(f"- {item}", styles["BulletItem"]))

    story.append(Paragraph("3. Methodology", styles["Heading"]))
    for p in METHODOLOGY:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Table 1. Technology Stack and Frameworks Used", styles["Center"]))
    story.append(rl_table([["Layer", "Technologies / Tools"]] + [list(r) for r in TECH_STACK_ROWS], [45 * mm, 105 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Table 2. Development Methodology Phases", styles["Center"]))
    story.append(rl_table([["Phase", "Description"]] + [list(r) for r in METHODOLOGY_PHASES], [38 * mm, 112 * mm]))

    story.append(Paragraph("4. System Architecture and Design", styles["Heading"]))
    for p in ARCHITECTURE_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Database Design Overview", styles["Body"]))
    for p in DATABASE_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Table 3. Core Database Tables and Purpose", styles["Center"]))
    story.append(rl_table([["Table", "Purpose"]] + [list(r) for r in DATABASE_TABLE_ROWS], [42 * mm, 108 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Table 4. Major Application Modules", styles["Center"]))
    story.append(rl_table([["Module", "Description"]] + [list(r) for r in MODULE_DESCRIPTION_ROWS], [46 * mm, 104 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Security Design Considerations", styles["Body"]))
    for p in SECURITY_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    for idx, diagram in enumerate(diagrams[:3], start=1):
        story.append(Spacer(1, 8))
        story.append(RLImage(str(diagram["path"]), width=160 * mm, height=105 * mm))
        story.append(Paragraph(f"Figure {idx}. {diagram['title']}", styles["Center"]))

    story.append(Paragraph("5. Progress and Accomplishments", styles["Heading"]))
    for p in PROGRESS_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Table 2. Interim Progress Matrix", styles["Center"]))
    story.append(rl_table([["Milestone", "Status", "Remarks"]] + [list(r) for r in PROGRESS_ROWS], [55 * mm, 30 * mm, 65 * mm]))
    story.append(Paragraph("Table 3. Mandatory Interim Functionality Coverage", styles["Center"]))
    coverage_rows = [
        ["Login", "Implemented", "Available through /api/auth/login and React Login page."],
        ["Register / Signup", "Implemented", "Available through /api/auth/register and React Register page."],
        ["Customer can add beneficiaries", "Implemented", "Protected beneficiary API and management page are operational."],
        ["Admin can view customer details excluding password", "Implemented", "Admin uses UserProfileDto and does not receive password data."],
    ]
    story.append(rl_table([["Functionality", "Coverage", "Evidence"]] + coverage_rows, [55 * mm, 30 * mm, 65 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Testing and Validation Evidence", styles["Body"]))
    for p in TESTING_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("User Interface Evidence", styles["Body"]))
    for p in UI_EVIDENCE_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Table 4. Challenges Encountered During Interim Phase", styles["Center"]))
    story.append(rl_table([["Challenge", "Observation"]] + [list(r) for r in CHALLENGE_ROWS], [48 * mm, 102 * mm]))

    story.append(Paragraph("6. Future Work and Timeline", styles["Heading"]))
    for p in FUTURE_WORK_TEXT:
        story.append(Paragraph(p, styles["Body"]))
    story.append(Paragraph("Table 5. Remaining Work Timeline", styles["Center"]))
    story.append(rl_table([["Week", "Planned Activities"]] + [list(r) for r in TIMELINE_ROWS], [25 * mm, 125 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Table 6. Risk Assessment for Remaining Phase", styles["Center"]))
    story.append(rl_table([["Risk", "Possible Impact", "Mitigation"]] + [list(r) for r in RISK_ROWS], [38 * mm, 55 * mm, 57 * mm]))

    story.append(Paragraph("ANNEXURE A. KEY IMPLEMENTED ENDPOINTS", styles["TitleCenter"]))
    story.append(Paragraph("The following endpoints provide concise evidence of the minimum interim functionality that has been implemented in the current project version.", styles["Body"]))
    story.append(Paragraph("Table 7. Key Implemented REST Endpoints", styles["Center"]))
    story.append(rl_table([["Endpoint", "Purpose"]] + [list(r) for r in IMPLEMENTED_ENDPOINTS], [55 * mm, 95 * mm]))
    story.append(PageBreak())

    story.append(Paragraph("ANNEXURE B. API SUMMARY AND DATABASE OVERVIEW", styles["TitleCenter"]))
    story.append(Paragraph("This annexure summarizes key API routes and database mappings that support the implemented interim functionality.", styles["Body"]))
    story.append(Paragraph("Table 8. API Summary", styles["Center"]))
    story.append(rl_table([["Endpoint", "Access", "Purpose"]] + [list(r) for r in API_SUMMARY_ROWS], [48 * mm, 28 * mm, 74 * mm]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Table 9. Entity-to-Module Mapping", styles["Center"]))
    story.append(rl_table(
        [["Entity Group", "Mapped Module"]]
        + [
            ["User + Role", "Authentication and Authorization"],
            ["Account", "Profile and Account Summary"],
            ["Beneficiary", "Beneficiary Management"],
            ["Transaction", "Transfer and History Modules"],
            ["FraudLog", "Fraud Analytics"],
        ],
        [50 * mm, 100 * mm],
    ))
    story.append(PageBreak())

    story.append(Paragraph("ANNEXURE C. ADDITIONAL DESIGN DIAGRAMS", styles["TitleCenter"]))
    story.append(Paragraph("The following diagrams provide additional technical explanation for database relationships, authentication flow, user activity, and deployment view.", styles["Body"]))
    for idx, diagram in enumerate(diagrams[3:], start=4):
        story.append(Spacer(1, 8))
        story.append(RLImage(str(diagram["path"]), width=160 * mm, height=105 * mm))
        story.append(Paragraph(f"Figure {idx}. {diagram['title']}", styles["Center"]))
    story.append(PageBreak())

    story.append(Paragraph("7. Conclusion", styles["Heading"]))
    for p in CONCLUSION_TEXT:
        story.append(Paragraph(p, styles["Body"]))

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Times-Roman", 12)
        page_width, _ = A4
        canvas.drawCentredString(page_width / 2, 12 * mm, str(doc_obj.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def main():
    context = DIAGRAMS / "figure1_context_diagram.png"
    architecture = DIAGRAMS / "figure2_architecture_diagram.png"
    usecase = DIAGRAMS / "figure3_usecase_diagram.png"
    er = DIAGRAMS / "figure4_er_diagram.png"
    auth_seq = DIAGRAMS / "figure5_auth_sequence_diagram.png"
    activity = DIAGRAMS / "figure6_activity_diagram.png"
    deployment = DIAGRAMS / "figure7_deployment_diagram.png"
    create_context_diagram(context)
    create_architecture_diagram(architecture)
    create_usecase_diagram(usecase)
    create_er_diagram(er)
    create_auth_sequence_diagram(auth_seq)
    create_activity_diagram(activity)
    create_deployment_diagram(deployment)
    diagrams = [
        {"path": context, "title": "Context Diagram of NovaBank"},
        {"path": architecture, "title": "Layered System Architecture"},
        {"path": usecase, "title": "Interim Use Case Diagram"},
        {"path": er, "title": "Database Entity Relationship View"},
        {"path": auth_seq, "title": "Authentication Sequence Diagram"},
        {"path": activity, "title": "Beneficiary Management Activity Diagram"},
        {"path": deployment, "title": "Deployment / Runtime View"},
    ]
    build_docx(diagrams)
    build_pdf(diagrams)


if __name__ == "__main__":
    main()
