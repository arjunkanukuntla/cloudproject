import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_evaluation_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Keynote Dark Luxury Theme
    BG = RGBColor(11, 15, 25)           # #0B0F19 Dark Navy
    CARD_BG = RGBColor(22, 30, 46)        # #161E2E Slate Card
    CARD_BORDER = RGBColor(45, 60, 88)    # #2D3C58 Card Border
    CYAN = RGBColor(6, 182, 212)          # #06B6D4 Electric Cyan
    RED = RGBColor(239, 68, 68)           # #EF4444 Crimson Alert
    GREEN = RGBColor(34, 197, 94)         # #22C55E Emerald Green
    WHITE = RGBColor(248, 250, 252)       # Crisp White
    MUTED = RGBColor(148, 163, 184)     # Slate Gray

    blank_layout = prs.slide_layouts[6]
    assets_dir = r"c:\cloud project\docs\assets"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG
        bg.line.fill.background()

    def add_top_bar(slide, tag_text, title_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN
        p_tag.font.name = "Arial"

        p_ttl = tf.add_paragraph()
        p_ttl.text = title_text
        p_ttl.font.size = Pt(24)
        p_ttl.font.bold = True
        p_ttl.font.color.rgb = WHITE
        p_ttl.font.name = "Arial"
        p_ttl.space_before = Pt(2)

    def draw_card(slide, left, top, width, height, border_color=CARD_BORDER, bg_color=CARD_BG):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    def add_fitted_image(slide, img_name, left, top, width, height, border_color=CYAN):
        draw_card(slide, left, top, width, height, border_color=border_color, bg_color=CARD_BG)
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            pad = Inches(0.1)
            return slide.shapes.add_picture(img_path, left + pad, top + pad, width = width - (2*pad), height = height - (2*pad))
        return None

    def add_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Title Slide & Author Domain Allocation
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CLOUD SECURITY ALERT LAMP 🚨💡"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "Real-Time Cyber-Physical Alert System & Digital Twin for AWS S3 Exposures"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(4)

    # 4 Team Cards mapping Product, AWS, Backend, Frontend/HW
    authors = [
        ("D. Chander", "2503A52214", "PRODUCT OVERVIEW", "Product Concept & S3 Leak Dangers"),
        ("G. Rohan", "2503S52224", "AWS SERVICES & SECURITY", "Lambda, IoT Core mTLS & IAM"),
        ("K. Arjun", "2503A52235", "BACKEND & DATABASE", "FastAPI, DynamoDB & SNS Alerts"),
        ("P. Sachin", "2503A52240", "FRONTEND & HARDWARE", "Web Twin UI & ESP32 Firmware")
    ]

    card_w = Inches(2.7)
    gap = Inches(0.25)
    left_start = Inches(0.8)

    for idx, (name, roll, domain, desc) in enumerate(authors):
        c_left = left_start + idx * (card_w + gap)
        draw_card(s1, c_left, Inches(2.4), card_w, Inches(4.3), border_color=CYAN)

        tb = s1.shapes.add_textbox(c_left + Inches(0.12), Inches(2.55), card_w - Inches(0.24), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p_name = tf.paragraphs[0]
        p_name.text = name
        p_name.font.size = Pt(16)
        p_name.font.bold = True
        p_name.font.color.rgb = WHITE

        p_roll = tf.add_paragraph()
        p_roll.text = f"Roll: {roll}"
        p_roll.font.size = Pt(11)
        p_roll.font.color.rgb = MUTED

        p_dom = tf.add_paragraph()
        p_dom.text = domain
        p_dom.font.size = Pt(11)
        p_dom.font.bold = True
        p_dom.font.color.rgb = GREEN
        p_dom.space_before = Pt(12)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = WHITE
        p_desc.space_before = Pt(4)

    add_speaker_notes(s1, "SPEAKER NOTES - D. Chander: Good morning evaluators. Today our team presents the Cloud Security Alert Lamp. All 4 team members will present their technical domain: Product Overview by Chander, AWS Services & Security by Rohan, Backend & Database by Arjun, and Frontend & Hardware by Sachin.")

    # =========================================================================
    # SLIDE 2: PRODUCT OVERVIEW & CONCEPT (D. Chander)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_top_bar(s2, "PRODUCT OVERVIEW — PRESENTED BY D. CHANDER", "The Cyber-Physical Alert Product Concept")

    draw_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Product Innovation & Value"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    product_points = [
        ("Sub-Second Desk Actuation", "Bridges AWS Cloud security auditing directly with physical ESP32 LED hardware on an engineer's desk."),
        ("Ambient Threat Awareness", "Converts silent, easily ignored security emails into an instant, un-ignorable physical Red flashing LED."),
        ("Dual Alert Ecosystem", "Features both physical IoT desk hardware and an interactive real-time Web Dashboard Digital Twin."),
        ("Enterprise Risk Reduction", "Prevents catastrophic data leaks by cutting mean-time-to-detection from > 14 hours to < 1 second.")
    ]
    for title, desc in product_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s2, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s2, "SPEAKER NOTES - D. Chander: I am D. Chander, explaining our product vision. In cloud infrastructure, accidental public exposure of S3 buckets causes severe data breaches. Our product bridges AWS Cloud auditing with physical hardware: when a public S3 bucket is created, a Red LED blinks rapidly on the engineer's desk.")

    # =========================================================================
    # SLIDE 3: AWS SERVICES USED MATRIX (G. Rohan)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_top_bar(s3, "AWS SERVICES USED — PRESENTED BY G. ROHAN", "Comprehensive AWS Cloud Infrastructure Breakdown")

    aws_services = [
        ("AWS Lambda", "Serverless Auditor", CYAN, ["Runs Python boto3 S3 scanner", "Triggered by API / Schedule", "Zero server management"]),
        ("Amazon DynamoDB", "NoSQL Database", GREEN, ["Stores SecurityEvents table", "Partition Key: eventId", "PAY_PER_REQUEST auto-scaling"]),
        ("Amazon SNS", "Push Notifications", CYAN, ["CloudSecurityAlerts topic", "Dispatches SMS & emails", "Instant admin alert push"]),
        ("AWS IoT Core", "MQTT Message Broker", RED, ["TLS 1.2 on Port 8883", "X.509 Mutual Certificate Auth", "Topic: cloud/security/alert"])
    ]

    for idx, (service, role, color, points) in enumerate(aws_services):
        row = idx // 2
        col = idx % 2
        l = Inches(0.8) if col == 0 else Inches(6.8)
        t = Inches(1.8) if row == 0 else Inches(4.3)
        w = Inches(5.7)
        h = Inches(2.3)

        draw_card(s3, l, t, w, h, border_color=color)

        tb = s3.shapes.add_textbox(l + Inches(0.15), t + Inches(0.15), w - Inches(0.3), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = service
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.text = role.upper()
        p_sub.font.size = Pt(9)
        p_sub.font.bold = True
        p_sub.font.color.rgb = WHITE
        p_sub.space_before = Pt(1)

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = f"•  {pt}"
            p_pt.font.size = Pt(10)
            p_pt.font.color.rgb = MUTED
            p_pt.space_before = Pt(2)

    add_speaker_notes(s3, "SPEAKER NOTES - G. Rohan: Good morning professors, I am G. Rohan. Here is our AWS Cloud service matrix: we use AWS Lambda for serverless scanning, DynamoDB for event history, SNS for push alerts, and AWS IoT Core for secure MQTT messaging.")

    # =========================================================================
    # SLIDE 4: AWS CLOUD DEEP DIVE — LAMBDA AUDITOR (G. Rohan)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_top_bar(s4, "AWS CLOUD DEEP DIVE — PRESENTED BY G. ROHAN", "AWS Lambda 3-Layer S3 Security Auditor")

    add_fitted_image(s4, "security_layers_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Lambda boto3 3-Layer Audit"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RED

    audit_layers = [
        ("Layer 1: Public Access Block", "Calls GetPublicAccessBlock. Flagged if any of 4 block parameters are False."),
        ("Layer 2: Bucket Policy Status", "Queries GetBucketPolicyStatus. Flagged if IsPublic == True or wildcard Principal: '*'."),
        ("Layer 3: S3 ACL Access Grants", "Parses GetBucketAcl. Flagged if AllUsers or AuthenticatedUsers URI exists.")
    ]
    for lyr, desc in audit_layers:
        p = tf.add_paragraph()
        p.text = f"•  {lyr}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_speaker_notes(s4, "SPEAKER NOTES - G. Rohan: S3 bucket publicity occurs via 3 vectors: Public Access Block configuration, JSON bucket policies, or S3 ACL grants. Our Lambda function audits all 3 layers.")

    # =========================================================================
    # SLIDE 5: AWS CLOUD DEEP DIVE — IOT CORE & SECURITY (G. Rohan)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_top_bar(s5, "AWS CLOUD DEEP DIVE — PRESENTED BY G. ROHAN", "AWS IoT Core Mutual TLS 1.2 & IAM Security")

    add_fitted_image(s5, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Zero-Trust IoT Security"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    iot_sec = [
        ("Mutual Authentication (mTLS)", "ESP32 validates Amazon Root CA 1; AWS IoT validates hardware client X.509 cert."),
        ("X.509 Certificate Storage", "RSA 2048-bit keypair stored on ESP32 SPIFFS memory."),
        ("TLS 1.2 Encrypted MQTT", "Port 8883 connection prevents payload sniffing or packet injection."),
        ("Scoped IAM Policy", "Restricts hardware client strictly to topic 'cloud/security/alert'.")
    ]
    for title, desc in iot_sec:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_speaker_notes(s5, "SPEAKER NOTES - G. Rohan: We enforce Zero Trust security on hardware: the ESP32 connects over port 8883 using X.509 mutual TLS authentication.")

    # =========================================================================
    # SLIDE 6: BACKEND ARCHITECTURE — FASTAPI (K. Arjun)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_top_bar(s6, "BACKEND ARCHITECTURE — PRESENTED BY K. ARJUN", "FastAPI Asynchronous Application & REST API Layer")

    draw_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FastAPI Python Core"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    be_points = [
        ("Asynchronous Event Loop", "Built on Python's asyncio & uvicorn for high concurrency."),
        ("REST API Endpoints", "Exposes /api/dashboard, /api/events, and /api/scan for frontend UI."),
        ("WebSocket Engine (/ws)", "Maintains persistent WebSocket connections to stream live updates to Web Twin.")
    ]
    for title, desc in be_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s6, "cyber_alert_desk.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s6, "SPEAKER NOTES - K. Arjun: I am K. Arjun, handling backend and database infrastructure. Our server is built on FastAPI using asynchronous event loops...")

    # =========================================================================
    # SLIDE 7: BACKEND STORAGE & NOTIFICATIONS (K. Arjun)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_top_bar(s7, "BACKEND STORAGE — PRESENTED BY K. ARJUN", "Amazon DynamoDB Persistence & SNS Push Alerts")

    draw_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=GREEN)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DynamoDB 'SecurityEvents'"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    db_points = [
        ("NoSQL Event Log", "Stores immutable audit history of all S3 scan events."),
        ("Key Schema", "Partition Key: eventId (S) | Range Key: timestamp (S)."),
        ("On-Demand Auto Scaling", "PAY_PER_REQUEST billing auto-scales seamlessly.")
    ]
    for title, desc in db_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    draw_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Amazon SNS Dispatcher"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    sns_points = [
        ("Multi-Channel Push Alerts", "Dispatches instant SMS and email notifications."),
        ("CloudSecurityAlerts Topic", "Manages security team subscriber lists."),
        ("Zero Latency Delivery", "Pushes alerts concurrently with IoT MQTT payloads.")
    ]
    for title, desc in sns_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_speaker_notes(s7, "SPEAKER NOTES - K. Arjun: Every breach event is persisted in DynamoDB and pushed via Amazon SNS...")

    # =========================================================================
    # SLIDE 8: FRONTEND ARCHITECTURE — WEB TWIN (P. Sachin)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_top_bar(s8, "FRONTEND ARCHITECTURE — PRESENTED BY P. SACHIN", "Interactive Glassmorphism Digital Twin UI")

    draw_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Web Twin Dashboard UI"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    fe_points = [
        ("Dark Glassmorphism UI", "Styled with CSS backdrop blur, neon glow highlights, and reactive cards."),
        ("Simulated Virtual Lamp", "Pulsating neon red LED flashes synchronously with physical hardware."),
        ("Live WebSocket Sync", "Receives real-time state frames from backend WebSocket server (/ws)."),
        ("Interactive Test Harness", "Enables students & teachers to trigger scan tests directly from browser.")
    ]
    for title, desc in fe_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s8, "neon_dashboard_screen.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_speaker_notes(s8, "SPEAKER NOTES - P. Sachin: I am P. Sachin, explaining the Frontend Web Twin and Hardware. Our web UI provides a real-time digital twin of the hardware lamp...")

    # =========================================================================
    # SLIDE 9: HARDWARE ENGINEERING & FIRMWARE (P. Sachin)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_top_bar(s9, "HARDWARE ENGINEERING — PRESENTED BY P. SACHIN", "ESP32 Wiring & FreeRTOS Firmware Engine")

    draw_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Hardware Wiring & BOM"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN

    hw_points = [
        ("ESP32 DevKit v1", "Dual-core 240MHz MCU with hardware TLS crypto engine."),
        ("Red LED Actuator", "Anode connected to digital GPIO 23."),
        ("220Ω Limiting Resistor", "Protects LED & ensures stable 3.3V GPIO operation.")
    ]
    for title, desc in hw_points:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s9, "esp32_macro_render.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    add_speaker_notes(s9, "SPEAKER NOTES - P. Sachin: Our hardware uses an ESP32 connected to a high-brightness Red LED...")

    # =========================================================================
    # SLIDE 10: LIVE DEMONSTRATION & CONCLUSION (All Team Members)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_top_bar(s10, "LIVE DEMO & CONCLUSION — ALL TEAM MEMBERS", "4-Step Product Test Flow & System Achievements")

    draw_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Live Demo Test Flow"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RED

    demo_steps = [
        ("1. Baseline", "System in SECURE state. Red LED solid OFF 🟢."),
        ("2. Breach", "Run: python test_vulnerable_bucket.py create."),
        ("3. Actuation", "Red LED blinks rapidly (200ms) 🔴. Web UI turns ALERT."),
        ("4. Remediation", "Run: python test_vulnerable_bucket.py delete. LED turns OFF 🟢.")
    ]
    for stg, desc in demo_steps:
        p = tf.add_paragraph()
        p.text = f"•  {stg}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    draw_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key System Achievements"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN

    achieve = [
        ("Sub-Second Physical Awareness", "Bridges AWS Cloud scanning with desk hardware."),
        ("Zero-Trust Security", "X.509 client certs & TLS 1.2 port 8883 MQTT."),
        ("100% Automated Deployment", "1-Click python deploy_aws.py script (< 60s)."),
        ("Real-Time Digital Twin", "FastAPI WebSocket UI state synchronization.")
    ]
    for title, desc in achieve:
        p = tf.add_paragraph()
        p.text = f"✔  {title}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_speaker_notes(s10, "SPEAKER NOTES - All Members: That concludes our live demonstration and project review presentation. Thank you evaluators.")

    # Save to PowerPoint presentation files
    out_paths = [
        "docs/Cloud_Security_Alert_Lamp_Presentation.pptx",
        "docs/Cloud_Security_Alert_Lamp_Minimal.pptx",
        "docs/Cloud_Security_Alert_Lamp_Executive.pptx"
    ]
    for pth in out_paths:
        try:
            prs.save(pth)
            print(f"[+] Successfully saved Evaluation Deck to: {pth}")
        except PermissionError:
            alt = pth.replace(".pptx", "_eval.pptx")
            prs.save(alt)
            print(f"[+] Saved to eval path: {alt}")

if __name__ == "__main__":
    create_evaluation_deck()
