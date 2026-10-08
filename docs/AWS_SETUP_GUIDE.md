# AWS Setup Guide: Cloud Security Alert Lamp
### Tailored for AWS Student Accounts ($50 Learner Lab & AWS Free Tier)

This guide walks you through setting up the cloud infrastructure using your $50 AWS Student / Learner Lab Account.

---

## 1. AWS Learner Lab Budget & Cost Estimate

> [!TIP]
> **Total Project Cost: $0.00**
> All services used in this project (AWS Lambda, AWS IoT Core, S3, EventBridge, and SNS) fall well within the **AWS Free Tier limits**:
> * **AWS Lambda**: 1,000,000 free requests per month.
> * **AWS IoT Core**: 250,000 free messages per month.
> * **AWS S3**: 5GB free storage.
> Your $50 student credits will remain 100% intact!

---

## 2. Fast Automated Setup (Recommended)

1. Open your terminal in `c:\cloud project\`.
2. Configure your AWS Student CLI credentials:
   ```bash
   aws configure
   ```
   *(Or export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` provided by your AWS Learner Lab portal).*

3. Run the automated deployment script:
   ```bash
   python cloud/deploy_aws.py
   ```

4. What happens automatically:
   - Detects AWS Learner Lab pre-configured `LabRole`.
   - Packs and deploys `CloudSecurityS3Auditor` Lambda function.
   - Provisions AWS IoT Core Thing `SecurityAlertLamp` and IoT X.509 certificates.
   - Automatically populates `firmware/include/secrets.h` with your unique AWS IoT endpoint and X.509 certificates!

---

## 3. Manual Step-by-Step Setup (Alternative)

If you prefer manual configuration in the AWS Management Console:

### Step A: AWS IoT Core Setup
1. Navigate to **AWS IoT Core** -> **All devices** -> **Things** -> Click **Create things**.
2. Name the Thing: `SecurityAlertLamp`.
3. Choose **Auto-generate a new certificate**.
4. Attach Policy: Create a policy named `CloudSecurityAlertLampPolicy` allowing `iot:Connect`, `iot:Subscribe`, `iot:Receive`, and `iot:Publish` on topic `cloud/security/*`.
5. Download `Device Certificate`, `Private Key`, and `Amazon Root CA 1`.
6. Copy certificates into `firmware/include/secrets.h`.
7. Note your IoT Endpoint under **AWS IoT Core** -> **Settings** (e.g. `a3xxxxxxx-ats.iot.us-east-1.amazonaws.com`).

### Step B: AWS Lambda Setup
1. Navigate to **AWS Lambda** -> Click **Create function**.
2. Name: `CloudSecurityS3Auditor`, Runtime: **Python 3.11**.
3. Under **Permissions**, choose **Use an existing role** -> Select `LabRole`.
4. Paste the code from `cloud/lambda/auditor.py` into the editor.
5. Environment Variables: Set `MQTT_TOPIC` = `cloud/security/alerts`.
6. Click **Deploy**.

### Step C: EventBridge Cron Schedule
1. Navigate to **Amazon EventBridge** -> **Rules** -> Click **Create rule**.
2. Rule Name: `CloudSecurityAuditorSchedule`.
3. Schedule: `rate(5 minutes)`.
4. Target: Select **Lambda function** -> `CloudSecurityS3Auditor`.

---

## 4. End-to-End System Testing

### Test 1: Trigger Physical Security Lamp (Vulnerability Created)
Run the test script to create a public S3 bucket:
```bash
python cloud/test_vulnerable_bucket.py create
```
* **Expected Result**: Lambda detects public bucket, publishes `ALERT` JSON to AWS IoT Core, and your ESP32 **Red LED starts blinking rapidly**!

### Test 2: Clear Security Lamp (Vulnerability Resolved)
Run the test script to delete the public S3 bucket:
```bash
python cloud/test_vulnerable_bucket.py delete
```
* **Expected Result**: Lambda detects zero public buckets, publishes `OK` JSON to AWS IoT Core, and your ESP32 **Red LED turns OFF**!
