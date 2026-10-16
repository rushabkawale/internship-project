import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def add_page_borders(section):
    sectPr = section._sectPr
    pgBorders = parse_xml(
        r'<w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:offsetFrom="page">'
        r'<w:top w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
        r'<w:left w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
        r'<w:bottom w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
        r'<w:right w:val="single" w:sz="12" w:space="24" w:color="000000"/>'
        r'</w:pgBorders>'
    )
    sectPr.append(pgBorders)

def create_report():
    doc = Document()
    
    # Configure Section & Margins
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4 width
    section.page_height = Inches(11.69) # A4 height
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    
    # Add page border to section
    add_page_borders(section)
    
    # Base Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(6)

    def add_title(text, space_before=10, space_after=20):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_after=8):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        return p

    def add_bullet(text, level=0, space_after=4):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.left_indent = Inches(0.3 * (level + 1))
        run = p.add_run(text)
        run.font.size = Pt(11.5)
        return p

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(25)
    p_logo.paragraph_format.space_after = Pt(25)
    run_badge = p_logo.add_run("🎓\n[ INSTITUTION EMBLEM / LOGO ]")
    run_badge.bold = True
    run_badge.font.size = Pt(13)
    run_badge.font.color.rgb = RGBColor(100, 116, 139)

    add_title("ON-THE-JOB TRAINING REPORT", space_before=15, space_after=18)
    
    add_para("SUBMITTED TO", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=12)
    add_para("SHIVAJI UNIVERSITY, KOLHAPUR", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=16)
    
    add_para("FOR THE PARTIAL FULFILLMENT OF THE DEGREE OF", align=WD_ALIGN_PARAGRAPH.CENTER, size=11, space_after=10)
    add_para("BCA-III SEM-V (2026-2027)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=28)
    
    add_para("SUBMITTED BY", align=WD_ALIGN_PARAGRAPH.CENTER, size=11, space_after=10)
    add_para("VIVEK BANDU LAVHATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=8)
    add_para("PRN No.: 2024079264", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=32)
    
    add_para("DEPARTMENT OF COMPUTER APPLICATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=8)
    add_para("GOPAL KRUSHANA GOKHALE COLLEGE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=10)
    add_para("Academic Year: 2026-2027", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=10)
    
    doc.add_page_break()

    # =========================================================================
    # PAGE 2: JOINING LETTER
    # =========================================================================
    add_title("JOINING LETTER", space_before=10, space_after=18)
    
    add_para("Axelyne LLP\nLLPIN: ACV-0266 | Email: sales@axelyne.com | Phone: +91 9623922545", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    p_line = doc.add_paragraph()
    p_line.paragraph_format.space_after = Pt(14)
    run_l = p_line.add_run("_________________________________________________________________________________")
    run_l.font.color.rgb = RGBColor(148, 163, 184)
    
    add_para("Ref: AXELYNE/HRD/OJT/0564                                                      Date: 06 October 2026", bold=True, size=10.5, space_after=14)
    add_para("To,\nMr./Ms. Vivek Bandu Lavhate", bold=True, size=11.5, space_after=12)
    add_para("Subject: Joining Confirmation for Two-Month (60 Hours) Internship Program", bold=True, size=11.5, space_after=14)
    
    add_para("Dear Mr./Ms. Vivek Bandu Lavhate,")
    add_para("We are pleased to confirm that you have joined Axelyne LLP, as a Software Development Intern under our Two-Month Internship Program, effective from 03 August 2026.")
    add_para("During your internship, you will be engaged in practical training, hands-on learning, and project-based activities related to software development. You are expected to participate regularly, complete the assigned tasks and projects, and follow the instructions, policies, and professional standards of the organization.")
    add_para("This internship is intended to provide you with practical industry exposure and hands-on experience in a professional work environment. Completion of the internship will be subject to satisfactory attendance, participation, task/project completion, and adherence to organizational guidelines.")
    add_para("You are required to maintain the confidentiality of all company information, project-related information, data, and other proprietary materials accessed during the internship.")
    add_para("We welcome you to Axelyne LLP and wish you a successful and enriching internship experience.")
    
    add_para("\nMrs. Archana Sachin Nigade\nDirector, Axelyne LLP\n[Seal & Signature: Axelyne LLP, Pune]", bold=True, size=11, space_after=10)
    add_para("Address: SNO.19A/2A/2B, Office B/317, 3rd Floor, Rajdhani Complex, Near Shankar Maharaj Math, Pune-Satara Road, Pune - 411043, Maharashtra, India", align=WD_ALIGN_PARAGRAPH.CENTER, size=9, italic=True)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: COMPLETION CERTIFICATE
    # =========================================================================
    add_title("ON-THE-JOB TRAINING COMPLETION CERTIFICATE", space_before=10, space_after=18)
    
    add_para("Axelyne LLP\nLLPIN: ACV-0266 | Email: sales@axelyne.com | Phone: +91 9623922545", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    p_line2 = doc.add_paragraph()
    p_line2.paragraph_format.space_after = Pt(14)
    run_l2 = p_line2.add_run("_________________________________________________________________________________")
    run_l2.font.color.rgb = RGBColor(148, 163, 184)
    
    add_title("CERTIFICATE OF COMPLETION", space_before=10, space_after=14)
    add_para("AXELYNE/HRD/OJT/0564                                                           Date: 06 October 2026", bold=True, size=10.5, space_after=16)
    
    add_para("This is to certify that", italic=True)
    add_para("Mr./Ms. Vivek Bandu Lavhate", bold=True, size=13, space_after=12)
    add_para("a student has successfully completed the internship program at Axelyne LLP as Software Development Intern, 03 August 2026 to 03 October 2026.")
    add_para("During this period, the intern demonstrated consistent dedication and professionalism, and has successfully fulfilled all requirements of the program, including assignments, project work on the CraveHub Full-Stack Food Delivery Platform, and the final presentation.")
    add_para("We wish Vivek Bandu Lavhate continued success in all future endeavors.")
    
    add_para("\n\nMrs. Archana Sachin Nigade\nDirector, Axelyne LLP\n[Authorized Seal & Signature]", bold=True, size=11.5, space_after=14)
    add_para("Address: SNO.19A/2A/2B, Office B/317, 3rd Floor, Rajdhani Complex, Near Shankar Maharaj Math, Pune-Satara Road, Pune - 411043, Maharashtra, India", align=WD_ALIGN_PARAGRAPH.CENTER, size=9, italic=True)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: COLLEGE CERTIFICATE
    # =========================================================================
    add_title("CERTIFICATE", space_before=25, space_after=25)
    
    add_para("This is to certify that the On-the-Job Training report submitted herewith for partial fulfilment of the BCA degree as laid down by Shivaji University, Kolhapur, is the original work completed at this college by Vivek Bandu Lavhate under our supervision and guidance, and, to the best of our knowledge, has not been submitted to any other university or examining body.", space_after=25)
    
    add_para("Place: Kolhapur\n\nDate: ____________", bold=True, space_after=65)
    
    # Signature row
    table_sig = doc.add_table(rows=1, cols=2)
    table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sig.rows[0].cells[0].paragraphs[0].text = "_____________________\nExaminer"
    table_sig.rows[0].cells[0].paragraphs[0].runs[0].bold = True
    table_sig.rows[0].cells[1].paragraphs[0].text = "_____________________\nCo-Ordinator"
    table_sig.rows[0].cells[1].paragraphs[0].runs[0].bold = True
    table_sig.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: DECLARATION
    # =========================================================================
    add_title("DECLARATION", space_before=15, space_after=20)
    
    add_para("I hereby declare that the On-the-Job Training (OJT) report entitled “CraveHub: Full-Stack Gourmet Food Delivery Platform & Kitchen Management System” is a record of the training completed by me at Axelyne LLP during the period from 03 Aug 2026 to 03 Oct 2026.")
    add_para("The work presented in this report is based on my learning, practical experience, and activities carried out during the training period. This report has been prepared by me as a part of the academic requirements of the BCA programme.")
    add_para("I further declare that the information presented in this report is true and correct to the best of my knowledge.")
    
    add_para("\nPlace: _______________", bold=True)
    add_para("Date: _______________", bold=True, space_after=20)
    add_para("Name of Student: Vivek Bandu Lavhate", bold=True)
    add_para("PRN No.: 2024079264", bold=True)
    add_para("Signature of Student: ___________________________", bold=True, space_after=15)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: ACKNOWLEDGEMENT
    # =========================================================================
    add_title("ACKNOWLEDGEMENT", space_before=15, space_after=20)
    
    add_para("I would like to express my sincere gratitude to Axelyne LLP for providing me with the opportunity to complete my On-the-Job Training (OJT).")
    add_para("I am thankful to my industry supervisor, Ms. Archana Sachin Nigade for valuable guidance, support, and encouragement throughout the training period. The practical knowledge and professional experience gained during this training have helped me to enhance my technical skills and understand the working environment of the industry.")
    add_para("I express my heartfelt thanks to the Principal, Head of the Department, OJT Coordinator, and all faculty members of Gopal Krushana Gokhale College / The New College Kolhapur for their guidance and support in successfully completing this training.")
    add_para("Finally, I would like to thank everyone who directly or indirectly contributed to the successful completion of my On-the-Job Training.")
    
    add_para("\nName of Student: Vivek Bandu Lavhate", bold=True)
    add_para("PRN No.: 2024079264", bold=True)
    add_para("Class: BCA-III", bold=True)
    add_para("Academic Year: 2026-27", bold=True, space_after=15)

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: INDEX
    # =========================================================================
    add_title("INDEX", space_before=10, space_after=15)
    
    index_items = [
        ("1", "Student Information", "8"),
        ("2", "Introduction to CraveHub Project", "9"),
        ("3", "Objectives of Training", "10"),
        ("4", "Company Profile (Axelyne LLP)", "11"),
        ("5", "Training Details and Activities (Modules 1-4)", "12"),
        ("6", "Technologies and Tools Used", "14"),
        ("7", "Task Undertaken & System Architecture", "15"),
        ("8", "System Design: Entity Relationship Diagram (ERD)", "16"),
        ("9", "System Design: Data Flow Diagrams (DFD Level 0 & 1)", "17"),
        ("10", "Results & Application Snapshots", "18"),
        ("11", "Skills & Knowledge Acquired", "21"),
        ("12", "Learning Experience & Professional Reflection", "22"),
        ("13", "Conclusion", "23")
    ]
    
    t_idx = doc.add_table(rows=len(index_items) + 1, cols=3)
    t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = t_idx.rows[0].cells
    hdr_cells[0].text = "Sr. No"
    hdr_cells[1].text = "Contents"
    hdr_cells[2].text = "Page No."
    for cell in hdr_cells:
        set_cell_background(cell, "DCEBF8")
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, (sr, title, pg) in enumerate(index_items):
        row_cells = t_idx.rows[r_idx + 1].cells
        row_cells[0].text = sr
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[1].text = title
        row_cells[2].text = pg
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for c in row_cells:
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: STUDENT INFORMATION
    # =========================================================================
    add_title("STUDENT INFORMATION", space_before=15, space_after=18)
    
    info_data = [
        ("Name of Student", "Vivek Bandu Lavhate"),
        ("Class", "BCA-III"),
        ("PRN", "2024079264"),
        ("Name of Company", "Axelyne LLP"),
        ("Company Address", "Office No. B/317, 3rd Floor, Rajdhani Complex, Near Shankar Maharaj Math, Pune-Satara Road, Dhankawadi, Pune - 411043, Maharashtra, India"),
        ("Training Domain", "Full-Stack Web & Software Engineering Intern"),
        ("Training Duration", "From 03 Aug 2026 to 03 Oct 2026"),
        ("Industry Supervisor", "Archana Nigade"),
        ("Faculty Guide", "________________________")
    ]
    
    t_info = doc.add_table(rows=len(info_data) + 1, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_info.rows[0].cells[0].text = "Particulars"
    t_info.rows[0].cells[1].text = "Details"
    for c in t_info.rows[0].cells:
        set_cell_background(c, "DCEBF8")
        set_cell_margins(c, top=140, bottom=140, left=150, right=150)
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, (part, val) in enumerate(info_data):
        r_cells = t_info.rows[r_idx + 1].cells
        r_cells[0].text = part
        r_cells[0].paragraphs[0].runs[0].bold = True
        r_cells[1].text = val
        for c in r_cells:
            set_cell_margins(c, top=110, bottom=110, left=150, right=150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: INTRODUCTION
    # =========================================================================
    add_title("INTRODUCTION", space_before=15, space_after=18)
    
    add_para("On-the-Job Training (OJT) is an essential practical curriculum component of the Bachelor of Computer Applications (BCA). It provides students with an invaluable opportunity to bridge academic concepts with real-world professional software engineering methodologies. OJT enables students to gain practical exposure to modern programming frameworks, software architecture, RESTful API integrations, relational databases, agile team workflows, and version control systems.")
    add_para("I completed my On-the-Job Training at Axelyne LLP for a duration of 2 months, from 03 Aug 2026 to 03 Oct 2026. During this internship, I was assigned to develop a complete full-stack web application titled “CraveHub: Gourmet Food Delivery & Kitchen Management Platform”.")
    add_para("CraveHub is designed to solve real-world challenges in the restaurant and food logistics industry. It connects four major stakeholders in an interconnected workflow: Customers (who discover dishes, manage carts, make UPI payments, and track live status), Kitchen Staff (who manage kitchen preparation orders on an interactive KDS board), Delivery Executives (who complete handovers using a secure 4-digit customer verification OTP), and Administrators (who monitor live business revenue trends, top-selling dishes, and dispatch logistics).")
    add_para("The training provided me with comprehensive hands-on knowledge in Python programming, Flask REST API microservices, Streamlit reactive web framework, MySQL / SQLite relational database modeling, CSS custom design tokens, Git/GitHub version control, and multi-user authentication. This experience reinforced the importance of writing clean, modular, and maintainable software code.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: OBJECTIVES OF TRAINING
    # =========================================================================
    add_title("OBJECTIVES OF TRAINING", space_before=15, space_after=18)
    
    objs = [
        "To gain hands-on practical experience in computer science principles through live software engineering tasks at Axelyne LLP.",
        "To understand how professional IT companies plan, architect, implement, test, and deploy multi-tier software applications.",
        "To master front-end and back-end web development using Python, Flask REST API endpoints, Streamlit, and modern CSS design tokens.",
        "To design, implement, and optimize relational database models using SQLite and MySQL, executing comprehensive CRUD operations.",
        "To implement robust multi-role Authentication and Authorization (Customer, Admin, Kitchen, and Delivery Partner).",
        "To integrate digital payment workflows including UPI intent generation, deep-links, and transaction verification.",
        "To design real-world operational workflows such as Kitchen Display Systems (KDS) and OTP-verified delivery handovers.",
        "To utilize professional development tools including Visual Studio Code, Git, GitHub, and Postman.",
        "To improve software debugging, problem-solving, code documentation, and time management in an industry setting."
    ]
    for o in objs:
        add_bullet(o, space_after=8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: COMPANY PROFILE
    # =========================================================================
    add_title("COMPANY PROFILE", space_before=15, space_after=18)
    
    add_para("Name of the Company: Axelyne LLP", bold=True, size=13, space_after=12)
    add_para("About the Company:", bold=True, size=12, space_after=6)
    add_para("Axelyne LLP is a technology-driven software development and digital solutions company headquartered in Pune, Maharashtra. It delivers innovative, scalable, and business-focused solutions in custom enterprise software development, web and mobile applications, cloud engineering, AI-powered systems, and digital marketing. The company collaborates with fast-growing startups, SMEs, educational institutions, and corporate enterprises.")
    add_para("Axelyne has a dedicated team of 22+ software professionals, including full-stack engineers, cloud architects, mobile developers, UI/UX designers, QA automation testers, and technical project mentors. It has successfully engineered over 40+ software solutions spanning healthcare, education, retail, logistics, agriculture, and hospitality.")
    add_para("Core Services:", bold=True, size=11.5, space_after=4)
    add_bullet("Custom Web and Enterprise Software Development")
    add_bullet("Mobile Application Engineering (Android, iOS & Flutter)")
    add_bullet("Cloud Solutions and RESTful API Architecture")
    add_bullet("AI / Machine Learning and Data Analytics Services")
    add_bullet("UI/UX Prototyping and Performance Optimization")
    add_bullet("Software Quality Assurance, Deployment and Maintenance Support")
    add_para("Technologies Deployed: Python, Java, Spring Boot, React.js, Streamlit, Flask, Flutter, Node.js, MySQL, PostgreSQL, SQLite, AWS Cloud, Docker, Git, REST APIs, and Agile DevOps methodologies.", space_after=10)

    doc.add_page_break()

    # =========================================================================
    # PAGE 12: TRAINING DETAILS AND ACTIVITIES (PART 1)
    # =========================================================================
    add_title("TRAINING DETAILS AND ACTIVITIES", space_before=10, space_after=15)
    
    add_para("During the 60-hour training program at Axelyne LLP, I participated in structured theoretical training, laboratory exercises, and live project implementation under senior mentoring. The syllabus was divided into four comprehensive work modules:")
    
    def add_module_box(mod_name, mod_title, bullet_items):
        t_mod = doc.add_table(rows=2, cols=1)
        t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        c_hdr = t_mod.rows[0].cells[0]
        c_hdr.text = f"{mod_name}\n{mod_title}"
        set_cell_background(c_hdr, "DCEBF8")
        set_cell_margins(c_hdr, top=100, bottom=100, left=150, right=150)
        c_hdr.paragraphs[0].runs[0].bold = True
        c_hdr.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Content Row
        c_body = t_mod.rows[1].cells[0]
        set_cell_margins(c_body, top=100, bottom=100, left=150, right=150)
        p_body = c_body.paragraphs[0]
        for idx, item in enumerate(bullet_items):
            if idx > 0:
                p_body = c_body.add_paragraph()
            p_body.paragraph_format.space_after = Pt(3)
            r = p_body.add_run(f"• {item}")
            r.font.size = Pt(10.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_module_box(
        "Module 1 (01 Hours To 15 Hours)",
        "Web Foundations: HTML5, CSS3 & Responsive UI",
        [
            "HTML5 semantic structures, forms, audio/video, and interactive controls.",
            "CSS3 box model, flexbox, CSS grid, transitions, and hover micro-animations.",
            "Mobile-responsive design principles and CSS custom properties (variables).",
            "CSS styling injection into modern Python web application frameworks."
        ]
    )

    add_module_box(
        "Module 2 (16 Hours To 30 Hours)",
        "Core Python Programming & Data Manipulation",
        [
            "Python data structures: lists, tuples, dictionaries, and set operations.",
            "Object-Oriented Programming (OOP): classes, inheritance, encapsulation, and methods.",
            "Modular architecture, exception handling, and virtual environments (venv).",
            "Database connectivity using sqlite3 and PyMySQL libraries."
        ]
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 13: TRAINING DETAILS AND ACTIVITIES (PART 2)
    # =========================================================================
    add_module_box(
        "Module 3 (31 Hours To 45 Hours)",
        "Backend Architecture: Flask REST API & Relational Database",
        [
            "Flask application factory pattern and modular Blueprints.",
            "Designing RESTful HTTP endpoints (GET, POST, PUT, DELETE) with JSON serialization.",
            "Database schema migrations, primary/foreign key relationships, and transactions.",
            "Role-Based Access Control (RBAC) and user session state handling.",
            "API testing with Postman, request validation, and error code handling."
        ]
    )

    add_module_box(
        "Module 4 (46 Hours To 60 Hours)",
        "CraveHub Project Implementation & Testing",
        [
            "End-to-end implementation of CraveHub Gourmet Delivery Platform.",
            "Designing Royal Velvet UI theme (Indigo/Violet) with animated cards and banner.",
            "Building 5-step live order tracking and 4-digit OTP handover verification.",
            "Developing Kitchen Display System (KDS) and Admin Analytics with pandas charts.",
            "End-to-end integration testing, debugging, and git version control push."
        ]
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 14: TECHNOLOGIES AND TOOLS USED
    # =========================================================================
    add_title("TECHNOLOGIES AND TOOLS USED", space_before=15, space_after=20)
    
    tech_data = [
        ("Programming Language", "Python 3.13 (Core language powering both backend API & frontend UI)"),
        ("Backend Web Framework", "Flask 3.x (Lightweight, modular RESTful API microservices engine)"),
        ("Frontend UI Framework", "Streamlit 1.30+ (Modern, dynamic reactive data web framework)"),
        ("Styling & Theming", "Vanilla CSS3, Google Fonts (Plus Jakarta Sans), Royal Velvet Design System"),
        ("Database Systems", "SQLite 3 (Zero-config local engine) & MySQL 8.x (Production enterprise DB)"),
        ("Data Processing", "Pandas 2.x & NumPy (Analytics aggregation, revenue calculation & metrics)"),
        ("Version Control", "Git & GitHub (Repository management, branching, commits, and deployment)"),
        ("Development Environment", "Visual Studio Code (VS Code IDE with Python, Linters, and Git tools)")
    ]
    
    t_tech = doc.add_table(rows=len(tech_data) + 1, cols=2)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tech.rows[0].cells[0].text = "Technology / Tool"
    t_tech.rows[0].cells[1].text = "Specification & Usage in CraveHub"
    for c in t_tech.rows[0].cells:
        set_cell_background(c, "DCEBF8")
        set_cell_margins(c, top=140, bottom=140, left=150, right=150)
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    for r_idx, (t_name, t_desc) in enumerate(tech_data):
        r_c = t_tech.rows[r_idx + 1].cells
        r_c[0].text = t_name
        r_c[0].paragraphs[0].runs[0].bold = True
        r_c[1].text = t_desc
        for c in r_c:
            set_cell_margins(c, top=110, bottom=110, left=150, right=150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 15: TASK UNDERTAKEN
    # =========================================================================
    add_title("TASK UNDERTAKEN", space_before=15, space_after=18)
    
    add_para("Objective of Tasks:", bold=True, size=12.5, space_after=6)
    tasks = [
        "Architecting a modular full-stack application connecting customer ordering with kitchen operations.",
        "Developing a secure authentication module with role separation (Customer, Admin, Kitchen, Delivery).",
        "Building an interactive customer showcase featuring category filters, search, and dynamic cart operations.",
        "Designing a real-world checkout module supporting simulated UPI intent payments with transaction ID generation.",
        "Developing a 5-step live order status visual pipeline with real-time progression.",
        "Implementing a secure 4-digit OTP handover mechanism ensuring order parcels are delivered to verified customers.",
        "Engineering a real-time Kitchen Display System (KDS) enabling chefs to update order status.",
        "Developing an executive Admin Analytics Dashboard with revenue charts, order counts, and top-dish metrics."
    ]
    for t in tasks:
        add_bullet(t, space_after=6)
        
    add_para("\nOutcome Achieved:", bold=True, size=12.5, space_after=6)
    add_para("The tasks enabled me to master end-to-end full-stack software development, REST API design, concurrent server execution, database normalization, and user experience engineering in Python.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 16: SYSTEM DESIGN - ENTITY RELATIONSHIP DIAGRAM (ERD)
    # =========================================================================
    add_title("SYSTEM DESIGN: ENTITY RELATIONSHIP DIAGRAM (ERD)", space_before=10, space_after=14)
    
    add_para("The CraveHub database architecture is normalized to 3NF (Third Normal Form) to eliminate data redundancy and preserve referential integrity across relational tables:")
    
    if os.path.exists("report_assets/erd_diagram.png"):
        doc.add_picture("report_assets/erd_diagram.png", width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 1: CraveHub Entity Relationship Diagram (Database Schema)")
        r_cap.font.size = Pt(10)
        r_cap.italic = True
        
    add_para("Key Entities & Relationships in CraveHub:", bold=True, size=11.5, space_after=4)
    add_bullet("USERS: Stores credentials, phone numbers, and roles (Customer, Kitchen, Delivery, Admin).")
    add_bullet("CATEGORIES & MENU_ITEMS: 1-to-Many hierarchy defining food catalog items, pricing, and stock status.")
    add_bullet("ORDERS & ORDER_ITEMS: 1-to-Many relationship capturing order placements, customer address, and items.")
    add_bullet("PAYMENTS: 1-to-1 relationship recording payment method (UPI/COD/Card), transaction ID, and status.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 17: SYSTEM DESIGN - DATA FLOW DIAGRAMS (DFD)
    # =========================================================================
    add_title("SYSTEM DESIGN: DATA FLOW DIAGRAMS (DFD)", space_before=10, space_after=12)
    
    add_para("DFD Level 0 (Context Level Diagram):", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/dfd_level0.png"):
        doc.add_picture("report_assets/dfd_level0.png", width=Inches(6.2))
        p_cap0 = doc.add_paragraph()
        p_cap0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap0.paragraph_format.space_after = Pt(8)
        r_c0 = p_cap0.add_run("Figure 2: DFD Level 0 -- CraveHub Context-Level Architecture")
        r_c0.font.size = Pt(9.5)
        r_c0.italic = True
        
    add_para("DFD Level 1 (Decomposition of Processes & Data Stores):", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/dfd_level1.png"):
        doc.add_picture("report_assets/dfd_level1.png", width=Inches(6.2))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(8)
        r_c1 = p_cap1.add_run("Figure 3: DFD Level 1 -- Subsystem Processes and Data Stores")
        r_c1.font.size = Pt(9.5)
        r_c1.italic = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 18: RESULTS & SNAPSHOTS (PART 1)
    # =========================================================================
    add_title("RESULTS & APPLICATION SNAPSHOTS", space_before=10, space_after=14)
    
    add_para("Task 1: User Authentication & Role-Based Access Portal", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/snapshot_login.png"):
        doc.add_picture("report_assets/snapshot_login.png", width=Inches(6.2))
    add_para("Description: Implemented a responsive sign-in and registration portal. Securely routes authenticated sessions to specific role panels (Customer, Admin, Kitchen, or Delivery).", size=10.5, space_after=16)

    add_para("Task 2: Customer Food Showcase & Royal Velvet Hero Banner", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/snapshot_customer.png"):
        doc.add_picture("report_assets/snapshot_customer.png", width=Inches(6.2))
    add_para("Description: Dynamic food catalog with real-time category filtering, search, pricing badges, and interactive 'Add to Order' buttons styled with Royal Velvet Indigo & Violet design tokens.", size=10.5, space_after=12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 19: RESULTS & SNAPSHOTS (PART 2)
    # =========================================================================
    add_title("RESULTS & APPLICATION SNAPSHOTS (CONTD.)", space_before=10, space_after=14)
    
    add_para("Task 3: Live 5-Step Order Tracking & Handover OTP Verification", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/snapshot_tracking.png"):
        doc.add_picture("report_assets/snapshot_tracking.png", width=Inches(6.2))
    add_para("Description: Interactive tracking screen displaying real-time preparation status (Order Placed -> Preparing -> Food Ready -> On The Way -> Delivered) and customer verification 4-digit OTP PIN.", size=10.5, space_after=16)

    add_para("Task 4: Executive Business Analytics Dashboard", bold=True, size=12, space_after=4)
    if os.path.exists("report_assets/snapshot_analytics.png"):
        doc.add_picture("report_assets/snapshot_analytics.png", width=Inches(6.2))
    add_para("Description: Real-time business reporting panel providing metric scorecards (Total Revenue, Order Count, AOV) and interactive trend visualizations generated with Pandas.", size=10.5, space_after=12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 20: SKILLS AND KNOWLEDGE ACQUIRED
    # =========================================================================
    add_title("SKILLS AND KNOWLEDGE ACQUIRED", space_before=15, space_after=18)
    
    skills = [
        "Hands-on expertise in full-stack Python application engineering and concurrent process execution.",
        "Proficiency in building modular RESTful microservices using Flask, Blueprints, and JSON endpoints.",
        "Expertise in creating reactive, interactive, modern web frontends using Streamlit and custom CSS design systems.",
        "Deep understanding of relational database normalization, schema design, indexes, and SQL transactions (SQLite/MySQL).",
        "Implementation of secure role-based access control, session state persistence, and authentication logic.",
        "Real-world understanding of business workflows including digital UPI payments, Kitchen KDS, and OTP verification.",
        "Software testing, exception handling, data sanitization, and structured error reporting.",
        "Professional version control workflows with Git and GitHub (branching, commits, pull/push, conflict resolution).",
        "Practical experience with project documentation, technical design, and agile problem solving."
    ]
    for s in skills:
        add_bullet(s, space_after=8)

    doc.add_page_break()

    # =========================================================================
    # PAGE 21: LEARNING EXPERIENCE
    # =========================================================================
    add_title("LEARNING EXPERIENCE", space_before=15, space_after=18)
    
    add_para("The On-the-Job Training at Axelyne LLP provided me with enriching practical software engineering experience and significantly deepened my understanding of how modern IT companies conceptualize, architect, and deliver digital products.")
    add_para("Working on the CraveHub project gave me an end-to-end perspective on software development life cycle (SDLC). Rather than developing isolated academic code snippets, I learned how frontend reactive components interface with backend REST APIs, how data persistence is managed across distributed operations, and how to structure code for maintainability and scalability.")
    add_para("Overcoming technical obstacles—such as handling concurrency between Flask and Streamlit, preventing database constraint conflicts, and designing responsive CSS themes—helped me enhance my debugging and problem-solving skills. The continuous mentoring from my industry supervisor taught me industry best practices regarding clean code, documentation, and agile execution.")
    add_para("Overall, this training has boosted my technical confidence, strengthened my computer science foundation, and prepared me for professional software engineering opportunities.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 22: CONCLUSION
    # =========================================================================
    add_title("CONCLUSION", space_before=20, space_after=22)
    
    add_para("The On-the-Job Training programme at Axelyne LLP was an immensely valuable learning journey. It allowed me to transform academic computer applications concepts into a fully functioning, professional full-stack web application.")
    add_para("Through the design and development of CraveHub, I acquired practical competencies in Python, Flask REST APIs, Streamlit frontend design, relational database modeling, and real-time operational workflows. The training fostered an understanding of software engineering ethics, team collaboration, and professional industry practices.")
    add_para("I am deeply thankful to Axelyne LLP, my industry supervisor Ms. Archana Sachin Nigade, the Department of Computer Application, and the faculty members of Gopal Krushana Gokhale College / Shivaji University, Kolhapur for their invaluable guidance and support throughout this program.")
    
    add_para("\nPlace: Kolhapur", bold=True)
    add_para("Date: ________________", bold=True, space_after=55)
    add_para("____________________________________", bold=True)
    add_para("Student Signature (Vivek Bandu Lavhate)", bold=True, size=12)

    # Save Document
    out_path = "CraveHub_OJT_Project_Report.docx"
    doc.save(out_path)
    print(f"Documentation successfully created at: {os.path.abspath(out_path)}")

if __name__ == "__main__":
    create_report()
