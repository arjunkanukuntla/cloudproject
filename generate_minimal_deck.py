import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_apple_style_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Keynote Dark Luxury Theme Colors
    BG = RGBColor(8, 12, 20)           # #080C14 Pitch Dark Navy
    CARD_BG = RGBColor(17, 24, 39)      # #111827 Dark Slate Card
    CARD_BORDER = RGBColor(31, 41, 55)  # #1F2937 Minimal Border
    CYAN = RGBColor(0, 240, 255)       # #00F0FF Glowing Electric Cyan
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

    def add_top_bar(slide, tag_text, title_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
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

    def add_image_card(slide, img_name, left, top, width, height, border_color=CYAN):
        img_path = os.path.join(assets_dir, img_name)
        if os.path.exists(img_path):
            draw_card(slide, left - Inches(0.05), top - Inches(0.05), width + Inches(0.1), height + Inches(0.1), border_color=border_color)
            return slide.shapes.add_picture(img_path, left, top, width, height)
        return None

    # =========================================================================
    # SLIDE 1: Title Slide & Visual Hero
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Left text info (50% width)
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.0), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CLOUD SECURITY ALERT LAMP 🚨💡"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p_sub = tf1.add_paragraph()
    p_sub.text = "Real-Time Cyber-Physical Alerting for AWS S3 Bucket Exposure"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(8)

    # Team Grid (4 compact pill cards)
    team = [
        ("D. Chander", "2503A52214", "Lead & Dashboard"),
        ("K. Arjun", "2503A52235", "Backend & Database"),
        ("G. Rohan", "2503S52224", "Architecture & Security"),
        ("P. Sachin", "2503A52240", "Hardware & Firmware")
    ]
    for idx, (name, roll, role) in enumerate(team):
        p_t = tf1.add_paragraph()
        p_t.text = f"{name} ({roll}) — {role}"
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = MUTED
        p_t.space_before = Pt(10 if idx==0 else 4)

    # Right Hero Image
    add_image_card(s1, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.2), Inches(5.7), Inches(5.0), border_color=CYAN)

    # =========================================================================
    # SLIDE 2: The Problem: S3 Leaks & Alert Fatigue
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_top_bar(s2, "Problem Statement", "S3 Data Leaks & Email Alert Fatigue")

    # Card 1: Mass Risk
    draw_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "$4.45 Million"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = RED

    p_sub = tf.add_paragraph()
    p_sub.text = "Average Enterprise Cloud Data Breach Cost"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(4)

    bullets1 = [
        "Accidental Public S3 Buckets",
        "Scanners Exploit Leaks in Seconds",
        "Dev Exposure Causes Mass Leaks"
    ]
    for b in bullets1:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # Card 2: Alert Fatigue
    draw_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "> 14 Hours"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p_sub = tf.add_paragraph()
    p_sub.text = "Average Time to Detect Silent S3 Leaks"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = WHITE
    p_sub.space_before = Pt(4)

    bullets2 = [
        "500+ Security Emails Daily",
        "Critical Warnings Get Ignored",
        "Zero Physical Desk Awareness"
    ]
    for b in bullets2:
        p = tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: The Solution: Cyber-Physical Lamp & Web Twin
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_top_bar(s3, "The Solution", "Sub-Second Cyber-Physical Desk Alerting")

    # Left Image
    add_image_card(s3, "cloud_pipeline_3d.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    # Right Content Card
    draw_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "< 1 Second Alert Latency"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = GREEN

    features = [
        ("🔴 Physical Desk Actuator", "Red LED blinks rapidly on engineer's desk."),
        ("⚡ AWS Serverless Scanning", "Lambda boto3 inspects policies instantly."),
        ("🔒 Mutual TLS Security", "Encrypted MQTT telemetry over port 8883."),
        ("🌐 Web Twin Dashboard", "Live WebSocket state synchronization.")
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
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 4: Architecture Pipeline (4 Minimal Flow Cards)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_top_bar(s4, "System Architecture", "4-Stage Event-Driven Pipeline")

    stages = [
        ("STAGE 1", "AWS Lambda Scanner", CYAN, "Audits S3 Policies & ACLs\nGenerates Risk JSON"),
        ("STAGE 2", "DynamoDB & SNS", GREEN, "Logs Security Event\nDispatches SMS/Email"),
        ("STAGE 3", "AWS IoT Core Broker", CYAN, "MQTT over TLS 1.2\nX.509 Device Auth"),
        ("STAGE 4", "ESP32 & Web Twin", RED, "Flashes Red LED 🔴\nWebSocket UI Sync")
    ]

    card_w = Inches(2.7)
    gap = Inches(0.25)
    left_start = Inches(0.8)

    for idx, (stg, title, color, desc) in enumerate(stages):
        c_left = left_start + idx * (card_w + gap)
        draw_card(s4, c_left, Inches(1.8), card_w, Inches(4.8), border_color=color)

        tb = s4.shapes.add_textbox(c_left + Inches(0.12), Inches(2.0), card_w - Inches(0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_stg = tf.paragraphs[0]
        p_stg.text = stg
        p_stg.font.size = Pt(11)
        p_stg.font.bold = True
        p_stg.font.color.rgb = color

        p_ttl = tf.add_paragraph()
        p_ttl.text = title
        p_ttl.font.size = Pt(15)
        p_ttl.font.bold = True
        p_ttl.font.color.rgb = WHITE
        p_ttl.space_before = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = MUTED
        p_desc.space_before = Pt(14)

    # =========================================================================
    # SLIDE 5: Tech Stack Engine (4 Grid Tiles)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_top_bar(s5, "Technology Stack", "Core Frameworks & Tools Used")

    tech_tiles = [
        ("AWS Serverless Scanner", "Python Lambda & Boto3", CYAN, ["3-Layer Policy Audit", "PublicAccessBlock Check", "Zero Server Overhead"]),
        ("Data & Messaging", "DynamoDB, SNS & IoT Core", GREEN, ["NoSQL Audit History", "Push SMS & Email Alerts", "TLS 1.2 MQTT Messaging"]),
        ("Backend & Web Twin", "FastAPI & WebSockets", CYAN, ["Async Event Engine", "REST API Dashboard", "Glassmorphic Web UI"]),
        ("Physical Hardware", "ESP32 & C++ FreeRTOS", RED, ["Dual-Core 240MHz MCU", "Millis Timer FSM", "X.509 SPIFFS Storage"])
    ]

    for idx, (cat, title, color, points) in enumerate(tech_tiles):
        row = idx // 2
        col = idx % 2
        l = Inches(0.8) if col == 0 else Inches(6.8)
        t = Inches(1.8) if row == 0 else Inches(4.3)
        w = Inches(5.7)
        h = Inches(2.3)

        draw_card(s5, l, t, w, h, border_color=color)

        tb = s5.shapes.add_textbox(l + Inches(0.15), t + Inches(0.15), w - Inches(0.3), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = cat.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = color

        p_ttl = tf.add_paragraph()
        p_ttl.text = title
        p_ttl.font.size = Pt(16)
        p_ttl.font.bold = True
        p_ttl.font.color.rgb = WHITE
        p_ttl.space_before = Pt(2)

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = f"• {pt}"
            p_pt.font.size = Pt(10)
            p_pt.font.color.rgb = MUTED
            p_pt.space_before = Pt(2)

    # =========================================================================
    # SLIDE 6: Security & Zero-Trust mTLS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_top_bar(s6, "Security Architecture", "Zero-Trust X.509 Mutual TLS Encryption")

    add_image_card(s6, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TLS 1.2 & X.509 Certs"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = GREEN

    sec_bullets = [
        ("Mutual Authentication", "ESP32 validates Amazon Root CA 1."),
        ("Hardware Identity", "X.509 Certificate stored on device SPIFFS."),
        ("Encrypted Transport", "Port 8883 MQTT prevents packet sniffing."),
        ("Scoped IAM Policy", "Device restricted strictly to alert topic.")
    ]
    for t, d in sec_bullets:
        p = tf.add_paragraph()
        p.text = f"•  {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

        p_d = tf.add_paragraph()
        p_d.text = f"   {d}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    # =========================================================================
    # SLIDE 7: Live Classroom Demo Flow
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_top_bar(s7, "Classroom Demo", "4-Step Security Breach Test Flow")

    demo_steps = [
        ("STEP 1", "Baseline Secure", GREEN, "System Idle\nLED Solid OFF 🟢"),
        ("STEP 2", "Create S3 Leak", RED, "Run test script\nPublic S3 Created"),
        ("STEP 3", "Instant Alert", RED, "LED Blinks Rapidly 🔴\nWeb UI Alert"),
        ("STEP 4", "Auto Cleanup", CYAN, "Delete S3 Bucket\nLED Turns OFF 🟢")
    ]

    for idx, (step, title, color, desc) in enumerate(demo_steps):
        c_left = left_start + idx * (card_w + gap)
        draw_card(s7, c_left, Inches(1.8), card_w, Inches(4.8), border_color=color)

        tb = s7.shapes.add_textbox(c_left + Inches(0.12), Inches(2.0), card_w - Inches(0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_stg = tf.paragraphs[0]
        p_stg.text = step
        p_stg.font.size = Pt(11)
        p_stg.font.bold = True
        p_stg.font.color.rgb = color

        p_ttl = tf.add_paragraph()
        p_ttl.text = title
        p_ttl.font.size = Pt(15)
        p_ttl.font.bold = True
        p_ttl.font.color.rgb = WHITE
        p_ttl.space_before = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = MUTED
        p_desc.space_before = Pt(14)

    # =========================================================================
    # SLIDE 8: Key Takeaways & Q&A
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_top_bar(s8, "Summary & Jury Q&A", "Key Takeaways & Technical Defense")

    draw_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Achievements"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    takeaways = [
        "Sub-Second Physical Awareness",
        "Zero-Trust Hardware mTLS 1.2",
        "100% Automated 1-Click Deployer",
        "Real-Time WebSocket Digital Twin"
    ]
    for t in takeaways:
        p = tf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(12)

    draw_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Jury Q&A Defense"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    qa = [
        ("Wi-Fi Loss?", "Pulses slowly (1000ms) & auto-reconnects."),
        ("Spoofing Risk?", "Blocked by X.509 Client Cert mTLS."),
        ("AWS Student Ready?", "Auto-detects $50 Learner Lab LabRole.")
    ]
    for q, a in qa:
        p = tf.add_paragraph()
        p.text = f"Q: {q}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_a = tf.add_paragraph()
        p_a.text = f"A: {a}"
        p_a.font.size = Pt(11)
        p_a.font.color.rgb = MUTED

    # Save presentation
    paths = ["docs/Cloud_Security_Alert_Lamp_Presentation.pptx", "docs/Cloud_Security_Alert_Lamp_Minimal.pptx"]
    for pth in paths:
        try:
            prs.save(pth)
            print(f"[+] Successfully saved Apple-Style Minimal Deck to: {pth}")
        except PermissionError:
            print(f"[-] Could not overwrite {pth} (file in use), skipping.")

if __name__ == "__main__":
    create_apple_style_deck()
