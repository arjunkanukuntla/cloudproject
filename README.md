# Cloud Security Alert Lamp 🚨💡
> **Real-time IoT Physical Alert System & Dashboard for AWS S3 Bucket Public Exposure**

The **Cloud Security Alert Lamp** is an end-to-end cyber-physical cloud security monitoring system. Whenever an AWS Lambda auditor detects a public S3 bucket or misconfigured public policy/ACL in your AWS account, it logs the event to **Amazon DynamoDB**, sends an **Amazon SNS** alert, and publishes an alert payload to **AWS IoT Core** over MQTT. An **ESP32 microcontroller with a Red LED** (or desktop terminal simulator) receives the alert over TLS 1.2 and blinks rapidly to notify security engineers of the public exposure in real time!

---

## 🌟 Key Features

- **Automated 3-Layer S3 Auditor**: Lambda function built with `boto3` auditing `PublicAccessBlock`, `IsPublic PolicyStatus`, and `Public ACL Grants`.
- **Amazon DynamoDB Logging**: Persistent audit trail stored in `SecurityEvents` table.
- **Real-Time IoT Alerting**: Uses AWS IoT Core MQTT Broker (Port 8883) with X.509 Certificate Mutual TLS Security.
- **FastAPI Full Backend**: Python FastAPI server providing REST API and WebSocket (`/ws`) real-time live synchronization.
- **Hardware ESP32 Lamp & Desktop Simulator**: C++ PlatformIO / Arduino firmware and Python `led_controller.py` terminal simulator.
- **Student Account & Learner Lab Ready**: Designed for $50 AWS Student accounts (auto-detects `LabRole` or creates standard IAM roles).
- **Automated Provisioner**: 1-click Python deployment script (`deploy_aws.py`) provisioning DynamoDB, SNS, Lambda, IoT Core, X.509 Certs, and populating `secrets.h` + `.env`.
- **Test CLI Utility**: `test_vulnerable_bucket.py` tool to simulate public S3 bucket creation and cleanup.
- **Interactive Visual Presentation Decks**: PowerPoint `.pptx` deck, interactive HTML web deck, and slide scripts for class presentation!

---

## 📁 Repository Structure

```
c:\cloud project\
├── backend/                         # FastAPI Backend Application & API
│   ├── main.py                     # Server entry point (REST API, WebSockets & Static Hosting)
│   ├── led_controller.py           # Desktop / Raspberry Pi IoT Lamp Simulator
│   └── requirements.txt            # Python dependencies
│
├── cloud/                           # AWS Infrastructure & Deployment Automation
│   ├── deploy_aws.py               # Automated 1-click AWS setup script (DynamoDB + Lambda + IoT)
│   ├── test_vulnerable_bucket.py   # Public bucket test & cleanup CLI
│   ├── aws_iot_policy.json         # AWS IoT Policy schema
│   └── lambda/
│       └── auditor.py              # AWS Lambda S3 Scanner (boto3)
│
├── firmware/                        # ESP32 Microcontroller Code
│   ├── platformio.ini              # PlatformIO project config
│   ├── esp32_firmware.ino          # Arduino IDE sketch version
│   ├── src/
│   │   └── main.cpp                # ESP32 TLS MQTT Client & LED state machine
│   └── include/
│       ├── config.h                # Hardware pinouts & MQTT topics
        └── secrets.h.template      # Wi-Fi & AWS X.509 Certs template
│
├── web_dashboard/                   # Live Web Twin Dashboard UI
│   ├── index.html                  # Dashboard UI HTML
│   ├── styles.css                  # Dark glassmorphism styles & neon LED animation
│   └── app.js                      # Real-time WebSocket & simulation logic
│
├── docs/                            # Documentation, Presentations & Visual Decks
│   ├── REAL_AWS_DEPLOYMENT_GUIDE.md# Complete step-by-step real AWS deployment guide
│   ├── PRESENTATION_SLIDES.md      # Presentation script & slide breakdown
│   ├── presentation.html           # Standalone interactive HTML presentation deck
│   ├── Cloud_Security_Alert_Lamp_Presentation.pptx # Widescreen 16:9 PowerPoint deck
│   ├── WIRING_GUIDE.md             # Pinout connections & circuit schematics
│   └── AWS_SETUP_GUIDE.md          # AWS Student / Learner Lab setup guide
│
└── README.md                        # Master Documentation
```

---

## 🚀 Quick Start Guide

### 1. Provision AWS Infrastructure (1-Click)
Ensure your AWS credentials are active (`aws configure` or Learner Lab credentials), then run:
```bash
python cloud/deploy_aws.py
```
*This provisions Lambda, DynamoDB, SNS, IoT Core Thing & Certs, and populates `firmware/include/secrets.h` and `.env`.*

### 2. Start the FastAPI Backend & Web Dashboard
```bash
pip install -r backend/requirements.txt
python backend/main.py
```
Open your browser to: **`http://localhost:8000`**

### 3. Connect IoT Lamp (Hardware ESP32 or Desktop Simulator)
- **Option A (Physical ESP32)**: Fill in Wi-Fi details in `firmware/include/secrets.h` and upload to your board via PlatformIO / Arduino IDE.
- **Option B (Desktop Simulator)**: Run `python backend/led_controller.py` in a terminal window.

### 4. Test the System!
- **Simulate Security Breach**:
  ```bash
  python cloud/test_vulnerable_bucket.py create
  ```
  *(Physical Red LED / Terminal Lamp blinks rapidly 🔴! Dashboard turns to CRITICAL ALERT).*

- **Clear Security Breach**:
  ```bash
  python cloud/test_vulnerable_bucket.py delete
  ```
  *(Physical Red LED turns OFF 🟢! Dashboard returns to SYSTEM SECURE).*

---

## 📊 Class Presentation Resources

- **PowerPoint File**: [docs/Cloud_Security_Alert_Lamp_Presentation.pptx](file:///c:/cloud%20project/docs/Cloud_Security_Alert_Lamp_Presentation.pptx)
- **Interactive Browser Deck**: [docs/presentation.html](file:///c:/cloud%20project/docs/presentation.html) *(Press **N** for live speaker script)*
- **Real AWS Deployment Guide**: [docs/REAL_AWS_DEPLOYMENT_GUIDE.md](file:///c:/cloud%20project/docs/REAL_AWS_DEPLOYMENT_GUIDE.md)
