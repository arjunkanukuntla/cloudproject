import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_executive_clean_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Sleek Professional Dark Theme
    BG_COLOR = RGBColor(11, 15, 25)       # #0B0F19 Deep Dark Charcoal/Navy
    CARD_BG = RGBColor(22, 30, 46)        # #161E2E Slate Card
    CARD_BORDER = RGBColor(45, 60, 88)    # #2D3C58 Subtle Border
    CYAN = RGBColor(6, 182, 212)          # #06B6D4 Electric Cyan
    RED = RGBColor(239, 68, 68)           # #EF4444 Crimson Alert
    GREEN = RGBColor(34, 197, 94)         # #22C55E Emerald Green
    TEXT_MAIN = RGBColor(248, 250, 252)   # #F8FAFC Crisp White
    TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8 Slate Gray

    blank_layout = prs.slide_layouts[6]
    assets_dir = r"c:\cloud project\docs\assets"

    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="CLOUD SECURITY ALERT LAMP"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN
        p_cat.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN
        p_title.font.name = "Arial"

    def draw_card(slide, left, top, width, height, border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_fitted_image(slide, img_name, left, top, width, height, border_color=CYAN):
        # Draw bounding container card
        draw_card(slide, left, top, width, height, border_color=border_color, bg_color=CARD_BG)
        
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            pad = Inches(0.1)
            img_left = left + pad
            img_top = top + pad
            img_width = width - (2 * pad)
            img_height = height - (2 * pad)
            return slide.shapes.add_picture(img_path, img_left, img_top, width=img_width, height=img_height)
        return None

    def add_speaker_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text

    # =========================================================================
    # SLIDE 1: Title Slide & Authors
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(1.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CLOUD SECURITY ALERT LAMP 🚨💡"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "Real-Time Cyber-Physical Alert System & Digital Twin for AWS S3 Bucket Exposure"
    p_sub.font.size = Pt(18)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_MAIN
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(8)

    # 4 Author Cards
    authors = [
        ("D. Chander", "Roll: 2503A52214", "Project Lead & Web Twin"),
        ("G. Rohan", "Roll: 2503S52224", "System Architecture & Security"),
        ("K. Arjun", "Roll: 2503A52235", "Backend & Database Developer"),
        ("P. Sachin", "Roll: 2503A52240", "Hardware & Firmware Engineer")
    ]

    card_w = Inches(2.7)
    gap = Inches(0.25)
    left_start = Inches(0.8)

    for idx, (name, roll, role) in enumerate(authors):
        c_left = left_start + idx * (card_w + gap)
        draw_card(s1, c_left, Inches(2.7), card_w, Inches(3.8), border_color=CYAN)

        tb = s1.shapes.add_textbox(c_left + Inches(0.15), Inches(2.9), card_w - Inches(0.3), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_name = tf.paragraphs[0]
        p_name.text = name
        p_name.font.size = Pt(17)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_MAIN

        p_roll = tf.add_paragraph()
        p_roll.text = roll
        p_roll.font.size = Pt(12)
        p_roll.font.color.rgb = TEXT_MUTED
        p_roll.space_before = Pt(4)

        p_role = tf.add_paragraph()
        p_role.text = role
        p_role.font.size = Pt(12)
        p_role.font.bold = True
        p_role.font.color.rgb = GREEN
        p_role.space_before = Pt(16)

    add_speaker_notes(s1, "SPEAKER NOTES - D. Chander: Respected evaluators, good morning. We present the Cloud Security Alert Lamp...")

    # =========================================================================
    # SLIDE 2: Executive Summary
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Executive Summary & Core Value Proposition", "EXECUTIVE SUMMARY")

    draw_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Core Solution Pillars"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN

    pillars = [
        ("Sub-Second Physical Actuation", "High-brightness Red LED flashes instantly on engineer's desk upon S3 breach."),
        ("Automated Serverless Scanning", "AWS Lambda evaluates S3 policies & ACLs using boto3 without polling overhead."),
        ("Zero-Trust Hardware Security", "X.509 client certificates & TLS 1.2 port 8883 MQTT protect IoT endpoints.")
    ]
    for title, desc in pillars:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s2, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s2, "SPEAKER NOTES - D. Chander: Our solution bridges cloud security scanning with physical desk hardware...")

    # =========================================================================
    # SLIDE 3: The Problem Statement
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "The Problem: S3 Public Exposures & Email Alert Fatigue", "PROBLEM STATEMENT")

    draw_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "$4.45 Million"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RED

    p_sub = tf.add_paragraph()
    p_sub.text = "Average Enterprise Cloud Data Breach Cost"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_MAIN
    p_sub.space_before = Pt(4)

    probs = [
        "Accidental Public S3 Bucket Policies",
        "Automated Bots Exploit Leaks in Seconds",
        "500+ Daily Security Emails Cause Inbox Noise",
        "> 14 Hours Average Time to Detect Open Buckets"
    ]
    for b in probs:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_fitted_image(s3, "data_leak_concept.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    add_speaker_notes(s3, "SPEAKER NOTES - D. Chander: Misconfigured S3 buckets remain a major cause of data breaches...")

    # =========================================================================
    # SLIDE 4: Solution Architecture Pipeline
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "End-to-End Cyber-Physical System Architecture", "SYSTEM ARCHITECTURE")

    add_fitted_image(s4, "cloud_pipeline_3d.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "4-Stage Event Pipeline"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    stages = [
        ("Stage 1: Lambda Auditor", "Evaluates S3 PublicAccessBlock, Bucket Policy & ACLs."),
        ("Stage 2: Storage & SNS", "Logs event to DynamoDB and broadcasts SNS emails/SMS."),
        ("Stage 3: AWS IoT Core", "Publishes JSON alert payload over MQTT (TLS 1.2)."),
        ("Stage 4: Physical Lamp", "ESP32 blinks Red LED and updates WebSocket Web Twin UI.")
    ]
    for stg, desc in stages:
        p = tf.add_paragraph()
        p.text = f"•  {stg}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s4, "SPEAKER NOTES - G. Rohan: Here is our 4-stage decoupled architecture...")

    # =========================================================================
    # SLIDE 5: AWS Lambda 3-Layer Auditor
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Deep Dive: AWS Lambda 3-Layer Auditor Engine", "CLOUD SCANNER")

    add_fitted_image(s5, "security_layers_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "3-Layer Inspection Matrix"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RED

    layers = [
        ("Layer 1: Public Access Block", "Audits account & bucket-level public access restrictions."),
        ("Layer 2: Bucket Policy Status", "Inspects JSON statements for IsPublic: True or Principal: '*'."),
        ("Layer 3: S3 ACL Grants", "Parses grants for AllUsers or AuthenticatedUsers URIs.")
    ]
    for lyr, desc in layers:
        p = tf.add_paragraph()
        p.text = f"•  {lyr}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s5, "SPEAKER NOTES - G. Rohan: The scanner evaluates three distinct exposure vectors...")

    # =========================================================================
    # SLIDE 6: Zero-Trust X.509 Mutual TLS Security
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "AWS IoT Core Mutual TLS & X.509 Security", "SECURITY PROTOCOLS")

    add_fitted_image(s6, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Hardware Security Blueprint"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    sec = [
        ("Mutual Authentication (mTLS)", "ESP32 validates Amazon Root CA 1; AWS IoT validates client cert."),
        ("Hardware X.509 Certificate", "Device private key stored securely in hardware SPIFFS storage."),
        ("Port 8883 Encrypted Transport", "Prevents packet sniffing or payload tampering on local networks."),
        ("Scoped IAM IoT Policy", "Restricts hardware client strictly to topic cloud/security/alert.")
    ]
    for title, desc in sec:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s6, "SPEAKER NOTES - G. Rohan: We implement Zero-Trust hardware security using X.509 certificates...")

    # =========================================================================
    # SLIDE 7: FastAPI Asynchronous Backend Server
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_header(s7, "FastAPI Backend Application & REST API Layer", "BACKEND ARCHITECTURE")

    draw_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FastAPI Async Core"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    be = [
        ("High Concurrency Event Loop", "Asynchronous Python server handles high-throughput requests effortlessly."),
        ("REST Endpoints Provided", "Exposes /api/dashboard, /api/events, and /api/scan."),
        ("WebSocket Broadcast Engine", "Pushes real-time state frames directly to connected Web Twin clients.")
    ]
    for title, desc in be:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s7, "cyber_alert_desk.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s7, "SPEAKER NOTES - K. Arjun: I am K. Arjun, handling backend and database services...")

    # =========================================================================
    # SLIDE 8: Amazon DynamoDB & SNS Alert Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)
    add_header(s8, "Amazon DynamoDB Persistence & SNS Push Alerts", "STORAGE & NOTIFICATIONS")

    draw_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=GREEN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DynamoDB Audit Trail"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    db = [
        ("NoSQL Audit Log", "Stores immutable scan records in 'SecurityEvents' table."),
        ("Key Schema", "Partition Key: eventId (S) | Range Key: timestamp (S)."),
        ("On-Demand Auto Scaling", "PAY_PER_REQUEST billing auto-scales seamlessly.")
    ]
    for title, desc in db:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    draw_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Amazon SNS Dispatcher"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    sns = [
        ("Multi-Channel Push Alerts", "Dispatches instant SMS and email notifications."),
        ("Subscriber Management", "CloudSecurityAlerts SNS topic manages recipient lists."),
        ("Zero Latency Delivery", "Broadcasts alerts concurrently with IoT MQTT payloads.")
    ]
    for title, desc in sns:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s8, "SPEAKER NOTES - K. Arjun: Every breach event is persisted into DynamoDB...")

    # =========================================================================
    # SLIDE 9: Automated Infrastructure Provisioner
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_background(s9)
    add_header(s9, "Automated Cloud Infrastructure Provisioning", "CLOUD AUTOMATION")

    draw_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "1-Click Deployer Script"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    prov = [
        ("Automated Deployment", "Single command python cloud/deploy_aws.py provisions full stack."),
        ("Resource Management", "Creates DynamoDB table, SNS topic, Lambda function & IoT Thing."),
        ("Student Account Ready", "Auto-detects $50 AWS Learner Lab LabRole constraints."),
        ("Cert Auto-Injection", "Generates X.509 keys and populates firmware/include/secrets.h.")
    ]
    for title, desc in prov:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s9, "cloud_pipeline_3d.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s9, "SPEAKER NOTES - K. Arjun: Running deploy_aws.py automates cloud infrastructure provisioning...")

    # =========================================================================
    # SLIDE 10: ESP32 Hardware Circuitry
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_background(s10)
    add_header(s10, "ESP32 Hardware Engineering & Circuit Schematics", "HARDWARE ENGINEERING")

    draw_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Circuit Wiring & BOM"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    hw = [
        ("ESP32 DevKit v1", "Dual-core 240MHz microcontroller with hardware TLS crypto engine."),
        ("Red LED Actuator", "Anode connected to digital GPIO 23."),
        ("220Ω Limiting Resistor", "Protects LED & ensures stable 3.3V GPIO operation."),
        ("Status Blue LED", "GPIO 2 indicates Wi-Fi connectivity and handshake status.")
    ]
    for title, desc in hw:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s10, "esp32_macro_render.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    add_speaker_notes(s10, "SPEAKER NOTES - P. Sachin: I am P. Sachin, responsible for hardware wiring and firmware...")

    # =========================================================================
    # SLIDE 11: Firmware Finite State Machine
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_background(s11)
    add_header(s11, "ESP32 C++ FreeRTOS Firmware Engine", "FIRMWARE ARCHITECTURE")

    add_fitted_image(s11, "state_machine_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Millis() FSM State Machine"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    states = [
        ("STATE_SECURE 🟢", "System Idle. Red LED solid OFF."),
        ("STATE_ALERT 🔴", "Public S3 detected. Red LED blinks rapidly (200ms)."),
        ("STATE_DISCONNECTED 🟡", "Network drop. Red LED pulses slowly (1000ms)."),
        ("Non-Blocking Execution", "Driven by millis() timers; zero blocking delay() calls.")
    ]
    for st, desc in states:
        p = tf.add_paragraph()
        p.text = f"•  {st}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s11, "SPEAKER NOTES - P. Sachin: Our C++ firmware uses a non-blocking millis() state machine...")

    # =========================================================================
    # SLIDE 12: Interactive Web Dashboard Twin
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_background(s12)
    add_header(s12, "Interactive Glassmorphism Digital Twin UI", "DIGITAL TWIN UI")

    draw_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Digital Twin Features"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    dash = [
        ("Dark Glassmorphism UI", "Styled with CSS backdrop blur, neon glow highlights, and reactive cards."),
        ("Simulated Virtual LED", "Pulsating neon red LED flashes synchronously with physical hardware."),
        ("Live Audit Event Log", "Renders history of scanned bucket names, timestamps, and severity levels."),
        ("Interactive Test Harness", "Enables students & teachers to trigger scan tests directly from browser.")
    ]
    for t, d in dash:
        p = tf.add_paragraph()
        p.text = f"•  {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s12, "neon_dashboard_screen.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s12, "SPEAKER NOTES - D. Chander: Our web dashboard acts as a live digital twin...")

    # =========================================================================
    # SLIDE 13: Conclusion & Key Achievements
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_background(s13)
    add_header(s13, "Conclusion & Key System Achievements", "CONCLUSION")

    draw_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key System Achievements"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    achieve = [
        ("Sub-Second Physical Awareness", "Eliminated cloud incident response lag by bringing alert light into physical space."),
        ("Zero-Trust Hardware mTLS 1.2", "Protected IoT endpoints using X.509 client certificates and scoped IAM policies."),
        ("100% Automated Deployment", "1-Click deployer script provisions full AWS stack in under 60 seconds."),
        ("Real-Time Digital Twin", "Synchronized physical micro-controller state with interactive web dashboard via WebSockets.")
    ]
    for t, d in achieve:
        p = tf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED

    add_fitted_image(s13, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s13, "SPEAKER NOTES - D. Chander: In conclusion, our Cloud Security Alert Lamp demonstrates Defense in Depth...")

    # Save to all target paths
    out_paths = [
        "docs/Cloud_Security_Alert_Lamp_Presentation.pptx",
        "docs/Cloud_Security_Alert_Lamp_Minimal.pptx",
        "docs/Cloud_Security_Alert_Lamp_Executive.pptx"
    ]
    for pth in out_paths:
        try:
            prs.save(pth)
            print(f"[+] Successfully saved Executive Clean Deck to: {pth}")
        except PermissionError:
            alt = pth.replace(".pptx", "_clean.pptx")
            prs.save(alt)
            print(f"[+] Saved to clean path: {alt}")

if __name__ == "__main__":
    create_executive_clean_deck()
