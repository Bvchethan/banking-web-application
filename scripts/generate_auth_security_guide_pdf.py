from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak


OUTPUT = Path("output/pdf/banking-architecture-guide-part-2.pdf")
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
        fontSize=9.4,
        leading=13,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#e2e8f0"),
        borderPadding=8,
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
    story.append(p("Part 2: Authentication, JWT, Spring Security, and Core Backend Annotations"))
    story.append(
        p(
            "This part focuses on the security heart of the project. If you can explain this clearly, you will sound "
            "like someone who understands not just coding, but safe system design."
        )
    )
    story.append(Spacer(1, 8))

    story.append(p("1. Authentication Module Overview", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> The authentication module proves who the user is. In this project, it handles "
            "registration, login, password encryption, token generation, and identity retrieval for future requests."
        )
    )
    story.append(
        p(
            "<b>Main classes involved:</b> <b>AuthController</b>, <b>AuthService</b>, <b>CustomUserDetailsService</b>, "
            "<b>JwtService</b>, <b>JwtAuthenticationFilter</b>, and <b>SecurityConfig</b>."
        )
    )
    story.append(p("Module interaction diagram:", "Subsection"))
    story.append(
        code(
            "Login Request\n"
            "   -> AuthController\n"
            "   -> AuthService\n"
            "   -> AuthenticationManager\n"
            "   -> CustomUserDetailsService\n"
            "   -> UserRepository / MySQL\n"
            "   -> JwtService generates token\n"
            "   -> JSON response back to React"
        )
    )
    story.append(
        p(
            "<b>Why this code is written this way:</b> login should not be handled by one giant class. We separate HTTP "
            "entry, business logic, token generation, and user lookup so each piece has one clear responsibility."
        )
    )
    story.append(
        p(
            "<b>Viva line:</b> “Authentication is split into controller, service, and security components so that user "
            "verification, password checking, and token generation stay modular and maintainable.”"
        )
    )
    story.append(
        p(
            "Mentor note: in interviews, always separate <b>authentication</b> from <b>authorization</b>. "
            "Authentication answers ‘who are you?’ Authorization answers ‘what are you allowed to do?’",
            "Callout",
        )
    )

    story.append(PageBreak())

    story.append(p("2. JWT Flow Visually", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> JWT allows stateless authentication. After login, the server does not need to store a "
            "session in memory. Instead, the client sends the token with each request."
        )
    )
    story.append(p("Simple JWT lifecycle:", "Subsection"))
    story.append(
        code(
            "1. User logs in with email + password\n"
            "2. Backend verifies credentials\n"
            "3. Backend generates JWT token\n"
            "4. Frontend stores token\n"
            "5. Frontend sends token in Authorization header\n"
            "6. Backend validates token on each protected request\n"
            "7. Backend allows or rejects access"
        )
    )
    story.append(p("Visual flow diagram:", "Subsection"))
    story.append(
        code(
            "React Login Page\n"
            "   |\n"
            "   | POST /api/auth/login\n"
            "   v\n"
            "Spring Boot\n"
            "   |\n"
            "   | validate username/password\n"
            "   | create JWT\n"
            "   v\n"
            "React stores JWT\n"
            "   |\n"
            "   | GET /api/customer/account\n"
            "   | Authorization: Bearer <token>\n"
            "   v\n"
            "JwtAuthenticationFilter\n"
            "   |\n"
            "   | token valid? -> yes\n"
            "   v\n"
            "Controller / Service / DB\n"
            "   |\n"
            "   v\n"
            "JSON Response"
        )
    )
    story.append(
        p(
            "<b>Why JWT is useful here:</b> It works well for REST APIs, React frontends, and role-based access. "
            "It also scales better than tightly coupled server sessions."
        )
    )
    story.append(
        p(
            "<b>Security flow:</b> the JWT contains the username and role claims. The backend verifies the signature "
            "before trusting any token data. If the signature is invalid or the token is expired, access is denied."
        )
    )
    story.append(
        p(
            "<b>Frontend-backend communication:</b> Axios automatically attaches the JWT from local storage in the "
            "Authorization header. This keeps protected API calls consistent across pages."
        )
    )
    story.append(
        p(
            "<b>Database interaction:</b> the token itself is not stored in MySQL in this version. Instead, once a "
            "token is validated, the user is loaded again from the database using email. That ensures current user "
            "status and roles remain trusted from server-side data."
        )
    )

    story.append(PageBreak())

    story.append(p("3. Spring Security Configuration, Explained Simply", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> Spring Security protects the application before requests reach business logic. "
            "It defines which endpoints are public, which require login, and which roles can access them."
        )
    )
    story.append(p("Mental model:", "Subsection"))
    story.append(
        code(
            "Public endpoints:\n"
            "  /api/auth/**\n"
            "\n"
            "Admin only endpoints:\n"
            "  /api/admin/**\n"
            "\n"
            "Customer or Admin endpoints:\n"
            "  /api/customer/**"
        )
    )
    story.append(
        p(
            "In <b>SecurityConfig</b>, we disable CSRF for this stateless REST API, enable CORS for the React app, "
            "set the session policy to <b>STATELESS</b>, define authorization rules, and insert the JWT filter before "
            "the normal username-password authentication filter."
        )
    )
    story.append(p("Simple filter chain idea:", "Subsection"))
    story.append(
        code(
            "HTTP Request\n"
            "   -> CORS check\n"
            "   -> JWT filter\n"
            "   -> role check\n"
            "   -> controller method\n"
            "   -> response"
        )
    )
    story.append(
        p(
            "<b>Why written this way:</b> placing JWT validation in a filter means every protected request is checked "
            "centrally instead of repeating token logic in every controller."
        )
    )
    story.append(
        p(
            "<b>Viva line:</b> “Spring Security is configured as a stateless API security layer. Public authentication "
            "routes are open, while customer and admin APIs are protected by role-based authorization rules.”"
        )
    )
    story.append(
        p(
            "Mentor note: if someone asks why sessions are disabled, say because JWT-based APIs are stateless and do not "
            "rely on server-side session tracking.", "Callout"
        )
    )

    story.append(PageBreak())

    story.append(p("4. Important Spring Annotations You Should Explain in Viva", "Section"))
    story.append(
        p(
            "<b>Purpose:</b> Annotations tell Spring how to wire the application. A junior developer should not just "
            "memorize them, but understand what each one does in the architecture."
        )
    )

    annotation_rows = [
        ["Annotation", "Meaning", "Where used in this project"],
        ["@SpringBootApplication", "Main boot entry point", "BankingApplication.java"],
        ["@RestController", "Class returns JSON responses", "AuthController, CustomerController, AdminController"],
        ["@RequestMapping", "Base URL path mapping", "API route grouping"],
        ["@GetMapping / @PostMapping / @PutMapping / @DeleteMapping", "HTTP method mapping", "REST endpoints"],
        ["@Service", "Business logic bean", "Transfer, auth, fraud, admin services"],
        ["@Repository", "Persistence component", "JPA repositories"],
        ["@Entity", "Maps class to database table", "User, Account, Transaction, FraudLog"],
        ["@Table", "Customizes table name", "All entity classes"],
        ["@Id / @GeneratedValue", "Primary key mapping", "Entity identifiers"],
        ["@ManyToOne / @OneToOne / @ManyToMany", "Relationship mapping", "User-account-role-transaction relations"],
        ["@Valid", "Triggers validation on request DTOs", "Register, login, transfer, profile update"],
        ["@Transactional", "Run logic safely as one DB transaction", "Register and transfer logic"],
        ["@EnableMethodSecurity", "Enables method-level security support", "SecurityConfig"],
        ["@RequiredArgsConstructor", "Generates constructor injection", "Services and controllers"],
    ]
    table = Table(annotation_rows, colWidths=[40 * mm, 55 * mm, 75 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))
    story.append(
        p(
            "<b>Why these matter:</b> Annotations reduce boilerplate, make the code declarative, and clearly communicate "
            "developer intent. In enterprise Java, being able to explain annotations is a big signal of competence."
        )
    )

    story.append(PageBreak())

    story.append(p("5. Security Flow Module by Module", "Section"))
    story.append(p("AuthController", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> receives login and registration HTTP requests.<br/>"
            "<b>Request flow:</b> validates JSON input, forwards it to AuthService, returns token response.<br/>"
            "<b>Why written this way:</b> controllers should stay thin and not contain password or token logic."
        )
    )

    story.append(p("AuthService", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> handles registration and login business logic.<br/>"
            "<b>Security flow:</b> encrypts passwords with BCrypt, authenticates credentials through Spring Security, "
            "and creates JWT tokens.<br/>"
            "<b>Database interaction:</b> saves new users and accounts, checks duplicate email and phone, loads users "
            "during login."
        )
    )

    story.append(p("CustomUserDetailsService", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> adapts our database user into Spring Security's expected format.<br/>"
            "<b>Why written this way:</b> Spring Security wants a <b>UserDetails</b> object, but our app stores "
            "users in MySQL. This class bridges that gap."
        )
    )

    story.append(p("JwtService", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> generates, parses, and validates JWTs.<br/>"
            "<b>Security flow:</b> adds subject, roles, issue time, and expiration, then signs the token using the "
            "secret key."
        )
    )

    story.append(p("JwtAuthenticationFilter", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> intercepts each request and checks the Authorization header.<br/>"
            "<b>Security flow:</b> extracts token, reads username, loads user details, validates token, and sets the "
            "authenticated principal in Spring Security's context."
        )
    )

    story.append(p("SecurityConfig", "Subsection"))
    story.append(
        p(
            "<b>Purpose:</b> defines the global rules for API protection.<br/>"
            "<b>Frontend-backend communication:</b> also configures CORS so the React app on localhost:5173 can call "
            "the backend safely from a different origin."
        )
    )
    story.append(
        p(
            "Mentor note: this module-by-module explanation is exactly the style examiners like, because it proves you "
            "understand the role of each class, not just the final outcome.", "Callout"
        )
    )

    story.append(PageBreak())

    story.append(p("6. How Login and Protected Requests Work End to End", "Section"))
    story.append(p("Login flow example", "Subsection"))
    story.append(
        code(
            "Frontend LoginPage submits email + password\n"
            "   -> Axios POST /api/auth/login\n"
            "   -> AuthController.login()\n"
            "   -> AuthService.login()\n"
            "   -> AuthenticationManager.authenticate()\n"
            "   -> CustomUserDetailsService loads user from MySQL\n"
            "   -> Password check succeeds\n"
            "   -> JwtService.generateToken()\n"
            "   -> token returned to React\n"
            "   -> React stores token and redirects user"
        )
    )
    story.append(p("Protected API example", "Subsection"))
    story.append(
        code(
            "CustomerDashboardPage loads\n"
            "   -> Axios GET /api/customer/account\n"
            "   -> Authorization header contains JWT\n"
            "   -> JwtAuthenticationFilter validates JWT\n"
            "   -> SecurityContext gets authenticated user\n"
            "   -> CustomerController.account()\n"
            "   -> AccountService.getAccountSummary()\n"
            "   -> AccountRepository.findByUser()\n"
            "   -> MySQL returns account\n"
            "   -> DTO returned as JSON\n"
            "   -> React displays account balance"
        )
    )
    story.append(
        p(
            "<b>Why protected routes matter:</b> without this flow, any user could call admin or customer APIs directly. "
            "Security must be enforced on the backend, not just hidden in the UI."
        )
    )

    story.append(p("7. Common Viva Questions and Smart Answers", "Section"))
    qa_rows = [
        ["Question", "Strong short answer"],
        ["Why use BCrypt?", "Because passwords must never be stored in plain text. BCrypt hashes them securely."],
        ["Why use DTOs in auth responses?", "To return only required fields like token, name, email, and roles."],
        ["Why use JWT instead of sessions?", "JWT supports stateless REST APIs and works cleanly with React clients."],
        ["Why reload the user from DB during validation?", "Because the server should trust current database roles and status, not only token content."],
        ["Why is role-based access important?", "Because admin and customer features must be isolated to prevent privilege abuse."],
    ]
    qa_table = Table(qa_rows, colWidths=[70 * mm, 100 * mm])
    qa_table.setStyle(
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
    story.append(qa_table)
    story.append(Spacer(1, 8))
    story.append(
        p(
            "Next, the best continuation is the business module pack: customer module, admin module, transfer logic, "
            "transaction internals, and money protection rules."
        )
    )
    story.append(
        p(
            "Use this transition line in a presentation: “Now that I have explained how the system authenticates and "
            "authorizes users, I can explain how the banking operations themselves are executed safely.”"
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
