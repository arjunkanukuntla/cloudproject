#!/usr/bin/env python3
"""
Test Utility: Create or Remove Vulnerable Public S3 Bucket
Allows manual end-to-end testing of the Cloud Security Alert Lamp.

Commands:
  python test_vulnerable_bucket.py create   -> Creates a public S3 bucket & triggers Lambda scan (LED blinks!)
  python test_vulnerable_bucket.py delete   -> Deletes public S3 bucket & triggers Lambda scan (LED turns off!)
"""

import sys
import json
import random
import string
import boto3
from botocore.exceptions import ClientError

BUCKET_PREFIX = "test-public-vulnerable-lamp-"

def generate_bucket_name():
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{BUCKET_PREFIX}{rand_suffix}"

def create_public_bucket():
    s3 = boto3.client('s3')
    region = boto3.Session().region_name or 'us-east-1'
    bucket_name = generate_bucket_name()

    print(f"[*] Creating test S3 bucket: {bucket_name} in region {region}...")
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"[+] S3 Bucket created: {bucket_name}")

        # 1. Disable Public Access Block so bucket policy can be public
        print("[*] Disabling S3 Public Access Block configuration...")
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print("[+] Public Access Block disabled!")

        # 2. Attach Public Read Policy
        print("[*] Attaching public read policy (s3:GetObject for *)...")
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(public_policy)
        )
        print(f"[+] Public policy attached successfully! Bucket '{bucket_name}' is now VULNERABLE.")

        # Save active test bucket name to local temp file
        with open('.active_test_bucket', 'w', encoding='utf-8') as f:
            f.write(bucket_name)

        # 3. Trigger Lambda function immediately
        invoke_auditor_lambda()

    except Exception as e:
        print(f"[-] ERROR creating public bucket: {e}")

def delete_public_bucket():
    s3 = boto3.client('s3')
    bucket_name = None

    # Try reading from saved file
    try:
        with open('.active_test_bucket', 'r', encoding='utf-8') as f:
            bucket_name = f.read().strip()
    except Exception:
        pass

    if not bucket_name:
        # Search S3 for matching prefix
        try:
            res = s3.list_buckets()
            for b in res.get('Buckets', []):
                if b['Name'].startswith(BUCKET_PREFIX):
                    bucket_name = b['Name']
                    break
        except Exception as e:
            print(f"[-] Error listing buckets: {e}")

    if not bucket_name:
        print("[*] No active test public bucket found.")
        invoke_auditor_lambda()
        return

    print(f"[*] Deleting test public bucket: {bucket_name}...")
    try:
        # Delete policy first
        try:
            s3.delete_bucket_policy(Bucket=bucket_name)
        except Exception:
            pass

        # Delete bucket
        s3.delete_bucket(Bucket=bucket_name)
        print(f"[+] S3 Bucket '{bucket_name}' deleted successfully!")

        if os.path.exists('.active_test_bucket'):
            os.remove('.active_test_bucket')

        # Trigger Lambda scan to verify security state is cleared
        invoke_auditor_lambda()

    except Exception as e:
        print(f"[-] Error deleting bucket {bucket_name}: {e}")

def invoke_auditor_lambda():
    print("\n[*] Invoking S3 Auditor Lambda function to update alert lamp...")
    lambda_client = boto3.client('lambda')
    try:
        res = lambda_client.invoke(
            FunctionName='CloudSecurityS3Auditor',
            InvocationType='RequestResponse'
        )
        payload = json.loads(res['Payload'].read().decode('utf-8'))
        print("[+] Lambda Response:")
        print(json.dumps(payload, indent=2))
        print("\n>>> Check your physical ESP32 LED or Web Simulator state now! <<<")
    except Exception as e:
        print(f"[-] Could not invoke Lambda directly: {e}")
        print("    (EventBridge cron will still run automatically every 5 mins)")

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ['create', 'delete']:
        print("Usage:")
        print("  python test_vulnerable_bucket.py create  (Creates public bucket -> Triggers Alert LED)")
        print("  python test_vulnerable_bucket.py delete  (Removes public bucket -> Turns OFF Alert LED)")
        sys.exit(1)

    command = sys.argv[1]
    if command == 'create':
        create_public_bucket()
    elif command == 'delete':
        delete_public_bucket()
