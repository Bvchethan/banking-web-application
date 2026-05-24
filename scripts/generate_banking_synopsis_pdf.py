from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak


OUTPUT = Path("output/pdf/banking-project-synopsis.pdf")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="SynopsisTitle",
        parent=styles["Title"],
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="HeadingCenter",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyJustify",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=12,
        leading=18,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCenter",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)


def p(text, style="BodyJustify"):
    return Paragraph(text, styles[style])


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=25 * mm,
        bottomMargin=25 * mm,
    )

    story = []

    story.append(Spacer(1, 10))
    story.append(p("Project Synopsis", "SynopsisTitle"))
    story.append(Spacer(1, 6))
    story.append(p("Title", "HeadingCenter"))
    story.append(
        p(
            "AI-Driven Secure Digital Banking Web Application Using React, Spring Boot, JWT Authentication, and MySQL",
            "BodyCenter",
        )
    )
    story.append(Spacer(1, 12))

    details = [
        ["Name", "______________________________"],
        ["USN", "______________________________"],
        ["Elective", "Computer Science and Information Technology"],
        ["Date of Submission", "______________________________"],
    ]
    details_table = Table(details, colWidths=[55 * mm, 95 * mm])
    details_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("LEADING", (0, 0), (-1, -1), 18),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 16))

    sections = [
        (
            "Problem Statement:",
            "The rapid digitization of banking services has made convenience and accessibility a major expectation for customers. "
            "However, many existing small and mid-scale digital banking systems still suffer from fragmented workflows, weak role-based security, "
            "limited transaction transparency, and poor monitoring of suspicious fund transfers. Customers often face difficulty in managing beneficiaries, "
            "tracking transaction history, reviewing account insights, and securely transferring money through a unified platform. On the administrative side, "
            "many systems do not provide centralized visibility into customer activity, suspicious transactions, or operational analytics needed for secure supervision.",
        ),
        (
            "",
            "This project proposes to develop a full-stack secure digital banking web application that supports customer and admin roles within a single responsive platform. "
            "The system will be built using React for the frontend, Spring Boot for the backend, Spring Security with JWT for authentication and authorization, "
            "Spring Data JPA for persistence, and MySQL as the relational database. The proposed application will provide registration, login, account management, "
            "beneficiary management, transaction history, secure money transfer, fraud analytics, and financial health insights. The study will emphasize security, "
            "transaction consistency, role-based access control, and user-centric financial visibility in modern banking software.",
        ),
        (
            "Objectives of the Project:",
            "Objective 1: To develop a role-based banking platform that enables customers to manage their profiles, beneficiaries, account balances, and transfers, "
            "while allowing administrators to monitor customers and transactions through a centralized dashboard.",
        ),
        (
            "",
            "Objective 2: To implement secure authentication and authorization using JWT, BCrypt password encryption, and Spring Security so that only valid users can access protected banking operations.",
        ),
        (
            "",
            "Objective 3: To ensure reliable transaction management by updating sender and receiver balances atomically and maintaining complete transaction records for both accounts.",
        ),
        (
            "",
            "Objective 4: To incorporate an AI-inspired fraud detection mechanism and a financial health scoring module that provide intelligent insights over customer transaction behavior.",
        ),
        (
            "Project Methodology:",
            "Type of Project: Application-based. The proposed system will be a deployable full-stack web application rather than a theoretical study. "
            "The project will cover practical software engineering activities such as requirement analysis, database design, backend development, frontend integration, testing, and deployment preparation.",
        ),
        (
            "",
            "Technology Stack: The frontend will be developed using React, Tailwind CSS, Axios, and React Router. The backend will be developed using Java Spring Boot, "
            "Spring Security, JWT, Spring Data JPA, and Maven. MySQL will be used as the normalized relational database for storing users, roles, accounts, beneficiaries, transactions, and fraud logs.",
        ),
        (
            "",
            "System Architecture: The project follows a layered client-server architecture. The frontend operates as a Single Page Application and communicates with the backend through REST APIs. "
            "The backend is structured into controller, service, repository, dto, entity, config, security, and exception packages to ensure maintainability, separation of concerns, and enterprise-style code organization.",
        ),
        (
            "",
            "Data Collection Methods: Secondary data will be used to understand digital banking workflows, security expectations, and transaction monitoring requirements from existing online banking systems. "
            "Primary data will be simulated through user actions such as login, profile updates, beneficiary creation, transfers, and transaction reviews, which will inform API design and database structure.",
        ),
    ]

    for heading, body in sections:
        if heading:
            story.append(p(heading, "BodyJustify"))
        story.append(p(body))

    story.append(p("Key Modules to be Developed:", "BodyJustify"))
    key_modules = [
        "User Management: Customer and admin registration, login, JWT-based authentication, password encryption, and role-based access control will be implemented to secure the application.",
        "Profile and Account Management: Customers will be able to view and update their personal details, access account summaries, and monitor available balances.",
        "Beneficiary Management: Customers will be able to add, edit, and delete trusted beneficiaries for future transfers.",
        "Secure Transfer Management: The application will support account-to-account money transfer with atomic balance updates, debit and credit transaction creation, and transaction history visibility for both sender and receiver.",
        "Transaction Monitoring: Customers will be able to search and review transaction histories, while administrators will be able to inspect all transactions through centralized reporting interfaces.",
        "Fraud Analytics: The system will evaluate risky transfers using rule-based fraud detection factors such as high amount, multiple rapid transfers, and newly added beneficiaries, then classify transactions into LOW, MEDIUM, or HIGH risk.",
        "Financial Health Insights: The application will generate monthly financial health scores, savings trends, and smart suggestions using customer spending and credit-debit behavior.",
        "Administrative Dashboard: The administrator will be able to view customer records, total transactions, high-risk transfer counts, and platform-level monitoring summaries.",
    ]
    for item in key_modules:
        story.append(p(item))

    story.append(p("Development Methodology:", "BodyJustify"))
    story.append(
        p(
            "An Agile iterative development approach will be followed throughout the project. The implementation will be divided into logical phases such as authentication, core banking modules, transfer processing, "
            "analytics, and final integration. Git-based version control will be used to manage source code changes. Functional testing, API verification, exception handling review, and UI validation will be performed throughout the development lifecycle to improve reliability and usability."
        )
    )

    story.append(p("Limitation:", "BodyJustify"))
    limitations = [
        "The current project scope will be limited to a web application and will not include native Android or iOS mobile applications.",
        "The fraud detection system will be rule-based and AI-inspired rather than a full machine learning model trained on real banking datasets.",
        "The platform will simulate internal banking transfers within the managed system and will not integrate with external inter-bank payment rails in this phase.",
        "Advanced production infrastructure features such as distributed deployment, load balancing, high availability clustering, and cloud-native scaling will remain outside the present implementation scope.",
        "The application will require an active internet connection and will not provide offline banking capabilities in this phase.",
        "Formal penetration testing, regulatory compliance certification, and large-scale banking-grade audit integration will not be fully covered within the academic project scope.",
    ]
    for item in limitations:
        story.append(p(item))

    story.append(PageBreak())
    story.append(p("Work Plan (Week 1 to Week 8)", "HeadingCenter"))
    story.append(Spacer(1, 6))

    work_plan_data = [
        ["Week No.", "Activities to be Completed"],
        [
            "Week 1",
            "Conduct requirement analysis of digital banking workflows and finalize the project scope, user roles, and technology stack. Prepare initial project structure and repository setup.",
        ],
        [
            "Week 2",
            "Design the MySQL database schema for users, roles, accounts, beneficiaries, transactions, and fraud logs. Define REST API routes and layered backend package structure.",
        ],
        [
            "Week 3",
            "Implement Spring Boot backend configuration, entity relationships, repositories, and user authentication modules. Develop registration, login, JWT generation, and role-based authorization.",
        ],
        [
            "Week 4",
            "Develop customer modules including profile management, account summary, beneficiary management, and transaction history APIs. Add input validation and exception handling.",
        ],
        [
            "Week 5",
            "Implement secure money transfer logic with atomic account updates, sender-receiver transaction recording, and fraud log generation. Start admin monitoring modules.",
        ],
        [
            "Week 6",
            "Develop the React frontend pages including login, registration, customer dashboard, admin dashboard, transfer money, profile, transaction history, and beneficiary management.",
        ],
        [
            "Week 7",
            "Integrate frontend and backend using Axios and protected routes. Implement fraud analytics and financial health score visual modules. Improve responsive design and search functionality.",
        ],
        [
            "Week 8",
            "Perform functional testing, debugging, schema validation, and final project documentation. Prepare project report, synopsis, and presentation materials for submission and viva.",
        ],
    ]

    work_table = Table(work_plan_data, colWidths=[28 * mm, 122 * mm])
    work_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("LEADING", (0, 0), (-1, -1), 18),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(work_table)

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Times-Roman", 12)
        page_width, _ = A4
        canvas.drawCentredString(page_width / 2, 12 * mm, str(doc_obj.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    build_pdf()
