"""
AWS Lambda Function: Cloud Security S3 Auditor
Audits all S3 buckets in the AWS account for public access exposure.
Publishes real-time alert JSON payloads to AWS IoT Core (MQTT) and AWS SNS.
"""

import os
import json
import time
import logging
import boto3
from botocore.exceptions import ClientError

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment Variables
MQTT_TOPIC = os.environ.get('MQTT_TOPIC', 'cloud/security/alerts')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

def handler(event, context):
    logger.info("Starting Cloud Security S3 Auditor scan...")

    s3 = boto3.client('s3')
    iot_data = boto3.client('iot-data')
    sns = boto3.client('sns')

    public_buckets = []
    total_buckets_scanned = 0

    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        total_buckets_scanned = len(buckets)
        logger.info(f"Found {total_buckets_scanned} bucket(s) in account.")

        for bucket in buckets:
            bucket_name = bucket['Name']
            is_public = check_bucket_publicity(s3, bucket_name)
            if is_public:
                public_buckets.append(bucket_name)

    except ClientError as e:
        logger.error(f"Error listing buckets: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    # Determine security state
    alert_triggered = len(public_buckets) > 0
    status = "ALERT" if alert_triggered else "OK"

    payload = {
        "status": status,
        "alert_level": "CRITICAL" if alert_triggered else "NONE",
        "public_buckets_count": len(public_buckets),
        "public_buckets": public_buckets,
        "scanned_total": total_buckets_scanned,
        "timestamp": int(time.time()),
        "scanner": "Lambda_S3_Auditor_v1.0"
    }

    logger.info(f"Scan complete. Status: {status}. Exposed Buckets: {public_buckets}")

    # 1. Publish to AWS IoT Core (MQTT)
    try:
        iot_data.publish(
            topic=MQTT_TOPIC,
            qos=1,
            payload=json.dumps(payload)
        )
        logger.info(f"Successfully published alert payload to AWS IoT Core topic: {MQTT_TOPIC}")
    except Exception as e:
        logger.error(f"Failed to publish to AWS IoT Core: {str(e)}")

    # 2. Publish to AWS SNS (Optional Email / Notification)
    if alert_triggered and SNS_TOPIC_ARN:
        try:
            sns_message = (
                f"SECURITY ALERT: Public S3 Bucket Detected!\n\n"
                f"Count: {len(public_buckets)}\n"
                f"Exposed Bucket(s):\n" + "\n".join([f" - {b}" for b in public_buckets]) + "\n\n"
                f"The physical ESP32 Cloud Security Alert Lamp has been triggered!"
            )
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="[CRITICAL ALERT] Public S3 Bucket Exposed",
                Message=sns_message
            )
            logger.info("Published notification to AWS SNS topic.")
        except Exception as e:
            logger.error(f"Failed to send SNS alert: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }

def check_bucket_publicity(s3_client, bucket_name):
    """
    Evaluates 3 security layers for an S3 bucket:
    1. Account/Bucket PublicAccessBlockConfiguration
    2. Bucket Policy Public Status
    3. Bucket ACL Grants (AllUsers / AuthenticatedUsers)
    """
    logger.info(f"Auditing bucket: {bucket_name}")

    # Layer 1: Check Public Access Block Configuration
    try:
        pab = s3_client.get_public_access_block(Bucket=bucket_name)
        config = pab.get('PublicAccessBlockConfiguration', {})
        # If all 4 blocks are True, the bucket cannot be public via policy/ACL
        if (config.get('BlockPublicAcls') and 
            config.get('IgnorePublicAcls') and 
            config.get('BlockPublicPolicy') and 
            config.get('RestrictPublicBuckets')):
            logger.info(f"Bucket '{bucket_name}' has full Public Access Block enabled. (SECURE)")
            return False
    except ClientError as e:
        # NoSuchPublicAccessBlock error means Public Access Block is NOT configured (potentially vulnerable!)
        if e.response['Error']['Code'] != 'NoSuchPublicAccessBlock':
            logger.warning(f"Could not read PublicAccessBlock for {bucket_name}: {e}")

    # Layer 2: Check Bucket Policy Status (IsPublic)
    try:
        policy_status = s3_client.get_bucket_policy_status(Bucket=bucket_name)
        if policy_status.get('PolicyStatus', {}).get('IsPublic', False):
            logger.warning(f"Bucket '{bucket_name}' bucket policy is marked PUBLIC!")
            return True
    except ClientError as e:
        if e.response['Error']['Code'] not in ['NoSuchBucketPolicy', 'AccessDenied']:
            logger.warning(f"Error checking policy status for {bucket_name}: {e}")

    # Layer 3: Check Bucket ACL Grants
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get('Grants', []):
            grantee = grant.get('Grantee', {})
            grantee_uri = grantee.get('URI', '')
            if 'AllUsers' in grantee_uri or 'AuthenticatedUsers' in grantee_uri:
                logger.warning(f"Bucket '{bucket_name}' has public ACL grant to {grantee_uri}!")
                return True
    except ClientError as e:
        logger.warning(f"Could not read ACL for {bucket_name}: {e}")

    return False
