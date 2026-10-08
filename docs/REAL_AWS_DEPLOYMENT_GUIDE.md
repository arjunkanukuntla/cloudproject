# 🚀 Cloud Security Alert Lamp: Complete Real AWS Deployment & Integration Guide

This guide provides the exact, step-by-step instructions to connect your **Frontend Dashboard**, **FastAPI Backend**, **AWS Cloud Infrastructure**, and **ESP32 Hardware / IoT Lamp** for a real live deployment on AWS!

---

## 🛠️ System Components Architecture

```
                      ┌────────────────────────┐
                      │    AWS S3 Buckets      │
                      └───────────┬────────────┘
                                  │ (Scanned)
                                  ▼
                      ┌────────────────────────┐
                      │   AWS Lambda Auditor   │ (Python boto3)
                      └─────┬────────────┬─────┘
                            │            │
         (Audit Log)        │            │ (MQTT Alert Payload)
              ▼             ▼            ▼
     ┌────────────────┐  ┌───────┐  ┌──────────────────┐
     │ Amazon DynamoDB│  │  SNS  │  │   AWS IoT Core   │
     │'SecurityEvents'│  └───────┘  │ (Port 8883 TLS)  │
     └────────────────┘             └────────┬─────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │ ESP32 Hardware   │ (Red LED Blinks 🔴)
                                    │ / Desktop Lamp   │
                                    └────────┬─────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │  Web Dashboard   │ (Live Web Twin)
                                    └──────────────────┘
```

---

## 📋 Step-by-Step Instructions

### Step 1: AWS Credentials & Account Setup
Ensure your AWS credentials are set up on your machine:
- **Standard AWS Accounts**: Run `aws configure` in terminal and enter your `AWS Access Key ID`, `AWS Secret Access Key`, and region (e.g. `us-east-1` or `ap-south-1`).
- **AWS Learner Lab / Student Accounts ($50 Credit)**: Copy your temporary credentials from AWS Academy console (`aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`) into `%USERPROFILE%\.aws\credentials` or your terminal session.

---

### Step 2: 1-Click Automated Cloud Deployment (`deploy_aws.py`)
Run the automated deployment script from your project root directory:

```bash
python cloud/deploy_aws.py
```

#### What `deploy_aws.py` automatically provisions in 60 seconds:
1. **IAM Role**: Auto-detects AWS Student Account `LabRole` or creates standard `CloudSecurityAuditorRole`.
2. **Amazon DynamoDB Table**: Creates `SecurityEvents` table for persistent event logging.
3. **Amazon SNS Topic**: Creates `CloudSecurityAlerts` topic for push notifications.
4. **AWS Lambda Auditor**: Deploys `CloudSecurityS3Auditor` Lambda function.
5. **AWS IoT Core**: Creates `SecurityAlertLamp` Thing, X.509 Certificate, Private Key, and IoT Policy.
6. **ESP32 Secrets Header**: Automatically populates `firmware/include/secrets.h` with AWS certificates & IoT Endpoint!
7. **EventBridge Cron Schedule**: Configures 5-minute automated audit scans.
8. **Root Environment File**: Writes `.env` configuration file for the backend server.

---

### Step 3: Flash ESP32 Hardware Firmware (or Desktop Simulator)

#### Option A: Physical ESP32 Board
1. Open `firmware/include/secrets.h`.
2. Enter your local Wi-Fi credentials:
   ```cpp
   const char* WIFI_SSID = "Your_WiFi_Name";
   const char* WIFI_PASSWORD = "Your_WiFi_Password";
   ```
3. Connect ESP32 to breadboard:
   - **GPIO 4** -> 220Ω Resistor -> **Red LED Anode (+)**
   - **GND** -> **Red LED Cathode (-)**
4. Flash using **PlatformIO** (`pio run --target upload`) or Arduino IDE (`firmware/esp32_firmware.ino`).

#### Option B: Desktop / Terminal Simulator (No Hardware Needed!)
If physical hardware is unavailable, run the Python IoT Lamp controller in terminal:
```bash
python backend/led_controller.py
```
*(This connects to the backend and simulates the Red LED flashing directly in your terminal screen!)*

---

### Step 4: Launch the FastAPI Backend & Web Dashboard

Install backend dependencies and run the server:

```bash
pip install -r backend/requirements.txt
python backend/main.py
```

- Open your browser to: **`http://localhost:8000`**
- You will see the **Live Cloud Security Alert Lamp Web Dashboard** connected via WebSockets to real-time telemetry!

---

### Step 5: Test the Live System End-to-End!

1. **Simulate a Public S3 Bucket Security Breach**:
   ```bash
   python cloud/test_vulnerable_bucket.py create
   ```
   - **Result**:
     - AWS Lambda auditor detects public S3 bucket.
     - DynamoDB records security event.
     - AWS IoT Core pushes MQTT alert payload over TLS.
     - **Physical ESP32 Red LED blinks rapidly!** (Terminal simulator displays `🚨 [🔴 RED LED: *** FLASHING ALERT ***]`).
     - Web Dashboard status turns to **CRITICAL ALERT**.

2. **Remediate Security Breach**:
   ```bash
   python cloud/test_vulnerable_bucket.py delete
   ```
   - **Result**:
     - Vulnerable test bucket is deleted.
     - AWS Lambda auditor confirms clean state.
     - **Physical ESP32 Red LED turns solid OFF!**
     - Web Dashboard returns to **SYSTEM SECURE**.

---

## ❓ Frequently Asked Questions (Classroom Defense)

| Question | Answer |
| :--- | :--- |
| **How does AWS IoT Core authenticate the ESP32?** | Via X.509 Mutual Certificate Authentication over TLS 1.2 on Port 8883. No plain passwords or HTTP API keys are used. |
| **What happens if Wi-Fi drops on the ESP32?** | The ESP32 enters `STATE_DISCONNECTED` (pulses Red LED once per second) while continuously retrying Wi-Fi & MQTT connections using non-blocking timers. |
| **How is AWS Student Account ($50 Learner Lab) supported?** | `deploy_aws.py` automatically detects the pre-created `LabRole` in AWS Academy Learner Lab accounts to bypass restricted `CreateRole` permissions. |
