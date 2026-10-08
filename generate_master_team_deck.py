import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_team_presentation_decks():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Keynote Pitch Dark Palette
    BG = RGBColor(8, 12, 20)           # #080C14 Pitch Dark Navy
    CARD_BG = RGBColor(17, 24, 39)      # #111827 Dark Slate Card
    CARD_BORDER = RGBColor(31, 41, 55)  # #1F2937 Minimal Border
    CYAN = RGBColor(0, 240, 255)       # #00F0FF Electric Cyan
    RED = RGBColor(255, 51, 102)       # #FF3366 Crimson Alert
    GREEN = RGBColor(0, 230, 118)      # #00E676 Vivid Emerald
    WHITE = RGBColor(255, 255, 255)    # Crisp White
    MUTED = RGBColor(156, 163, 175)    # #9CA3AF Readable Gray

    blank_layout = prs.slide_layouts[6]
    assets_dir = r"c:\cloud project\docs\assets"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG
        bg.line.fill.background()

    def add_top_bar(slide, speaker_tag, slide_title):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        p_tag.text = speaker_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN
        p_tag.font.name = "Arial"

        p_ttl = tf.add_paragraph()
        p_ttl.text = slide_title
        p_ttl.font.size = Pt(23)
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
        # Draw bounding card container
        draw_card(slide, left, top, width, height, border_color=border_color, bg_color=CARD_BG)
        
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            # Inset image inside the card container with padding to ensure perfect fit
            pad = Inches(0.1)
            img_left = left + pad
            img_top = top + pad
            img_width = width - (2 * pad)
            img_height = height - (2 * pad)
            return slide.shapes.add_picture(img_path, img_left, img_top, width=img_width, height=img_height)
        return None

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Title Slide & Team Roster
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CLOUD SECURITY ALERT LAMP 🚨💡"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "Real-Time Cyber-Physical Alerting for AWS S3 Bucket Exposure"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(4)

    # 4 Team Cards across middle
    members = [
        ("01", "D. Chander", "2503A52214", "Lead & Dashboard", ["• Problem & Motivation", "• Email Fatigue Bottleneck", "• Web Twin UI"]),
        ("02", "G. Rohan", "2503S52224", "Architecture & Security", ["• 4-Stage Data Pipeline", "• Lambda 3-Layer Auditor", "• X.509 Mutual TLS"]),
        ("03", "K. Arjun", "2503A52235", "Backend & Database", ["• FastAPI Server & REST", "• DynamoDB Audit Logging", "• 1-Click AWS Deployer"]),
        ("04", "P. Sachin", "2503A52240", "Hardware & Firmware", ["• ESP32 Circuit Wiring", "• FreeRTOS State Machine", "• Live Breach Demo Flow"])
    ]

    card_w = Inches(2.7)
    gap = Inches(0.25)
    left_start = Inches(0.8)

    for idx, (num, name, roll, role, bullets) in enumerate(members):
        c_left = left_start + idx * (card_w + gap)
        draw_card(s1, c_left, Inches(1.9), card_w, Inches(5.0), border_color=CYAN)

        tb = s1.shapes.add_textbox(c_left + Inches(0.12), Inches(2.05), card_w - Inches(0.24), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(20)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN

        p_name = tf.add_paragraph()
        p_name.text = name
        p_name.font.size = Pt(15)
        p_name.font.bold = True
        p_name.font.color.rgb = WHITE
        p_name.space_before = Pt(4)

        p_roll = tf.add_paragraph()
        p_roll.text = f"Roll: {roll}"
        p_roll.font.size = Pt(11)
        p_roll.font.color.rgb = MUTED

        p_role = tf.add_paragraph()
        p_role.text = role
        p_role.font.size = Pt(11)
        p_role.font.bold = True
        p_role.font.color.rgb = GREEN
        p_role.space_before = Pt(8)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = WHITE
            p_b.space_before = Pt(4)

    add_notes(s1, "SPEAKER NOTES: Welcome evaluators. Today we present the Cloud Security Alert Lamp...")

    # =========================================================================
    # SECTION 1: D. CHANDER (SLIDES 2, 3, 4)
    # =========================================================================

    # SLIDE 2: D. Chander - Problem Statement
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_top_bar(s2, "SECTION 1: D. CHANDER (1/3) — PROBLEM STATEMENT", "S3 Data Leaks & Email Alert Fatigue")

    draw_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
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
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(4)

    bullets = ["Accidental Public S3 Buckets", "Scanners Exploit Leaks in Seconds", "Dev Misconfigurations Expose PII"]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    add_fitted_image(s2, "data_leak_concept.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    add_notes(s2, "SPEAKER NOTES - D. Chander: S3 publicity is a catastrophic cloud risk...")

    # SLIDE 3: D. Chander - Email Fatigue & Detection Lag
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_top_bar(s3, "SECTION 1: D. CHANDER (2/3) — MOTIVATION", "Email Alert Fatigue & Detection Latency")

    draw_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "> 14 Hours"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p_sub = tf.add_paragraph()
    p_sub.text = "Average Time to Detect Silent S3 Leaks"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(4)

    bullets = ["500+ Security Emails Daily", "Critical Alerts Get Buried", "Zero Physical Desk Awareness"]
    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    add_fitted_image(s3, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_notes(s3, "SPEAKER NOTES - D. Chander: Email notifications create alert fatigue...")

    # SLIDE 4: D. Chander - Web Twin Dashboard UI
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_top_bar(s4, "SECTION 1: D. CHANDER (3/3) — DIGITAL TWIN", "Interactive Web Twin Dashboard UI")

    draw_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Glassmorphism UI"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = CYAN

    features = [
        ("Simulated Neon Lamp", "Pulsating virtual LED syncs with physical lamp."),
        ("Real-Time WebSockets", "Pushes instantaneous state updates to UI."),
        ("Interactive Test Controls", "Trigger simulated scans & remediation in browser.")
    ]
    for title, desc in features:
        p = tf.add_paragraph()
        p.text = f"•  {title}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s4, "neon_dashboard_screen.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_notes(s4, "SPEAKER NOTES - D. Chander: Our Web Twin Dashboard mirrors physical hardware...")

    # =========================================================================
    # SECTION 2: G. ROHAN (SLIDES 5, 6, 7)
    # =========================================================================

    # SLIDE 5: G. Rohan - Architecture Pipeline
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_top_bar(s5, "SECTION 2: G. ROHAN (1/3) — ARCHITECTURE", "4-Stage Event-Driven Pipeline")

    add_fitted_image(s5, "cloud_pipeline_3d.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "< 1 Second Latency"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = GREEN

    stages = [
        ("1. Detection", "AWS Lambda boto3 scans S3 policies."),
        ("2. Storage", "DynamoDB logs event & SNS emails alert."),
        ("3. Dispatch", "AWS IoT Core publishes payload over MQTT."),
        ("4. Actuation", "ESP32 flashes Red LED & Web Twin syncs.")
    ]
    for stg, desc in stages:
        p = tf.add_paragraph()
        p.text = f"•  {stg}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_notes(s5, "SPEAKER NOTES - G. Rohan: Here is our 4-stage decoupled pipeline...")

    # SLIDE 6: G. Rohan - AWS Lambda 3-Layer Auditor
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_top_bar(s6, "SECTION 2: G. ROHAN (2/3) — SCANNER ENGINE", "AWS Lambda 3-Layer Auditor (Boto3)")

    add_fitted_image(s6, "security_layers_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "3-Layer S3 Audit"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RED

    layers = [
        ("Layer 1: Public Access Block", "Checks if account-level blocks are enabled."),
        ("Layer 2: Bucket Policy Status", "Queries IsPublic == True or wildcard Principal: '*'."),
        ("Layer 3: S3 Access Control Lists", "Parses AllUsers / AuthenticatedUsers grants.")
    ]
    for lyr, desc in layers:
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

    add_notes(s6, "SPEAKER NOTES - G. Rohan: S3 publicity occurs via three distinct vectors...")

    # SLIDE 7: G. Rohan - Zero Trust X.509 Mutual TLS
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_top_bar(s7, "SECTION 2: G. ROHAN (3/3) — SECURITY", "Zero-Trust X.509 Mutual TLS Encryption")

    add_fitted_image(s7, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "mTLS 1.2 Security"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = GREEN

    sec = [
        ("Mutual Authentication", "ESP32 validates Amazon Root CA 1."),
        ("Hardware Cert Identity", "Client X.509 cert stored on SPIFFS."),
        ("Encrypted Transport", "Port 8883 MQTT prevents packet sniffing."),
        ("Scoped IAM Policy", "Restricts hardware client strictly to alert topic.")
    ]
    for title, desc in sec:
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

    add_notes(s7, "SPEAKER NOTES - G. Rohan: We enforce Zero-Trust mTLS on the hardware endpoint...")

    # =========================================================================
    # SECTION 3: K. ARJUN (SLIDES 8, 9, 10)
    # =========================================================================

    # SLIDE 8: K. Arjun - FastAPI Async Server
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_top_bar(s8, "SECTION 3: K. ARJUN (1/3) — BACKEND", "FastAPI Asynchronous Web Engine")

    draw_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FastAPI Framework"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = CYAN

    be = [
        ("High Concurrency Event Loop", "Asynchronous Python server handles high-throughput requests."),
        ("REST Endpoints Provided", "Exposes /api/dashboard, /api/events, and /api/scan."),
        ("WebSocket Broadcast", "Pushes real-time state frames directly to connected Web Twins.")
    ]
    for title, desc in be:
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

    add_fitted_image(s8, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_notes(s8, "SPEAKER NOTES - K. Arjun: I am K. Arjun, handling backend & database...")

    # SLIDE 9: K. Arjun - DynamoDB & SNS Dispatcher
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_top_bar(s9, "SECTION 3: K. ARJUN (2/3) — STORAGE & ALERTS", "Amazon DynamoDB & SNS Alert Engine")

    draw_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=GREEN)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DynamoDB 'SecurityEvents'"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = GREEN

    db = [
        ("NoSQL Audit Log", "Stores immutable scan records for historical analysis."),
        ("Key Schema", "Partition Key: eventId (S) | Range Key: timestamp (S)."),
        ("On-Demand Auto Scaling", "PAY_PER_REQUEST billing auto-scales effortlessly.")
    ]
    for title, desc in db:
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

    draw_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    tb = s9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Amazon SNS Dispatcher"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = CYAN

    sns = [
        ("Push Alert Broadcasting", "Dispatches instant SMS and email notifications."),
        ("Topic Configuration", "CloudSecurityAlerts SNS topic manages subscribers."),
        ("Zero Latency Delivery", "Pushes alerts simultaneously with IoT MQTT payloads.")
    ]
    for title, desc in sns:
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

    add_notes(s9, "SPEAKER NOTES - K. Arjun: Every breach event is persisted into DynamoDB...")

    # SLIDE 10: K. Arjun - 1-Click AWS Provisioner
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_top_bar(s10, "SECTION 3: K. ARJUN (3/3) — AUTOMATION", "1-Click AWS Provisioner (deploy_aws.py)")

    draw_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Automated Setup"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = CYAN

    prov = [
        ("Single Command Execution", "python cloud/deploy_aws.py provisions full stack."),
        ("Resource Creation", "Creates DynamoDB table, SNS topic, Lambda & IoT Thing."),
        ("Student Account Ready", "Auto-detects $50 AWS Learner Lab LabRole."),
        ("Cert Auto-Injection", "Populates firmware/include/secrets.h automatically.")
    ]
    for title, desc in prov:
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

    add_fitted_image(s10, "cloud_pipeline_3d.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    add_notes(s10, "SPEAKER NOTES - K. Arjun: Running deploy_aws.py automates infrastructure...")

    # =========================================================================
    # SECTION 4: P. SACHIN (SLIDES 11, 12, 13)
    # =========================================================================

    # SLIDE 11: P. Sachin - ESP32 Hardware Wiring & Schematic
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_top_bar(s11, "SECTION 4: P. SACHIN (1/3) — HARDWARE WIRING", "ESP32 Circuit Schematics & Hardware BOM")

    draw_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Hardware Schematics"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = CYAN

    hw = [
        ("ESP32 DevKit v1", "Dual-core 240MHz MCU with hardware TLS crypto engine."),
        ("Red LED Actuator", "Anode connected to digital GPIO 23."),
        ("220Ω Limiting Resistor", "Protects LED & ensures stable 3.3V GPIO operation."),
        ("Status Blue LED", "GPIO 2 indicates Wi-Fi handshake status.")
    ]
    for title, desc in hw:
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

    add_fitted_image(s11, "esp32_macro_render.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    add_notes(s11, "SPEAKER NOTES - P. Sachin: I am P. Sachin, handling ESP32 hardware...")

    # SLIDE 12: P. Sachin - Firmware Finite State Machine
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_top_bar(s12, "SECTION 4: P. SACHIN (2/3) — FIRMWARE ENGINE", "ESP32 C++ FreeRTOS Non-Blocking State Machine")

    add_fitted_image(s12, "state_machine_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s12.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Millis() FSM Engine"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = GREEN

    states = [
        ("STATE_SECURE 🟢", "System Idle. Red LED solid OFF."),
        ("STATE_ALERT 🔴", "Public S3 detected. Red LED blinks rapidly (200ms)."),
        ("STATE_DISCONNECTED 🟡", "Network drop. Red LED pulses slowly (1000ms)."),
        ("Non-Blocking Execution", "Uses millis() timers; zero blocking delay() calls.")
    ]
    for st, desc in states:
        p = tf.add_paragraph()
        p.text = f"•  {st}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_notes(s12, "SPEAKER NOTES - P. Sachin: Our C++ firmware uses a non-blocking millis() state machine...")

    # SLIDE 13: P. Sachin - Live Demo Flow & Q&A Conclusion
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_top_bar(s13, "SECTION 4: P. SACHIN (3/3) — LIVE DEMO & Q&A", "Live 4-Step Demonstration & Technical Q&A")

    draw_card(s13, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Live Demo Test Flow"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RED

    demo = [
        ("1. Baseline", "ESP32 connected to Wi-Fi. LED solid OFF 🟢."),
        ("2. Breach", "Run: python test_vulnerable_bucket.py create."),
        ("3. Actuation", "Red LED blinks rapidly (200ms) 🔴. Web UI Alert."),
        ("4. Remediation", "Run: python test_vulnerable_bucket.py delete. LED OFF 🟢.")
    ]
    for stg, desc in demo:
        p = tf.add_paragraph()
        p.text = f"•  {stg}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    draw_card(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s13.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Technical Jury Defense"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = GREEN

    qa = [
        ("Wi-Fi Connection Drop?", "Pulses slowly (1000ms) & executes auto-reconnect."),
        ("MQTT Spoofing Risk?", "Blocked by X.509 Client Cert mutual TLS."),
        ("AWS Student Ready?", "Auto-detects $50 Learner Lab LabRole.")
    ]
    for q, a in qa:
        p = tf.add_paragraph()
        p.text = f"Q: {q}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_a = tf.add_paragraph()
        p_a.text = f"A: {a}"
        p_a.font.size = Pt(10)
        p_a.font.color.rgb = MUTED

    add_notes(s13, "SPEAKER NOTES - P. Sachin & D. Chander: That concludes our presentation...")

    # Save presentation to unique paths to avoid PowerPoint file locks
    out_paths = [
        "docs/Cloud_Security_Alert_Lamp_Master_Team_Deck.pptx",
        "docs/Cloud_Security_Alert_Lamp_Minimal.pptx"
    ]
    for pth in out_paths:
        try:
            prs.save(pth)
            print(f"[+] Successfully saved Master 13-Slide Deck to: {pth}")
        except PermissionError:
            alt = pth.replace(".pptx", "_fresh.pptx")
            prs.save(alt)
            print(f"[+] Saved to fresh path: {alt}")

if __name__ == "__main__":
    build_team_presentation_decks()
