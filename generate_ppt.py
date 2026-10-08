import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_master_visual_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Curated Premium Minimal Dark Palette
    BG_COLOR = RGBColor(11, 15, 25)       # #0B0F19 Deep Dark Navy
    CARD_BG = RGBColor(22, 30, 46)        # #161E2E Slate Card
    CARD_BORDER = RGBColor(45, 60, 88)    # #2D3C58 Border
    ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4 Electric Cyan
    ALERT_RED = RGBColor(239, 68, 68)     # #EF4444 Crimson Alert
    TEXT_MAIN = RGBColor(248, 250, 252)   # #F8FAFC Crisp White
    TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8 Slate Gray
    ACCENT_GREEN = RGBColor(34, 197, 94)  # #22C55E Emerald Green

    blank_layout = prs.slide_layouts[6]
    assets_dir = r"c:\cloud project\docs\assets"

    def add_background(slide):
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="CLOUD SECURITY ALERT LAMP"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN
        p_cat.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        p_title.font.name = "Arial"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_image_card(slide, img_name, left, top, width, height, border_color=ACCENT_CYAN):
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            add_card(slide, left - Inches(0.06), top - Inches(0.06), width + Inches(0.12), height + Inches(0.12), bg_color=CARD_BG, border_color=border_color)
            return slide.shapes.add_picture(img_path, left, top, width, height)
        else:
            print(f"[-] Image not found: {img_path}")
            return None

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================
    # SLIDE 1: Title & Team Overview
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CLOUD SECURITY ALERT LAMP 🚨💡"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    p2 = tf1.add_paragraph()
    p2.text = "Real-Time Cyber-Physical Alert System & Digital Twin for AWS S3 Exposures"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(6)

    members = [
        ("01", "D. Chander", "Roll: 2503A52214", "Project Lead & Overview", ["• S3 Exposure Dangers", "• Email Fatigue Bottleneck", "• Digital Twin Web UI"]),
        ("02", "K. Arjun", "Roll: 2503A52235", "Backend & Database", ["• FastAPI Server & REST", "• DynamoDB Audit Logging", "• 1-Click AWS Deployer"]),
        ("03", "G. Rohan", "Roll: 2503S52224", "Architecture & Security", ["• 4-Stage Data Pipeline", "• Lambda 3-Layer Auditor", "• X.509 Mutual TLS"]),
        ("04", "P. Sachin", "Roll: 2503A52240", "Hardware & Firmware", ["• ESP32 Circuit Wiring", "• FreeRTOS State Machine", "• Live Breach Demo Flow"])
    ]

    card_w = Inches(2.7)
    gap = Inches(0.25)
    left_start = Inches(0.8)

    for idx, (num, name, roll, role, minibullets) in enumerate(members):
        c_left = left_start + idx * (card_w + gap)
        add_card(s1, c_left, Inches(2.0), card_w, Inches(4.8), bg_color=CARD_BG, border_color=ACCENT_CYAN)

        tb = s1.shapes.add_textbox(c_left + Inches(0.15), Inches(2.15), card_w - Inches(0.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(22)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_CYAN

        p_name = tf.add_paragraph()
        p_name.text = name
        p_name.font.size = Pt(16)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_MAIN
        p_name.space_before = Pt(6)

        p_roll = tf.add_paragraph()
        p_roll.text = roll
        p_roll.font.size = Pt(11)
        p_roll.font.color.rgb = TEXT_MUTED

        p_role = tf.add_paragraph()
        p_role.text = role
        p_role.font.size = Pt(12)
        p_role.font.bold = True
        p_role.font.color.rgb = ACCENT_GREEN
        p_role.space_before = Pt(8)

        for mb in minibullets:
            p_mb = tf.add_paragraph()
            p_mb.text = mb
            p_mb.font.size = Pt(10)
            p_mb.font.color.rgb = TEXT_MAIN
            p_mb.space_before = Pt(4)

    add_notes(s1, "SPEAKER NOTES - D. Chander: Welcome evaluators. Today we present the Cloud Security Alert Lamp...")

    # ==========================================
    # SLIDE 2: Team Roles & Evaluation Flow
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Team Presentation Roles & Evaluation Breakdown", "EXPERT DOMAIN ALLOCATION")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8), border_color=ACCENT_CYAN)
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.133), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "📋 Specialized Engineering Domain Allocation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    roles = [
        ("01. D. Chander (2503A52214) — Project Lead & Overview", [
            "• Explains business impact of S3 public leaks and alert fatigue.",
            "• Demonstrates interactive glassmorphism Web Twin Dashboard."
        ]),
        ("02. K. Arjun (2503A52235) — Backend & Database Developer", [
            "• Explains FastAPI async REST/WebSocket server and DynamoDB audit logging.",
            "• Demonstrates 1-click deployer script (deploy_aws.py)."
        ]),
        ("03. G. Rohan (2503S52224) — System Architecture & Security", [
            "• Explains 4-stage cyber-physical data pipeline.",
            "• Details AWS Lambda 3-Layer Auditor and X.509 Mutual TLS security."
        ]),
        ("04. P. Sachin (2503A52240) — Working Process & Hardware Developer", [
            "• Details ESP32 C++ non-blocking FreeRTOS state machine and circuit schematics.",
            "• Conducts live 4-step security breach and remediation test flow."
        ])
    ]

    for title, minibullets in roles:
        p_n = tf.add_paragraph()
        p_n.text = title
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = ACCENT_GREEN
        p_n.space_before = Pt(8)

        for mb in minibullets:
            p_mb = tf.add_paragraph()
            p_mb.text = mb
            p_mb.font.size = Pt(11)
            p_mb.font.color.rgb = TEXT_MAIN
            p_mb.space_before = Pt(2)

    # ==========================================
    # SLIDE 3: Problem Statement
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "The Problem: S3 Cloud Exposure & Alert Fatigue", "PROBLEM STATEMENT")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(6.0), Inches(2.25), border_color=ALERT_RED)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.6), Inches(1.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ Massive Cloud Data Exposure Risk"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED
    
    mini3_1 = [
        "• Root Cause: Accidental public bucket policies or disabled Account Public Access Block.",
        "• Bot Threat: Automated scrapers scan public AWS subdomains within 30 seconds of creation.",
        "• Business Loss: Average enterprise cloud data breach cost exceeds $4.45 Million."
    ]
    for mb in mini3_1:
        p = tf.add_paragraph()
        p.text = mb
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    add_card(s3, Inches(0.8), Inches(4.35), Inches(6.0), Inches(2.25), border_color=ACCENT_CYAN)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.6), Inches(1.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📫 Email Alert Fatigue & Response Lag"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    mini3_2 = [
        "• Inbox Noise: Security teams receive 500+ daily automated emails; critical alerts get buried.",
        "• Detection Delay: Industry average latency to identify open S3 buckets is > 14 hours.",
        "• Solution: Convert silent email noise into sub-second physical desk situational awareness."
    ]
    for mb in mini3_2:
        p = tf.add_paragraph()
        p.text = mb
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    add_image_card(s3, "data_leak_concept.png", Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.8), border_color=ALERT_RED)

    # ==========================================
    # SLIDE 4: Solution Architecture Pipeline
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "System Solution Architecture: 4-Stage Data Pipeline", "SYSTEM ARCHITECTURE")

    # 4 horizontal mini flow cards across bottom
    stages = [
        ("STAGE 1: DETECTION", "AWS Lambda Auditor", ACCENT_CYAN, [
            "• Scans S3 bucket policies & ACLs",
            "• Evaluates Account Public Block",
            "• Generates JSON risk payload"
        ]),
        ("STAGE 2: STORAGE", "DynamoDB & SNS", ACCENT_GREEN, [
            "• Logs audit record in DynamoDB",
            "• Dispatches SNS email/SMS alerts",
            "• Provides immutable history"
        ]),
        ("STAGE 3: DISPATCH", "AWS IoT Core Broker", ACCENT_CYAN, [
            "• Publishes payload over MQTT",
            "• Enforces TLS 1.2 on Port 8883",
            "• Validates X.509 client cert"
        ]),
        ("STAGE 4: ACTUATION", "ESP32 & Web Twin", ALERT_RED, [
            "• Flashes physical Red LED 🔴",
            "• Syncs Web UI via WebSockets",
            "• Provides instant physical alert"
        ])
    ]

    card_w4 = Inches(2.7)
    gap4 = Inches(0.25)
    left_start4 = Inches(0.8)

    for idx, (stg_name, stg_title, color, minibullets) in enumerate(stages):
        c_left = left_start4 + idx * (card_w4 + gap4)
        add_card(s4, c_left, Inches(1.8), card_w4, Inches(4.8), bg_color=CARD_BG, border_color=color)

        tb = s4.shapes.add_textbox(c_left + Inches(0.12), Inches(1.95), card_w4 - Inches(0.24), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_stg = tf.paragraphs[0]
        p_stg.text = stg_name
        p_stg.font.size = Pt(10)
        p_stg.font.bold = True
        p_stg.font.color.rgb = color

        p_ttl = tf.add_paragraph()
        p_ttl.text = stg_title
        p_ttl.font.size = Pt(15)
        p_ttl.font.bold = True
        p_ttl.font.color.rgb = TEXT_MAIN
        p_ttl.space_before = Pt(4)

        for mb in minibullets:
            p_mb = tf.add_paragraph()
            p_mb.text = mb
            p_mb.font.size = Pt(11)
            p_mb.font.color.rgb = TEXT_MUTED
            p_mb.space_before = Pt(6)

    # ==========================================
    # SLIDE 5: AWS S3 3-Layer Auditor
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Deep Dive: AWS S3 3-Layer Auditor (Lambda & Boto3)", "CLOUD SCANNER")

    add_image_card(s5, "security_layers_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ALERT_RED)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🛡️ 3 Audit Checks Executed Per Bucket"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    auditor_mini = [
        ("1. Public Access Block Check", "Audits GetPublicAccessBlock. If any of 4 block flags are False ➔ flagged."),
        ("2. Bucket Policy Status Check", "Queries GetBucketPolicyStatus. Checks for IsPublic: True or wildcard Principal: '*'."),
        ("3. ACL Access Grant Check", "Parses GetBucketAcl. Flagged if AllUsers or AuthenticatedUsers URI exists.")
    ]
    for title, desc in auditor_mini:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_desc = tf.add_paragraph()
        p_desc.text = "  • " + desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_before = Pt(1)

    # ==========================================
    # SLIDE 6: FastAPI Backend & DynamoDB
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "FastAPI Backend & DynamoDB Database Infrastructure", "BACKEND & STORAGE")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚡ FastAPI Asynchronous Server"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    be_mini = [
        ("Python Async Engine", "Non-blocking event loop handles high-concurrency client connections."),
        ("REST Endpoints", "Exposes /api/dashboard, /api/events, and /api/scan endpoints."),
        ("WebSocket Broadcast", "Push-delivers live state updates directly to browser Web Twin UI.")
    ]
    for title, desc in be_mini:
        p = tf.add_paragraph()
        p.text = "• " + title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_desc = tf.add_paragraph()
        p_desc.text = "  " + desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ACCENT_GREEN)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🗄️ DynamoDB & SNS Alert Dispatcher"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    db_mini = [
        ("NoSQL Audit Log", "Stores immutable scan records in DynamoDB 'SecurityEvents' table."),
        ("Key Schema", "Partition Key: eventId (S) | Range Key: timestamp (S)."),
        ("On-Demand Scaling", "PAY_PER_REQUEST billing auto-scales with zero server management."),
        ("Amazon SNS Alerts", "Dispatches instant SMS and email notifications to security subscribers.")
    ]
    for title, desc in db_mini:
        p = tf.add_paragraph()
        p.text = "• " + title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = "  " + desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: AWS IoT Core Security
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "AWS IoT Core Mutual TLS & X.509 Security", "SECURITY & PROTOCOLS")

    add_image_card(s7, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ACCENT_GREEN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔒 Zero-Trust IoT Security Blueprint"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    items_mini = [
        ("MQTT over TLS 1.2 (Port 8883)", "All hardware telemetry is encrypted end-to-end against sniffing."),
        ("Mutual X.509 Authentication", "ESP32 validates Amazon Root CA 1 and presents client X.509 cert."),
        ("Scoped IAM IoT Policy", "Restricts hardware client strictly to iot:Connect and iot:Subscribe actions.")
    ]
    for title, desc in items_mini:
        p = tf.add_paragraph()
        p.text = "• " + title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_desc = tf.add_paragraph()
        p_desc.text = "  " + desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: Hardware & Firmware
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "ESP32 Circuit Schematics & C++ Firmware Engine", "HARDWARE & FIRMWARE")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔌 Component Wiring & Firmware Engine"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    hw_mini = [
        ("ESP32 DevKit v1", "Dual-core 240MHz microcontroller with hardware TLS crypto engine."),
        ("Red LED Actuator", "Anode connected to GPIO 23 via 220Ω current-limiting resistor."),
        ("FreeRTOS Non-Blocking FSM", "Driven by millis() timers (zero blocking delay() calls)."),
        ("3 State Machine States", "STATE_SECURE 🟢 | STATE_ALERT 🔴 (200ms blink) | STATE_DISCONNECTED 🟡.")
    ]
    for title, desc in hw_mini:
        p = tf.add_paragraph()
        p.text = "• " + title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN
        p.space_before = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = "  " + desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MAIN

    add_image_card(s8, "esp32_macro_render.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ALERT_RED)

    # ==========================================
    # SLIDE 9: Web Twin Dashboard
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Interactive Glassmorphism Digital Twin Dashboard", "DIGITAL TWIN UI")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💻 Web Twin UI Capabilities"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    dash_mini = [
        ("Dark Glassmorphism UI", "Styled with CSS backdrop blur, neon glow highlights, and reactive cards."),
        ("Simulated Virtual LED", "Pulsating neon red LED flashes synchronously with physical hardware."),
        ("Live Audit Event Log", "Renders history of scanned bucket names, timestamps, and severity levels."),
        ("Interactive Test Harness", "Enables students/teachers to trigger scan tests directly from browser.")
    ]
    for t, d in dash_mini:
        p = tf.add_paragraph()
        p.text = "• " + t
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN
        p.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = "  " + d
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MAIN

    add_image_card(s9, "neon_dashboard_screen.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 10: 1-Click Provisioner & Test CLI
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Automated AWS Provisioner & Test CLI Utilities", "CLOUD AUTOMATION")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=ACCENT_CYAN)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 1-Click Provisioner (deploy_aws.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    deploy_mini = [
        "• Auto-provisions DynamoDB, SNS topic, Lambda function & IoT Thing.",
        "• Auto-detects AWS Learner Lab $50 Student Account 'LabRole' or creates standard IAM role.",
        "• Generates X.509 keys & certificates and populates firmware/include/secrets.h automatically."
    ]
    for d in deploy_mini:
        p = tf.add_paragraph()
        p.text = d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=ACCENT_GREEN)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧪 Test CLI Utility (test_vulnerable_bucket.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    cli_sample = (
        "# 1. Simulate S3 Security Exposure\n"
        "$ python cloud/test_vulnerable_bucket.py create\n"
        "[+] Created bucket: vulnerable-test-bucket-8842\n"
        "[+] Disabled PublicAccessBlock & attached PUBLIC policy!\n"
        "[+] Triggering Lambda scan...\n"
        "==> ESP32 LED BLINKS RAPIDLY (ALERT) 🔴\n\n"
        "# 2. Remediate & Cleanup\n"
        "$ python cloud/test_vulnerable_bucket.py delete\n"
        "[+] Deleted vulnerable bucket.\n"
        "==> ESP32 LED TURNS SOLID OFF (OK) 🟢"
    )
    p_code = tf.add_paragraph()
    p_code.text = cli_sample
    p_code.font.size = Pt(11)
    p_code.font.name = "Consolas"
    p_code.font.color.rgb = TEXT_MAIN
    p_code.space_before = Pt(8)

    # ==========================================
    # SLIDE 11: Live Working Demonstration Flow
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Live Working Demonstration Flow (Step-by-Step)", "CLASSROOM DEMO")

    step_data = [
        ("1. Baseline", "Connect ESP32 USB.\nConfirm LED is OFF 🟢.", ACCENT_CYAN),
        ("2. Breach", "Run: python test_vulnerable_bucket.py create", ALERT_RED),
        ("3. Actuation", "Red LED blinks rapidly (200ms) 🔴. Web UI ALERT.", ALERT_RED),
        ("4. Audit Logs", "Inspect DynamoDB event logs & serial monitor.", ACCENT_CYAN),
        ("5. Remediation", "Run: python test_vulnerable_bucket.py delete. LED OFF 🟢.", ACCENT_GREEN)
    ]

    card_w11 = Inches(2.2)
    gap11 = Inches(0.18)
    left_start11 = Inches(0.8)

    for idx, (title, desc, color) in enumerate(step_data):
        c_left = left_start11 + idx * (card_w11 + gap11)
        add_card(s11, c_left, Inches(1.8), card_w11, Inches(4.8), bg_color=CARD_BG, border_color=color)

        tb = s11.shapes.add_textbox(c_left + Inches(0.1), Inches(2.0), card_w11 - Inches(0.2), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_MAIN
        p_desc.space_before = Pt(12)

    # ==========================================
    # SLIDE 12: Q&A & Conclusion
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)

    add_card(s12, Inches(0.8), Inches(1.2), Inches(6.0), Inches(5.1), bg_color=CARD_BG, border_color=ACCENT_CYAN)

    tb = s12.shapes.add_textbox(Inches(1.1), Inches(1.5), Inches(5.4), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "THANK YOU! 🚨💡"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p2 = tf.add_paragraph()
    p2.text = "Questions & Technical Jury Defense"
    p2.font.size = Pt(20)
    p2.font.color.rgb = TEXT_MAIN
    p2.space_before = Pt(10)

    team_list = [
        "• D. Chander (Roll No: 2503A52214)",
        "• K. Arjun (Roll No: 2503A52235)",
        "• G. Rohan (Roll No: 2503S52224)",
        "• P. Sachin (Roll No: 2503A52240)"
    ]
    for m in team_list:
        p_m = tf.add_paragraph()
        p_m.text = m
        p_m.font.size = Pt(12)
        p_m.font.color.rgb = TEXT_MUTED
        p_m.space_before = Pt(4)

    add_image_card(s12, "cyber_alert_desk.png", Inches(7.1), Inches(1.2), Inches(5.4), Inches(5.1), border_color=ACCENT_CYAN)

    output_path = "docs/Cloud_Security_Alert_Lamp_Presentation.pptx"
    try:
        prs.save(output_path)
        print(f"[+] Enhanced Master Team PPTX successfully created at: {output_path}")
    except PermissionError:
        alt_path = "docs/Cloud_Security_Alert_Lamp_Presentation_v2.pptx"
        prs.save(alt_path)
        print(f"[+] Enhanced Master Team PPTX saved to alternative path (file was locked): {alt_path}")

if __name__ == "__main__":
    create_master_visual_deck()
