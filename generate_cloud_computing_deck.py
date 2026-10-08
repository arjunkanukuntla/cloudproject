import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_cloud_computing_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Sleek Dark Navy Palette for Cloud Computing
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

    # =========================================================================
    # SLIDE 1: Title Slide & Team Authors
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

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
    p_sub.font.color.rgb = WHITE
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(8)

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
        p_name.font.color.rgb = WHITE

        p_roll = tf.add_paragraph()
        p_roll.text = roll
        p_roll.font.size = Pt(12)
        p_roll.font.color.rgb = MUTED
        p_roll.space_before = Pt(4)

        p_role = tf.add_paragraph()
        p_role.text = role
        p_role.font.size = Pt(12)
        p_role.font.bold = True
        p_role.font.color.rgb = GREEN
        p_role.space_before = Pt(16)

    # =========================================================================
    # SLIDE 2: WHY (The Problem & Motivation)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_top_bar(s2, "WHY WE BUILT THIS PROJECT", "AWS S3 Exposure Dangers & Email Alert Fatigue")

    draw_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=RED)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Cloud Exposure Problem"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RED

    probs = [
        ("Accidental Public S3 Buckets", "Misconfigured bucket policies or disabled public access blocks leak PII globally."),
        ("Immediate Bot Exploitation", "Automated web scrapers detect open S3 buckets within 30 seconds of publicity."),
        ("Email Alert Fatigue", "Security teams receive 500+ daily emails; critical CloudWatch warnings get buried."),
        ("Delayed Incident Response", "Industry average latency to identify and remediate silent S3 leaks is over 14 hours.")
    ]
    for title, desc in probs:
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

    add_fitted_image(s2, "data_leak_concept.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)

    # =========================================================================
    # SLIDE 3: WHAT (The Core Project Concept)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_top_bar(s3, "WHAT IS OUR PROJECT", "Real-Time Cyber-Physical Alert System & Digital Twin")

    draw_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Project Concept & Innovation"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    sol = [
        ("Sub-Second Desk Actuation", "Bridges AWS Cloud auditing with physical ESP32 LED hardware on an engineer's desk."),
        ("Ambient Threat Awareness", "Converts passive email alert noise into an instant, un-ignorable physical Red flashing LED."),
        ("Real-Time Web Twin", "FastAPI WebSocket server mirrors physical hardware state synchronously in browser dashboard."),
        ("100% Serverless & Decoupled", "Runs on AWS Lambda, DynamoDB, SNS, and AWS IoT Core with zero server maintenance.")
    ]
    for title, desc in sol:
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

    add_fitted_image(s3, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)

    # =========================================================================
    # SLIDE 4: HOW (End-to-End Cloud Architecture Pipeline)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_top_bar(s4, "HOW OUR PROJECT WORKS", "End-to-End AWS Serverless & IoT Architecture")

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

    pipeline = [
        ("Stage 1: Lambda Auditor", "Python boto3 scanner inspects S3 bucket policies, ACLs & PublicAccessBlock."),
        ("Stage 2: Storage & SNS", "Persists event record into DynamoDB table 'SecurityEvents' & triggers SNS email/SMS."),
        ("Stage 3: AWS IoT Core", "Publishes JSON payload to topic 'cloud/security/alert' over MQTT TLS 1.2 Port 8883."),
        ("Stage 4: Hardware & Web Twin", "ESP32 receives payload, blinks Red LED 🔴, and updates WebSocket Web UI.")
    ]
    for stg, desc in pipeline:
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

    # =========================================================================
    # SLIDE 5: HOW (AWS Lambda 3-Layer S3 Auditor)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_top_bar(s5, "HOW OUR PROJECT WORKS — CLOUD SCANNER", "AWS Lambda 3-Layer S3 Auditor Engine")

    add_fitted_image(s5, "security_layers_diag.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=RED)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "3-Layer S3 Inspection Matrix"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RED

    layers = [
        ("Layer 1: Public Access Block", "Evaluates GetPublicAccessBlock. Flagged if any of 4 block flags are False."),
        ("Layer 2: Bucket Policy Status", "Queries GetBucketPolicyStatus. Flagged if IsPublic == True or wildcard Principal: '*'."),
        ("Layer 3: S3 Access Control Lists", "Parses GetBucketAcl. Flagged if AllUsers or AuthenticatedUsers URI exists.")
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

    # =========================================================================
    # SLIDE 6: HOW (AWS IoT Core Mutual TLS & Security)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_top_bar(s6, "HOW OUR PROJECT WORKS — SECURITY & PROTOCOLS", "AWS IoT Core Mutual TLS & X.509 Device Auth")

    add_fitted_image(s6, "crypto_shield_vault.png", Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)

    draw_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Zero-Trust IoT Security"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = GREEN

    sec = [
        ("Mutual Authentication (mTLS)", "ESP32 verifies Amazon Root CA 1; AWS IoT validates hardware client certificate."),
        ("Hardware X.509 Key Identity", "Private key stored securely on ESP32 SPIFFS flash memory."),
        ("TLS 1.2 Encrypted MQTT", "Port 8883 encryption prevents payload sniffing or network tampering."),
        ("Least Privilege IAM Policy", "Restricts hardware client strictly to topic 'cloud/security/alert'.")
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

    # =========================================================================
    # SLIDE 7: HOW (Deployment Automation & Verification)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_top_bar(s7, "HOW OUR PROJECT WORKS — AUTOMATION & TESTING", "1-Click AWS Provisioner & Vulnerability Test CLI")

    draw_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "1-Click Deployer (deploy_aws.py)"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN

    prov = [
        ("Automated Stack Setup", "Single command python cloud/deploy_aws.py provisions full AWS cloud architecture."),
        ("AWS Learner Lab Ready", "Auto-detects $50 student account 'LabRole' or creates standard IAM role."),
        ("Cert Auto-Injection", "Generates X.509 keys and populates firmware/include/secrets.h automatically.")
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

    draw_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=GREEN)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Test CLI (test_vulnerable_bucket.py)"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = GREEN

    test_flow = [
        ("1. Simulate S3 Leak", "python test_vulnerable_bucket.py create ➔ Creates public S3 bucket."),
        ("2. Instant Actuation", "Lambda scanner fires ➔ ESP32 Red LED blinks rapidly 🔴 & Web UI turns Crimson."),
        ("3. Remediation", "python test_vulnerable_bucket.py delete ➔ Deletes bucket & restores LED to solid OFF 🟢.")
    ]
    for title, desc in test_flow:
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

    # =========================================================================
    # SLIDE 8: SUMMARY & CONCLUSION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_top_bar(s8, "SUMMARY & KEY ACHIEVEMENTS", "Conclusion & Cloud Engineering Impact")

    draw_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=CYAN)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key System Achievements"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = CYAN

    achieve = [
        ("Sub-Second Physical Awareness", "Bridges AWS Cloud scanning with physical desk hardware to eliminate alert response latency."),
        ("Zero-Trust Hardware Security", "Protects IoT endpoints using X.509 client certificates, mTLS 1.2, and scoped IAM policies."),
        ("100% Automated Deployment", "1-Click deployer script provisions full AWS serverless stack in under 60 seconds."),
        ("Real-Time Digital Twin", "Synchronizes physical micro-controller hardware with interactive web dashboard via WebSockets.")
    ]
    for title, desc in achieve:
        p = tf.add_paragraph()
        p.text = f"✔  {title}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED

    add_fitted_image(s8, "cloud_security_hero_lamp.png", Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), border_color=CYAN)

    # Save presentation
    out_paths = [
        "docs/Cloud_Security_Alert_Lamp_Presentation.pptx",
        "docs/Cloud_Security_Alert_Lamp_Minimal.pptx",
        "docs/Cloud_Security_Alert_Lamp_Executive.pptx"
    ]
    for pth in out_paths:
        try:
            prs.save(pth)
            print(f"[+] Successfully saved Focused Cloud Lab Deck to: {pth}")
        except PermissionError:
            alt = pth.replace(".pptx", "_lab.pptx")
            prs.save(alt)
            print(f"[+] Saved to lab path: {alt}")

if __name__ == "__main__":
    create_cloud_computing_deck()
