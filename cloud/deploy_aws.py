#!/usr/bin/env python3
"""
Automated AWS Provisioning Script: Cloud Security Alert Lamp
Supports standard AWS accounts and AWS Student Accounts / Learner Lab (LabRole).

What this script does:
1. Detects AWS Account ID & Region.
2. Manages IAM execution role for Lambda (supports pre-existing 'LabRole' for AWS Academy).
3. Provisions Amazon DynamoDB Table 'SecurityEvents' for security audit logs.
4. Provisions Amazon SNS Topic 'CloudSecurityAlerts' for instant alerts.
5. Packages and deploys AWS Lambda function 'CloudSecurityS3Auditor'.
6. Queries AWS IoT Core Data-ATS endpoint.
7. Provisions AWS IoT Core Thing ('SecurityAlertLamp'), Policy ('CloudSecurityAlertLampPolicy'), and X.509 Certificates.
8. Automatically populates 'firmware/include/secrets.h' with generated certs & IoT endpoint!
9. Configures EventBridge cron schedule (runs Lambda scanner every 5 minutes).
10. Generates '.env' file for FastAPI backend connection!
"""

import sys
import os
import io
import zipfile
import json
import subprocess

# Auto-install boto3 if missing
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("[*] Installing missing dependency 'boto3'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "boto3", "botocore", "python-dotenv"])
    import boto3
    from botocore.exceptions import ClientError

def print_header(title):
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)

def main():
    print_header("Cloud Security Alert Lamp - AWS Auto Deployer")

    # Step 1: Check AWS Credentials & Account Info
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        account_id = identity['AccountId']
        arn = identity['Arn']
        print(f"[+] Connected to AWS Account ID: {account_id}")
        print(f"[+] IAM Identity: {arn}")
    except Exception as e:
        print(f"[-] ERROR: Failed to authenticate with AWS: {e}")
        print("    Please run 'aws configure' or set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.")
        sys.exit(1)

    region = boto3.Session().region_name or 'us-east-1'
    print(f"[+] AWS Region: {region}")

    # Step 2: Determine IAM Role for Lambda
    iam = boto3.client('iam')
    role_arn = None

    # Check for AWS Student Account / Learner Lab pre-created role 'LabRole'
    try:
        lab_role = iam.get_role(RoleName='LabRole')
        role_arn = lab_role['Role']['Arn']
        print(f"[+] Found AWS Learner Lab 'LabRole': {role_arn}")
    except ClientError:
        print("[*] 'LabRole' not found. Checking or creating custom IAM role 'CloudSecurityAuditorRole'...")
        role_name = 'CloudSecurityAuditorRole'
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }

        try:
            role_res = iam.get_role(RoleName=role_name)
            role_arn = role_res['Role']['Arn']
            print(f"[+] Using existing IAM role: {role_arn}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                try:
                    create_res = iam.create_role(
                        RoleName=role_name,
                        AssumeRolePolicyDocument=json.dumps(assume_role_policy),
                        Description="IAM Role for Cloud Security Alert Lamp S3 Auditor Lambda"
                    )
                    role_arn = create_res['Role']['Arn']
                    print(f"[+] Created IAM Role: {role_arn}")

                    # Attach policies
                    policies = [
                        "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                        "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
                        "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
                        "arn:aws:iam::aws:policy/AWSIoTFullAccess",
                        "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
                    ]
                    for policy_arn in policies:
                        try:
                            iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
                        except Exception as pe:
                            print(f"    [-] Warning attaching {policy_arn}: {pe}")

                except Exception as cre:
                    print(f"[-] Error creating IAM role: {cre}")
                    sys.exit(1)

    # Step 3: Provision DynamoDB Table 'SecurityEvents'
    print("\n[*] Provisioning Amazon DynamoDB Table 'SecurityEvents'...")
    dynamodb = boto3.client('dynamodb', region_name=region)
    table_name = 'SecurityEvents'
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'eventId', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'eventId', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"[+] Created DynamoDB Table: {table_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"[+] DynamoDB Table '{table_name}' already exists.")
        else:
            print(f"[-] DynamoDB Table note: {e}")

    # Step 4: Provision SNS Topic 'CloudSecurityAlerts'
    print("\n[*] Provisioning Amazon SNS Topic 'CloudSecurityAlerts'...")
    sns = boto3.client('sns', region_name=region)
    sns_topic_arn = ""
    try:
        res = sns.create_topic(Name='CloudSecurityAlerts')
        sns_topic_arn = res['TopicArn']
        print(f"[+] Created SNS Topic ARN: {sns_topic_arn}")
    except Exception as e:
        print(f"[-] SNS Topic note: {e}")

    # Step 5: Package Lambda Code into Zip
    print("\n[*] Packaging Lambda function...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lambda_code_path = os.path.join(script_dir, 'lambda', 'auditor.py')

    if not os.path.exists(lambda_code_path):
        print(f"[-] ERROR: Lambda file not found at {lambda_code_path}")
        sys.exit(1)

    with open(lambda_code_path, 'r', encoding='utf-8') as f:
        auditor_code = f.read()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('auditor.py', auditor_code)
    zip_bytes = zip_buffer.getvalue()

    # Step 6: Deploy or Update AWS Lambda Function
    lambda_client = boto3.client('lambda', region_name=region)
    function_name = 'CloudSecurityS3Auditor'

    lambda_arn = None
    try:
        res = lambda_client.get_function(FunctionName=function_name)
        lambda_arn = res['Configuration']['FunctionArn']
        print(f"[+] Updating existing Lambda function code: {function_name}")
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_bytes
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"[*] Creating new Lambda function: {function_name}")
            create_res = lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role=role_arn,
                Handler='auditor.handler',
                Code={'ZipFile': zip_bytes},
                Description='Audits S3 buckets for public exposure and triggers IoT Alert Lamp',
                Timeout=30,
                MemorySize=128,
                Environment={
                    'Variables': {
                        'MQTT_TOPIC': 'cloud/security/alerts',
                        'DYNAMODB_TABLE_NAME': table_name,
                        'SNS_TOPIC_ARN': sns_topic_arn
                    }
                }
            )
            lambda_arn = create_res['FunctionArn']
            print(f"[+] Created Lambda function: {lambda_arn}")

    # Step 7: Provision AWS IoT Core Components
    print("\n[*] Setting up AWS IoT Core...")
    iot = boto3.client('iot', region_name=region)

    endpoint_res = iot.describe_endpoint(endpointType='iot:Data-ATS')
    iot_endpoint = endpoint_res['endpointAddress']
    print(f"[+] AWS IoT Core Data-ATS Endpoint: {iot_endpoint}")

    policy_name = 'CloudSecurityAlertLampPolicy'
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["iot:Connect"],
                "Resource": ["*"]
            },
            {
                "Effect": "Allow",
                "Action": ["iot:Subscribe", "iot:Receive"],
                "Resource": ["arn:aws:iot:*:*:topicfilter/cloud/security/*", "arn:aws:iot:*:*:topic/cloud/security/*"]
            },
            {
                "Effect": "Allow",
                "Action": ["iot:Publish"],
                "Resource": ["arn:aws:iot:*:*:topic/cloud/security/*"]
            }
        ]
    }

    try:
        iot.create_policy(
            policyName=policy_name,
            policyDocument=json.dumps(policy_doc)
        )
        print(f"[+] Created IoT Policy: {policy_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            print(f"[+] IoT Policy '{policy_name}' already exists.")

    thing_name = 'SecurityAlertLamp'
    try:
        iot.create_thing(thingName=thing_name)
        print(f"[+] Created IoT Thing: {thing_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            print(f"[+] IoT Thing '{thing_name}' already exists.")

    print("[*] Generating X.509 Keys and Certificate for ESP32...")
    cert_res = iot.create_keys_and_certificate(setAsActive=True)
    cert_arn = cert_res['certificateArn']
    cert_pem = cert_res['certificatePem']
    private_key = cert_res['keyPair']['PrivateKey']

    print(f"[+] Created Certificate ARN: {cert_arn}")

    iot.attach_policy(policyName=policy_name, target=cert_arn)
    iot.attach_thing_principal(thingName=thing_name, principal=cert_arn)

    # Step 8: Write generated credentials into firmware/include/secrets.h!
    print("\n[*] Writing AWS certificates & IoT Endpoint into firmware/include/secrets.h...")
    secrets_file_path = os.path.join(script_dir, '..', 'firmware', 'include', 'secrets.h')

    secrets_content = f"""#ifndef SECRETS_H
#define SECRETS_H

#include <pgmspace.h>

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

const char* AWS_IOT_ENDPOINT = "{iot_endpoint}";

static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEz
BhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJvb3QgQ0Eg
MTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeWBnnOoAGpnN
99YbfyxjGVey18fusEhyyuhIp78KrtRHfT64/nziIB7zmFwkknqxquqwDAua9Ztg
fS759SxC54YxsTtTtepD+wuM8VaaPEAsU54552yhe/5Fyb59sm2n659s476iNti1
B0g71Bi216gS96e/n567n95n6759675/675/675/675/675/675/675/675/675
-----END CERTIFICATE-----
)EOF";

static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
{cert_pem}
)KEY";

static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
{private_key}
)KEY";

#endif // SECRETS_H
"""

    with open(secrets_file_path, 'w', encoding='utf-8') as f:
        f.write(secrets_content)

    print(f"[+] SUCCESS: Created firmware secrets header at: {secrets_file_path}")

    # Step 9: Write .env file for Backend
    env_file_path = os.path.join(script_dir, '..', '.env')
    env_content = f"""AWS_REGION={region}
AWS_IOT_ENDPOINT={iot_endpoint}
AWS_IOT_TOPIC=cloud/security/alerts
DYNAMODB_TABLE_NAME=SecurityEvents
SNS_TOPIC_ARN={sns_topic_arn}
LAMBDA_FUNCTION_NAME={function_name}
"""
    with open(env_file_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print(f"[+] SUCCESS: Created root environment file at: {env_file_path}")

    # Step 10: EventBridge Schedule Rule (Run scanner every 5 minutes)
    print("\n[*] Configuring EventBridge cron trigger (every 5 minutes)...")
    events = boto3.client('events', region_name=region)
    rule_name = 'CloudSecurityAuditorSchedule'

    try:
        events.put_rule(
            Name=rule_name,
            ScheduleExpression='rate(5 minutes)',
            State='ENABLED',
            Description='Triggers S3 Auditor Lambda every 5 minutes'
        )
        events.put_targets(
            Rule=rule_name,
            Targets=[{'Id': '1', 'Arn': lambda_arn}]
        )

        try:
            lambda_client.add_permission(
                FunctionName=function_name,
                StatementId='EventBridgeInvokeS3Auditor',
                Action='lambda:InvokeFunction',
                Principal='events.amazonaws.com',
                SourceArn=f"arn:aws:events:{region}:{account_id}:rule/{rule_name}"
            )
            print("[+] Granted EventBridge permission to invoke Lambda.")
        except ClientError as pe:
            if pe.response['Error']['Code'] != 'ResourceConflictException':
                print(f"    [-] Permission note: {pe}")

    except Exception as ee:
        print(f"[-] EventBridge configuration warning: {ee}")

    print_header("AWS DEPLOYMENT COMPLETE!")
    print(f"1. AWS Lambda Function : {function_name}")
    print(f"2. AWS IoT Endpoint    : {iot_endpoint}")
    print(f"3. DynamoDB Table      : {table_name}")
    print(f"4. SNS Topic           : {sns_topic_arn}")
    print(f"5. ESP32 Secrets Header: firmware/include/secrets.h (Populated!)")
    print("\nNext Steps:")
    print("a. Fill in WIFI_SSID and WIFI_PASSWORD in 'firmware/include/secrets.h'.")
    print("b. Upload firmware to your ESP32 board or start desktop simulator ('python backend/led_controller.py').")
    print("c. Start FastAPI Backend: 'python backend/main.py'.")
    print("d. Run 'python cloud/test_vulnerable_bucket.py create' to test live alert flow!")

if __name__ == '__main__':
    main()
