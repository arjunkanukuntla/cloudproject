# 🚨💡 Cloud Security Alert Lamp — Master Presentation Script & Defense Guide

**Project Title:** Cloud Security Alert Lamp  
**Subtitle:** Real-Time Physical & Digital Alert System for Public Amazon S3 Buckets  
**Domain:** Cloud Computing & Cyber-Physical Security Engineering  
**Tech Stack:** Python (boto3, FastAPI), AWS Lambda, AWS S3, Amazon DynamoDB, Amazon SNS, AWS IoT Core (MQTT/TLS 1.2), ESP32 / Raspberry Pi, WebSockets, HTML5/CSS3.  

---

## 👥 Team Members & Presentation Assignments

| No. | Team Member | Roll Number | Presentation Section / Role |
| :---: | :--- | :---: | :--- |
| **01** | **D. Chander** | `2503A52214` | **Project Leader & Introduction:** Project Title, Problem Statement, & Solution Overview |
| **02** | **K. Arjun** | `2503A52235` | **Backend & Database Developer:** FastAPI Architecture, DynamoDB Event Logging, & SNS Alerts |
| **03** | **G. Rohan** | `2503S52224` | **System Architecture & Cloud Security:** 3-Layer S3 Auditor, AWS IoT Core, & X.509 TLS Security |
| **04** | **P. Sachin** | `2503A52240` | **Hardware, Live Working Demo & Q&A:** ESP32 Firmware State Machine, 9-Step Demo Flow, Takeaways & Defense |

---

# 📊 Slide-by-Slide Presentation Outline & Script

---

### 🎴 SLIDE 1: Title Slide & Team Introduction
* **Assigned Presenter:** **D. Chander** (Roll No: 2503A52214)

#### 1. Slide Title
**CLOUD SECURITY ALERT LAMP**  
*Physical & Real-Time Security Alert System for Public Amazon S3 Buckets*

#### 2. Visual Layout / Diagram Suggestion
- **Center Hero Graphic:** 3D Isometric illustration of an AWS Cloud storage bucket connected via a glowing cyan data stream to a physical Red IoT Emergency Alert Lamp on a desk.
- **Team Grid (Dark Slate Cards):** 4 clean horizontal cards displaying names and roll numbers:
  - `01. D. Chander (Roll No: 2503A52214)` — Project Lead & Overview
  - `02. K. Arjun (Roll No: 2503A52235)` — Backend & DB Developer
  - `03. G. Rohan (Roll No: 2503S52224)` — System Architecture
  - `04. P. Sachin (Roll No: 2503A52240)` — Working Process & Hardware
- **Tagline at bottom:** *"Detect. Alert. Protect."*

#### 3. Bullet Points for Slide
- Real-time cyber-physical alert system bridging AWS Cloud monitoring with IoT hardware.
- Automated 3-Layer inspection for S3 Bucket Public Access Blocks, Bucket Policies, and ACL Grants.
- Zero-Trust telemetry via AWS IoT Core MQTT over mutual TLS 1.2 (Port 8883).
- Dual Alerting: Physical ESP32 Red Flashing Lamp + Live WebSocket Digital Twin Dashboard.

#### 4. Presenter Script (D. Chander — 45 to 60 Seconds)
> *"Respected Evaluators and Professors, good morning. My name is D. Chander, and along with my team members K. Arjun, G. Rohan, and P. Sachin, we present our project: the Cloud Security Alert Lamp.*  
> *In modern cloud infrastructure, accidental public exposure of Amazon S3 buckets is one of the leading causes of enterprise data breaches. Traditional email notifications often get lost in noisy developer inboxes. Our project bridges cloud security auditing in AWS directly with physical IoT hardware. Whenever a public S3 bucket is created or misconfigured, an AWS Lambda auditor detects it instantly and publishes an alert payload to AWS IoT Core over mutual TLS, causing a physical Red LED on an engineer’s desk to flash rapidly in real-time. I will now hand over to Arjun to discuss the core problem and backend infrastructure."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Why do we need a physical hardware lamp when AWS already provides CloudWatch and email notifications?"*
- **Confident Answer:** *"Respected Professor, AWS CloudWatch and SNS emails suffer from severe 'alert fatigue'. Security engineers receive hundreds of emails daily, leading to an average Mean Time to Detect (MTTD) of hours or days. A physical ambient warning light on a desk creates zero-latency visual awareness that is impossible to ignore, driving immediate incident remediation."*

---

### 🎴 SLIDE 2: Problem Statement & Motivation
* **Assigned Presenter:** **D. Chander** (Roll No: 2503A52214)

#### 1. Slide Title
**THE PROBLEM: S3 CLOUD MISCONFIGURATIONS & ALERT FATIGUE**

#### 2. Visual Layout / Diagram Suggestion
- **Split Screen Visual:**
  - **Left Box (Red Border):** Graphic showing sensitive corporate files spilling from a public S3 bucket with malicious web bots scraping subdomains.
  - **Right Box (Cyan Border):** An engineer's inbox overflowing with 500+ unread security alert emails with a clock showing hours of delay.

#### 3. Bullet Points for Slide
- S3 misconfigurations expose millions of PII and credential records globally.
- Automated internet scrapers scan public AWS subdomains within seconds of exposure.
- Standard email alerts cause severe developer fatigue and delayed incident response.
- Need for sub-second ambient physical awareness in security operations centers.

#### 4. Presenter Script (D. Chander — 45 to 60 Seconds)
> *"To understand our motivation, consider the current cloud security landscape. S3 bucket publicity isn't just a configuration mistake—it is a catastrophic risk. Automated bots continuously scan IP ranges and public subdomains. If a developer accidentally disables Public Access Block or attaches a wildcard bucket policy, data is exposed in seconds.*  
> *However, traditional alerting relies on email digest logs. When engineers receive hundreds of CloudWatch emails daily, critical alerts get buried. This delay between exposure and awareness is where data theft occurs. Our goal was to eliminate this gap by bringing cyber threat visibility directly into the physical environment."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Is S3 exposure really still a major issue now that AWS has 'Block Public Access' enabled by default?"*
- **Confident Answer:** *"Yes, Professor. While AWS enables Public Access Block by default on new buckets, legacy buckets, IAM role overrides, terraform automation scripts, or developer mistakes during debugging frequently disable these blocks or grant public READ permissions via Bucket Policies or ACLs."*

---

### 🎴 SLIDE 3: Solution Overview & End-to-End Pipeline
* **Assigned Presenter:** **K. Arjun** (Roll No: 2503A52235)

#### 1. Slide Title
**SOLUTION OVERVIEW: CYBER-PHYSICAL ALERT PIPELINE**

#### 2. Visual Layout / Diagram Suggestion
- **4-Stage Pipeline Flowchart:**
  `[ 1. S3 Audit (boto3) ] ➔ [ 2. DynamoDB & SNS ] ➔ [ 3. AWS IoT Core (MQTT/TLS) ] ➔ [ 4. ESP32 Red LED & Web Twin ]`
- Glowing status badges showing `SECURITY OK (Green LED Off)` vs `CRITICAL BREACH (Red LED Flashing)`.

#### 3. Bullet Points for Slide
- Automated AWS Lambda Auditor built with Python `boto3` SDK.
- Event-driven DynamoDB (`SecurityEvents`) logging and Amazon SNS push notifications.
- Sub-second MQTT payload transmission over TLS 1.2 (Port 8883) via AWS IoT Core.
- Physical ESP32 microcontroller actuator + real-time WebSocket digital twin web app.

#### 4. Presenter Script (K. Arjun — 45 to 60 Seconds)
> *"Thank you, Chander. I am K. Arjun, and I developed the Backend Application, Database, and Notification infrastructure.*  
> *Our solution operates as a seamless cyber-physical pipeline across four synchronized layers. First, an automated AWS Lambda function periodically or reactively audits all S3 buckets in the AWS account using boto3. Second, if a public bucket is detected, it logs the event into Amazon DynamoDB and dispatches an Amazon SNS notification. Third, it publishes an MQTT payload to AWS IoT Core over an encrypted TLS connection. Finally, the ESP32 microcontroller receives the topic message and immediately triggers rapid red LED blinking, while our FastAPI backend broadcasts the alert to our Web Dashboard."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Why did you choose MQTT over HTTP REST API calls for sending alerts to the IoT hardware?"*
- **Confident Answer:** *"MQTT is a lightweight publish-subscribe protocol that maintains an active, low-overhead persistent TLS TCP connection. Using HTTP REST would require the ESP32 to poll our backend continuously (a pull model), wasting CPU bandwidth and network overhead. MQTT allows AWS IoT Core to push alerts to the device instantaneously with sub-millisecond latency."*

---

### 🎴 SLIDE 4: System Solution Architecture
* **Assigned Presenter:** **G. Rohan** (Roll No: 2503S52224)

#### 1. Slide Title
**SYSTEM ARCHITECTURE & DATA FLOW DIAGRAM**

#### 2. Visual Layout / Diagram Suggestion
- **Full Architecture Schematic:** High-resolution diagram showing AWS Cloud boundary, Internet Gateway, AWS IoT Core Broker, DynamoDB NoSQL Table, FastAPI Backend, ESP32 Microcontroller on breadboard, and Web Dashboard.

```
  [ AWS S3 Buckets ] ──(Scanned)──► [ AWS Lambda Auditor ]
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
             [ Amazon DynamoDB ]                     [ AWS IoT Core ]
             (Table: SecurityEvents)               (Topic: cloud/security/alerts)
                        │                                     │
                        ▼ (REST / WS)                         ▼ (TLS 8883)
             [ FastAPI Backend ]                     [ ESP32 / Raspberry Pi ]
                        │                                     │
                        ▼                                     ▼
             [ Web Dashboard Twin ]                  [ 🔴 Red LED Lamp Flashing ]
```

#### 3. Bullet Points for Slide
- Decoupled microservices architecture separating cloud detection from hardware actuation.
- Amazon DynamoDB table storing partition key `eventId` and sort key `timestamp`.
- Enterprise X.509 mutual certificate authentication between hardware and AWS IoT Core.
- FastAPI backend serving REST endpoints and WebSockets (`/ws`) for live dashboard telemetry.

#### 4. Presenter Script (G. Rohan — 45 to 60 Seconds)
> *"Greetings Professors, I am G. Rohan, responsible for the System Architecture and Security Protocols.*  
> *As shown in our system architecture diagram, we engineered a completely decoupled, event-driven design. The cloud inspection layer operates inside AWS Lambda, isolated from the hardware layer. When Lambda evaluates bucket publicity, it simultaneously writes a structured event item into Amazon DynamoDB for historical auditing and dispatches an MQTT JSON payload to AWS IoT Core.*  
> *The ESP32 microcontroller subscribes to the IoT topic over port 8883. Simultaneously, our FastAPI server monitors backend events and broadcasts updates over WebSockets to our digital twin dashboard."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"What happens if the database or FastAPI backend goes down? Will the physical light still work?"*
- **Confident Answer:** *"Yes! That is the beauty of our decoupled architecture. Lambda publishes directly to AWS IoT Core via `iot-data`. Even if the local backend server or database is completely offline, the ESP32 connects directly to AWS IoT Core over TLS and will blink the Red LED without any dependency on local servers."*

---

### 🎴 SLIDE 5: Deep Dive — AWS S3 Security Auditor (Lambda)
* **Assigned Presenter:** **G. Rohan** (Roll No: 2503S52224)

#### 1. Slide Title
**AWS LAMBDA 3-LAYER S3 AUDITOR ALGORITHM**

#### 2. Visual Layout / Diagram Suggestion
- **3-Layer Security Shield Diagram:**
  - **Layer 1:** `PublicAccessBlock` (BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets).
  - **Layer 2:** `Bucket Policy Status` (Calls `get_bucket_policy_status()` ➔ `IsPublic == True`).
  - **Layer 3:** `Bucket ACL Grants` (Scans Grants for `AllUsers` / `AuthenticatedUsers` URIs).
- **Code Snippet Callout Box:** JSON alert payload schema showing `status`, `public_buckets_count`, `public_buckets` array.

#### 3. Bullet Points for Slide
- Evaluates 3 distinct S3 security layers to eliminate false negatives.
- Checks Account/Bucket `PublicAccessBlockConfiguration` overrides.
- Inspects AWS automated policy evaluation (`IsPublic` policy status).
- Audits legacy ACL Grants for wildcard permissions (`AllUsers`).

#### 4. Presenter Script (G. Rohan — 45 to 60 Seconds)
> *"Continuing with the auditor mechanics: determining whether an S3 bucket is public in AWS is complex because publicity can be granted through three different vectors.  
> First, our Lambda auditor uses `boto3` to inspect the `PublicAccessBlock`. If all four block parameters are enabled, the bucket is secure. Second, if a bucket policy exists, Lambda calls `get_bucket_policy_status()` to inspect AWS's internal Policy Evaluator for `IsPublic == True`. Third, Lambda iterates through the Bucket Access Control List (ACL) to verify no grants exist for `AllUsers` or `AuthenticatedUsers`. If any of these three layers indicate exposure, an `ALERT` payload is generated."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Does checking bucket ACLs cause performance degradation if an account has hundreds of buckets?"*
- **Confident Answer:** *"Lambda executes asynchronously in parallel. Furthermore, we evaluate PublicAccessBlock first as a fast short-circuit check. If PublicAccessBlock is fully enforced, Lambda skips policy and ACL evaluations, optimizing execution time to under 100 milliseconds per bucket."*

---

### 🎴 SLIDE 6: Backend & Database Infrastructure
* **Assigned Presenter:** **K. Arjun** (Roll No: 2503A52235)

#### 1. Slide Title
**FASTAPI BACKEND & DYNAMODB DATABASE LOGGING**

#### 2. Visual Layout / Diagram Suggestion
- **Database Schema Card:**
  - **DynamoDB Table:** `SecurityEvents` (BillingMode: PAY_PER_REQUEST)
  - **Primary Keys:** Partition Key `eventId` (String), Sort Key `timestamp` (String)
  - **Attributes:** `bucketName`, `riskLevel`, `ledStatus`, `eventType`, `details`
- **FastAPI Endpoints Box:** List of endpoints (`/api/dashboard`, `/api/events`, `/api/scan`, `/ws`).

#### 3. Bullet Points for Slide
- FastAPI asynchronous web framework providing high-concurrency REST endpoints.
- Amazon DynamoDB NoSQL table `SecurityEvents` for persistent audit history.
- Amazon SNS topic `CloudSecurityAlerts` for immediate email/SMS dispatch.
- Integrated WebSocket manager (`/ws`) for sub-millisecond frontend synchronization.

#### 4. Presenter Script (K. Arjun — 45 to 60 Seconds)
> *"I will now explain the backend and database implementation. We built the backend service using Python's FastAPI framework due to its native asynchronous event loop and high throughput.  
> When a security audit runs, all security events are persisted into Amazon DynamoDB table `SecurityEvents`. We configured DynamoDB with On-Demand billing, using `eventId` as the hash key and `timestamp` as the range key. Simultaneously, the backend triggers Amazon SNS to send push emails to administrators, and broadcasts the event over WebSockets to update the dashboard instantly."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Why use DynamoDB instead of a traditional relational database like MySQL or PostgreSQL?"*
- **Confident Answer:** *"DynamoDB is a fully managed NoSQL database that offers single-digit millisecond latency, seamlessly scales with AWS Lambda execution spikes without connection pool limits, and integrates natively with AWS IAM and SDKs without requiring database connection overhead."*

---

### SLIDE 7: AWS IoT Core & Zero-Trust Security
* **Assigned Presenter:** **G. Rohan** (Roll No: 2503S52224)

#### 1. Slide Title
**AWS IOT CORE MUTUAL TLS & X.509 SECURITY**

#### 2. Visual Layout / Diagram Suggestion
- **Security Concept Diagram:** Visual showing X.509 Client Certificate, Private Key, and Amazon Root CA 1 establishing a TLS 1.2 Encrypted Tunnel to AWS IoT Core (Port 8883).
- **JSON IoT Policy Schema Box:** Showing strict `iot:Connect`, `iot:Subscribe`, `iot:Receive` permission statements.

#### 3. Bullet Points for Slide
- Enterprise Zero-Trust IoT security model—no hardcoded passwords or plain API keys.
- TLS 1.2 mutual authentication on standard MQTT Port 8883.
- Device authenticates using X.509 Certificate (`certificate.pem.crt`) & Private Key.
- Least-privilege IAM IoT Policy strictly scoped to topic `cloud/security/alerts`.

#### 4. Presenter Script (G. Rohan — 45 to 60 Seconds)
> *"Security on the IoT endpoint is just as vital as cloud security. We implemented a Zero-Trust security model for our hardware lamp.  
> The ESP32 does not use unencrypted HTTP or simple API tokens. Instead, it authenticates with AWS IoT Core using X.509 client certificates generated during cloud deployment. The hardware validates AWS's server identity via Amazon Root CA 1, while AWS IoT Core validates the device certificate. Communication is fully encrypted over TLS 1.2 on port 8883, and our custom IoT IAM policy limits the device strictly to receive messages on the security alert topic."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Where are the private keys stored on the ESP32 hardware? Are they vulnerable to physical extraction?"*
- **Confident Answer:** *"The certificates and private keys are embedded in PROGMEM flash storage during firmware compilation. For production hardware hardening, the ESP32’s Flash Encryption and Secure Boot features can be enabled, encrypting the flash memory with a hardware key stored in eFuse, preventing key extraction even if physically analyzed."*

---

### 🎴 SLIDE 8: Hardware & Firmware Engineering
* **Assigned Presenter:** **P. Sachin** (Roll No: 2503A52240)

#### 1. Slide Title
**ESP32 HARDWARE SCHEMATICS & FIRMWARE ENGINE**

#### 2. Visual Layout / Diagram Suggestion
- **Breadboard Circuit Visual:** ESP32 Dev Kit pinout wired to GPIO 4 -> 220Ω Resistor -> Red LED Anode (+), GND -> Cathode (-).
- **State Machine Infographic (3 Cards):**
  - `🟢 STATE_OK`: Cloud Secure ➔ Red LED Solid OFF.
  - `🔴 STATE_ALERT`: Breach Detected ➔ Red LED Rapid 150ms Blink.
  - `🟡 STATE_DISCONNECTED`: Network Offline ➔ Heartbeat 1000ms Pulse.

#### 3. Bullet Points for Slide
- ESP32 32-bit dual-core 240MHz microcontroller with hardware crypto acceleration.
- GPIO 4 output driving 5mm Red LED through 220Ω current-limiting resistor.
- Non-blocking finite state machine evaluated using C++ `millis()` timers.
- Automatic network reconnection loop without blocking main execution threads.

#### 4. Presenter Script (P. Sachin — 45 to 60 Seconds)
> *"Good morning Professors, I am P. Sachin, and I developed the ESP32 Hardware Circuitry and C++ Firmware.  
> Our physical lamp uses an ESP32 development module. GPIO pin 4 connects through a 220-ohm resistor to the anode of a high-intensity Red LED.  
> The firmware is written in C++ using Arduino framework on PlatformIO. Crucially, the firmware uses a non-blocking state machine built with `millis()` timers rather than `delay()`. This ensures that while the LED is flashing rapidly at 150-millisecond intervals during an alert, the micro-controller continues to process incoming TLS MQTT packets and maintain Wi-Fi connectivity in parallel."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"Why did you avoid using the standard `delay()` function in your Arduino C++ code?"*
- **Confident Answer:** *"Using `delay()` pauses the CPU execution entirely. If the firmware used `delay(150)` to flash the LED, the ESP32 would fail to process incoming MQTT keep-alive pings, causing AWS IoT Core to drop the TLS TCP connection. Using `millis()` keeps the loop running at maximum CPU speed without blocking network tasks."*

---

### 🎴 SLIDE 9: Digital Twin Web Dashboard
* **Assigned Presenter:** **D. Chander** (Roll No: 2503A52214)

#### 1. Slide Title
**INTERACTIVE DIGITAL TWIN WEB DASHBOARD**

#### 2. Visual Layout / Diagram Suggestion
- **UI Screenshot Mockup:** High-tech dark glassmorphism dashboard UI showing:
  - Simulated ESP32 breadboard & glowing neon Red Alert Lamp.
  - Live metric boxes (Total Buckets, Public Count, MQTT Message Count).
  - S3 Security Audit Table & Real-time Console Log Feed.
  - Interactive Buttons (`Trigger Public S3 Alert` & `Clear Alert`).

#### 3. Bullet Points for Slide
- Modern dark glassmorphism interface styled with vanilla CSS & HTML5.
- Virtual Neon LED digital twin pulsing synchronously with physical hardware.
- Real-time WebSocket feed rendering AWS IoT Core MQTT message payloads.
- Integrated scenario tester for instant classroom demonstration.

#### 4. Presenter Script (D. Chander — 45 to 60 Seconds)
> *"To complement our physical hardware, we created a digital twin web dashboard.  
> Styled with a dark glassmorphism aesthetic, the dashboard connects via WebSockets directly to our FastAPI backend. It features a digital twin of our ESP32 breadboard and alert lamp. When an S3 breach occurs, the virtual neon lamp flashes synchronously with the physical hardware. It also provides an interactive scenario tester, allowing users to simulate security events, view bucket publicity details, and inspect live MQTT log streams."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"How does the web dashboard receive real-time updates without refreshing the browser page?"*
- **Confident Answer:** *"The browser establishes a persistent WebSocket connection to `/ws` on our FastAPI server upon loading. Whenever Lambda updates the security state, the backend broadcasts a JSON frame across all connected WebSocket clients, updating the DOM dynamically without page reloads."*

---

### 🎴 SLIDE 10: Automated AWS Provisioning & Test CLI
* **Assigned Presenter:** **K. Arjun** (Roll No: 2503A52235)

#### 1. Slide Title
**AUTOMATED AWS PROVISIONING & TESTING CLI**

#### 2. Visual Layout / Diagram Suggestion
- **Split Visual:**
  - **Left Box (`deploy_aws.py`):** Flow diagram showing 1-click provisioning of Lambda, DynamoDB, SNS, IoT Core Thing, X.509 Certs, and auto-generating `secrets.h` & `.env`.
  - **Right Box (`test_vulnerable_bucket.py`):** CLI terminal code execution showing `create` (triggers alert) and `delete` (remediates alert).

#### 3. Bullet Points for Slide
- 1-Click automated Python deployment script (`deploy_aws.py`) provisioning full AWS cloud stack.
- Auto-detects AWS Academy Learner Lab `$50 Student Account` IAM `LabRole`.
- Generates X.509 keys & automatically creates header `firmware/include/secrets.h`.
- Automated test utility CLI (`test_vulnerable_bucket.py`) for on-demand vulnerability creation.

#### 4. Presenter Script (K. Arjun — 45 to 60 Seconds)
> *"To ensure seamless deployment, we fully automated our AWS provisioning.  
> Running `python cloud/deploy_aws.py` executes a Python script using `boto3` that provisions DynamoDB, SNS, Lambda, and AWS IoT Core in under 60 seconds. It automatically detects AWS Learner Lab `LabRole` constraints for student accounts, generates X.509 keys, and populates `secrets.h` for the ESP32. We also created `test_vulnerable_bucket.py` to create and delete misconfigured S3 buckets on demand for testing."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"How did you handle IAM role creation restrictions in AWS Academy Learner Lab accounts?"*
- **Confident Answer:** *"AWS Learner Labs restrict the `iam:CreateRole` API. Our deployment script inspects the IAM environment first: if running in a Learner Lab, it automatically detects the pre-created `LabRole` ARN and attaches our Lambda policies to it, ensuring 100% compatibility without deployment errors."*

---

### 🎴 SLIDE 11: End-to-End Working Process & Live Demo
* **Assigned Presenter:** **P. Sachin** (Roll No: 2503A52240)

#### 1. Slide Title
**STEP-BY-STEP LIVE WORKING DEMONSTRATION**

#### 2. Visual Layout / Diagram Suggestion
- **5-Step Process Timeline Cards:**
  1. `1. BASELINE SETUP` (ESP32 connected, LED OFF, Status SECURE)
  2. `2. BREACH SIMULATION` (`python test_vulnerable_bucket.py create`)
  3. `3. LAMBDA AUDIT` (Detects `IsPublic: True` & logs to DynamoDB)
  4. `4. HARDWARE ALERT` (AWS IoT sends MQTT ➔ ESP32 Red LED Blinks 🔴)
  5. `5. REMEDIATION` (`python test_vulnerable_bucket.py delete` ➔ LED OFF 🟢)

#### 3. Bullet Points for Slide
- Step 1: System initializes in `STATE_OK` with Red LED solid OFF.
- Step 2: Test script creates public S3 bucket with disabled PublicAccessBlock.
- Step 3: Lambda auditor executes, records event in DynamoDB, publishes MQTT payload.
- Step 4: ESP32 Red LED blinks rapidly (150ms); Web Dashboard displays CRITICAL BREACH.
- Step 5: Remediation script deletes test bucket; ESP32 LED returns to solid OFF.

#### 4. Presenter Script (P. Sachin — 45 to 60 Seconds)
> *"Now, we will walk through our live system demonstration.  
> We start with a secure baseline: the ESP32 is connected to Wi-Fi, and the Red LED is solid OFF. Next, we execute `python cloud/test_vulnerable_bucket.py create`. This creates an S3 bucket with public read policy.  
> Within 1 second, Lambda scans the bucket, logs the breach to DynamoDB, and publishes an MQTT payload. The ESP32 receives the message over TLS and immediately blinks the Red LED rapidly. Finally, executing `python cloud/test_vulnerable_bucket.py delete` removes the vulnerable bucket, causing Lambda to publish a secure payload, turning the Red LED solid OFF."*

#### 5. Expected Professor / Evaluator Q&A Trap
- **Professor Question:** *"What happens if the ESP32 loses Wi-Fi connection while an alert is active?"*
- **Confident Answer:** *"The firmware enters `STATE_DISCONNECTED`. It smoothly transitions the Red LED to a slow 1-second heartbeat pulse to visually notify engineers of network loss, while continuously attempting Wi-Fi and MQTT reconnection in the background."*

---

### 🎴 SLIDE 12: Security Engineering Takeaways & Q&A
* **Assigned Presenter:** **D. Chander** (Roll No: 2503A52214) & All Team Members

#### 1. Slide Title
**KEY ENGINEERING TAKEAWAYS & EVALUATION Q&A**

#### 2. Visual Layout / Diagram Suggestion
- **3 Visual Takeaway Cards:**
  - `🛡️ Defense in Depth`: Account-level Public Access Block + Policy + ACL Auditing.
  - `🔑 Zero Trust IoT`: Mutual X.509 cert authentication & TLS 1.2 encryption.
  - `⚡ Ambient Awareness`: Physical warning lamps cut through email noise.
- **Team Contact Banner at Bottom:**
  - `D. Chander (2503A52214)` • `K. Arjun (2503A52235)` • `G. Rohan (2503S52224)` • `P. Sachin (2503A52240)`

#### 3. Bullet Points for Slide
- **Defense in Depth:** Multi-layered security inspection eliminates cloud exposure blind spots.
- **Zero Trust Hardware:** Enterprise TLS 1.2 & X.509 certificates harden IoT endpoints.
- **Ambient Alerting:** Cyber-physical awareness reduces mean time to detect (MTTD) from hours to seconds.
- **100% Automated Deployment:** Production-ready cloud provisioning & digital twin testing.

#### 4. Presenter Script (D. Chander — 45 to 60 Seconds)
> *"In conclusion, our Cloud Security Alert Lamp demonstrates three core engineering principles: Defense in Depth in cloud auditing, Zero Trust security in IoT communication, and Ambient Awareness in incident response. By combining AWS serverless cloud infrastructure with physical IoT hardware, we drastically reduce incident response times for cloud storage vulnerabilities.  
> On behalf of Arjun, Rohan, Sachin, and myself, thank you for your time. We are now open for your questions."*

#### 5. Expected Professor / Evaluator Q&A Trap Matrix (For All Team Members)

| Evaluator Question | Team Member to Answer | Best Technical Response |
| :--- | :--- | :--- |
| **"How can this scale to thousands of AWS accounts?"** | **K. Arjun** | *"Lambda scales natively. For multi-account AWS organizations, we can deploy this via AWS CloudFormation StackSets and aggregate alerts into a central AWS IoT Core hub."* |
| **"Why not use WebSockets for the ESP32 instead of MQTT?"** | **G. Rohan** | *"AWS IoT Core provides native MQTT broker capability with managed X.509 authentication, QoS 1 delivery guarantees, and minimal memory footprint suitable for microcontrollers."* |
| **"What is the cost of running this system in AWS?"** | **D. Chander** | *"It fits 100% within the AWS Free Tier and Learner Lab $50 budget. Lambda, DynamoDB on-demand, and IoT Core cost under $0.05 per month for typical auditing volumes."* |
| **"Can you add audio buzzers or RGB lights to the ESP32?"** | **P. Sachin** | *"Yes! Our C++ state machine is modular. We can assign GPIO pins for an active buzzer or NeoPixel RGB LED ring to show different colors for LOW, HIGH, and CRITICAL risks."* |

---
