from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


OUTPUT = Path("output/pdf/banking-architecture-guide-part-1.pdf")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleHero",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=24,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=8,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=6,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyGuide",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="MonoBox",
        parent=styles["BodyText"],
        fontName="Courier",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#e2e8f0"),
        borderPadding=8,
        borderRadius=None,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#7c2d12"),
        backColor=colors.HexColor("#ffedd5"),
        borderPadding=8,
        spaceAfter=8,
    )
)


def p(text, style="BodyGuide"):
    return Paragraph(text, styles[style])


def code(text):
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    return Paragraph(safe, styles["MonoBox"])


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )

    story = []

    story.append(p("Banking Web Application Teaching Guide", "TitleHero"))
    story.append(p("Part 1: Architecture Overview, Backend Folder Structure, and Full Request Lifecycle"))
    story.append(
        p(
            "This guide is written as if you are preparing for a viva, interview, or project presentation. "
            "The goal is not only to know what the project does, but to explain why it is structured this way."
        )
    )
    story.append(
        p(
            "Project stack: React + Tailwind CSS + Axios + React Router on the frontend, and Spring Boot + "
            "Spring Security + JWT + JPA + MySQL on the backend."
        )
    )
    story.append(Spacer(1, 8))

    story.append(p("1. Complete Project Architecture Overview", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> The architecture is designed like a real banking system with clear separation of "
            "responsibilities. The frontend handles user interaction, the backend enforces business rules and "
            "security, and the database stores durable banking data such as users, accounts, beneficiaries, "
            "transactions, and fraud logs."
        )
    )
    story.append(p("High-level architecture diagram:", "Subsection"))
    story.append(
        code(
            "User Browser\n"
            "   |\n"
            "   v\n"
            "React Frontend\n"
            "   |  (Axios HTTP requests with JWT token)\n"
            "   v\n"
            "Spring Boot REST API\n"
            "   |\n"
            "   +--> Spring Security + JWT Filter\n"
            "   +--> Controllers\n"
            "   +--> Services\n"
            "   +--> Repositories (JPA)\n"
            "   v\n"
            "MySQL Database"
        )
    )
    story.append(
        p(
            "<b>Why this structure is good for a capstone:</b> It is simple enough to explain clearly, but strong "
            "enough to show enterprise thinking. Each layer has one job, which makes debugging, testing, and "
            "future expansion easier."
        )
    )
    story.append(p("Main modules in the project:", "Subsection"))

    architecture_rows = [
        ["Module", "Purpose"],
        ["Frontend", "Shows pages, forms, dashboards, charts, and sends API requests."],
        ["Security Layer", "Authenticates users and checks roles such as ADMIN and CUSTOMER."],
        ["Controller Layer", "Receives HTTP requests and returns JSON responses."],
        ["Service Layer", "Contains banking business logic like transfer validation and fraud scoring."],
        ["Repository Layer", "Talks to MySQL through Spring Data JPA."],
        ["Database", "Stores normalized banking records safely."],
    ]
    table = Table(architecture_rows, colWidths=[45 * mm, 125 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))

    story.append(
        p(
            "<b>Interview explanation example:</b> “I used a layered full-stack architecture so the UI, security, "
            "business logic, and persistence concerns remain separate. This makes the application more secure, "
            "easier to maintain, and closer to how enterprise banking products are built.”"
        )
    )
    story.append(
        p(
            "If the examiner asks why not microservices, you can say: for a final-year capstone, a modular monolith "
            "is a smarter choice because it keeps deployment and explanation manageable while still following "
            "professional design principles."
        )
    )
    story.append(
        p(
            "Mentor note: always explain architecture from user flow first, then from code layers. That sounds much "
            "clearer in a viva."
        ,
            "Callout",
        )
    )

    story.append(PageBreak())

    story.append(p("2. Backend Folder Structure", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> The backend is organized by responsibility. This helps a junior developer quickly know "
            "where to place code and helps interviewers see that the project follows clean architecture practices."
        )
    )
    story.append(p("Backend package structure:", "Subsection"))
    story.append(
        code(
            "backend/src/main/java/com/banking/app/\n"
            "  config/\n"
            "  controller/\n"
            "  dto/\n"
            "  entity/\n"
            "  exception/\n"
            "  repository/\n"
            "  security/\n"
            "  service/\n"
            "BankingApplication.java"
        )
    )

    story.append(p("Folder-by-folder explanation:", "Subsection"))
    folder_rows = [
        ["Folder", "What goes here", "Why it matters"],
        ["config", "Beans, startup seed data, app-level configuration", "Keeps shared setup separate from business logic."],
        ["controller", "REST endpoints like /api/auth/login", "Acts as the API entry point."],
        ["dto", "Request and response classes", "Prevents exposing entity classes directly."],
        ["entity", "JPA database models", "Represents tables and relationships."],
        ["exception", "Custom errors and global handlers", "Makes API error responses clean and consistent."],
        ["repository", "Interfaces extending JpaRepository", "Removes boilerplate SQL for standard queries."],
        ["security", "JWT service, filter, user details service, security config", "Centralizes authentication and authorization."],
        ["service", "Core logic like transfer, profile update, fraud analysis", "This is where business rules live."],
    ]
    folder_table = Table(folder_rows, colWidths=[30 * mm, 70 * mm, 70 * mm])
    folder_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(folder_table)
    story.append(Spacer(1, 8))

    story.append(
        p(
            "<b>Why code is written this way:</b> In banking software, mixing SQL, security, validation, and HTTP "
            "handling in one class becomes dangerous very quickly. By splitting the code into layers, we reduce risk "
            "and make every class easier to review."
        )
    )
    story.append(
        p(
            "<b>Security angle:</b> Sensitive logic such as token parsing, role validation, and password encoding is "
            "kept in dedicated security classes. This reduces accidental mistakes and makes audits easier."
        )
    )
    story.append(
        p(
            "<b>Database interaction angle:</b> Entities define the table structure, repositories access data, and "
            "services decide when to read or write. That means the controller does not directly manipulate the database."
        )
    )
    story.append(
        p(
            "<b>Viva answer example:</b> “I used DTOs so my API does not expose internal entity models directly. "
            "This gives me better control over validation, security, and response formatting.”"
        )
    )
    story.append(
        p(
            "Mentor note: if someone asks where transfer logic should live, the correct answer is the <b>service</b> "
            "layer, not the controller and not the repository."
        ,
            "Callout",
        )
    )

    story.append(PageBreak())

    story.append(p("3. Request Lifecycle: Frontend -> Backend -> Database -> Response", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> This is the most important flow to understand for interviews. It shows how a user action "
            "travels through the whole system and returns safely with data."
        )
    )
    story.append(p("Example scenario: customer logs in and opens the dashboard.", "Subsection"))
    story.append(
        code(
            "Step 1: User enters email and password in React login form\n"
            "Step 2: Axios sends POST /api/auth/login to Spring Boot\n"
            "Step 3: AuthController receives the request\n"
            "Step 4: AuthService authenticates using Spring Security\n"
            "Step 5: JWT token is generated and returned\n"
            "Step 6: React stores the token\n"
            "Step 7: React sends GET /api/customer/account with Authorization header\n"
            "Step 8: JWT filter validates token before controller executes\n"
            "Step 9: Controller calls service\n"
            "Step 10: Service calls repository\n"
            "Step 11: Repository reads data from MySQL\n"
            "Step 12: DTO response is returned as JSON\n"
            "Step 13: React renders dashboard cards and tables"
        )
    )

    story.append(p("Simple lifecycle diagram:", "Subsection"))
    story.append(
        code(
            "React Page\n"
            "  |\n"
            "  | Axios request\n"
            "  v\n"
            "Controller\n"
            "  |\n"
            "  v\n"
            "Service\n"
            "  |\n"
            "  v\n"
            "Repository\n"
            "  |\n"
            "  v\n"
            "MySQL\n"
            "  |\n"
            "  v\n"
            "Repository -> Service -> Controller -> JSON Response -> React UI"
        )
    )

    story.append(p("How frontend-backend communication works:", "Subsection"))
    story.append(
        p(
            "The frontend uses Axios to send HTTP requests. For protected APIs, Axios attaches the JWT token in the "
            "Authorization header. The backend returns JSON, and React updates the page state using that response."
        )
    )
    story.append(
        p(
            "Example: when the dashboard loads, React calls <b>/api/customer/account</b>. The backend looks up the "
            "currently authenticated user from the JWT, finds the account in MySQL, maps it into an "
            "<b>AccountSummaryDto</b>, and returns it to the frontend."
        )
    )

    story.append(p("How security works inside the lifecycle:", "Subsection"))
    story.append(
        p(
            "Security happens <b>before</b> business logic. The JWT filter checks whether the request has a valid token. "
            "If the token is invalid or missing, the request should never reach the protected controller logic."
        )
    )
    story.append(
        code(
            "Browser request with JWT\n"
            "   -> JwtAuthenticationFilter\n"
            "   -> extract username from token\n"
            "   -> load user details\n"
            "   -> validate token\n"
            "   -> put authentication into SecurityContext\n"
            "   -> allow request to continue"
        )
    )

    story.append(p("How database interaction works:", "Subsection"))
    story.append(
        p(
            "The service layer never writes raw SQL in controllers. Instead, it calls repository methods such as "
            "findByEmail(), findByUser(), or save(). Spring Data JPA converts those into SQL operations under the hood."
        )
    )
    story.append(
        p(
            "This is useful because the business logic stays readable. For example, transfer logic can focus on "
            "checking balance, updating account balance, storing the transaction, and writing a fraud log."
        )
    )

    story.append(p("Why the response uses DTOs:", "Subsection"))
    story.append(
        p(
            "DTOs are safer than returning entities directly. They let us choose exactly which fields go to the client. "
            "For example, we never want to return hashed passwords, internal flags, or unnecessary relational data."
        )
    )

    story.append(p("Interview explanation example:", "Subsection"))
    story.append(
        p(
            "“The request first enters the controller, then the service handles business rules, then the repository "
            "communicates with the database. After data is retrieved, the backend returns a DTO as JSON to the React "
            "frontend. This keeps the flow secure, testable, and maintainable.”"
        )
    )
    story.append(
        p(
            "Mentor note: if you can clearly explain this flow, you will sound much stronger in a viva than someone "
            "who only describes screens."
        ,
            "Callout",
        )
    )

    story.append(Spacer(1, 12))
    story.append(p("Next Topics Preview", "Section"))
    story.append(
        p(
            "The next teaching pack should cover JWT flow visually, Spring Security configuration, annotations, module "
            "breakdown, transfer internals, fraud detection, and financial health score logic."
        )
    )
    story.append(
        p(
            "Use this line when presenting: “I can now walk you through how authentication, authorization, and secure "
            "money transfer are implemented step by step.”"
        )
    )

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawRightString(195 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_pdf()
