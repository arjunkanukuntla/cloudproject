#!/usr/bin/env python3
"""
Automated AWS Teardown & Pause Script: Cloud Security Alert Lamp
Allows pausing or completely deleting all AWS resources from the terminal.

Usage:
  python destroy_aws.py --pause      -> Pauses AWS scanning (disables EventBridge cron, zero lambda triggers)
  python destroy_aws.py --resume     -> Resumes AWS scanning (enables EventBridge cron)
  python destroy_aws.py --delete-all -> Completely tears down & deletes all AWS resources (Lambda, IoT, DynamoDB, SNS, S3, Rules)
"""

import sys
import os
import argparse
import boto3
from botocore.exceptions import ClientError

def print_header(title):
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)

def pause_schedule(events, rule_name='CloudSecurityAuditorSchedule'):
    print(f"[*] Pausing scheduled scans by disabling EventBridge rule '{rule_name}'...")
    try:
        events.disable_rule(Name=rule_name)
        print(f"[+] SUCCESS: EventBridge rule '{rule_name}' is now DISABLED.")
        print("[+] Lambda will no longer trigger automatically. No ongoing compute costs.")
    except ClientError as e:
        print(f"[-] Note: {e}")

def resume_schedule(events, rule_name='CloudSecurityAuditorSchedule'):
    print(f"[*] Resuming scheduled scans by enabling EventBridge rule '{rule_name}'...")
    try:
        events.enable_rule(Name=rule_name)
        print(f"[+] SUCCESS: EventBridge rule '{rule_name}' is now ENABLED.")
        print("[+] Lambda auditor will run every 5 minutes.")
    except ClientError as e:
        print(f"[-] Note: {e}")

def delete_all_resources(region):
    print_header("TEARING DOWN ALL AWS RESOURCES")

    # 1. EventBridge Rule & Targets
    print("\n[1/7] Removing EventBridge Rule...")
    events = boto3.client('events', region_name=region)
    rule_name = 'CloudSecurityAuditorSchedule'
    try:
        targets_res = events.list_targets_by_rule(Rule=rule_name)
        target_ids = [t['Id'] for t in targets_res.get('Targets', [])]
        if target_ids:
            events.remove_targets(Rule=rule_name, Ids=target_ids)
            print(f"  [+] Removed {len(target_ids)} target(s) from rule '{rule_name}'.")
        events.delete_rule(Name=rule_name)
        print(f"  [+] Deleted EventBridge rule '{rule_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"  [*] EventBridge rule '{rule_name}' does not exist.")
        else:
            print(f"  [-] EventBridge cleanup note: {e}")

    # 2. Lambda Function
    print("\n[2/7] Deleting AWS Lambda Function...")
    lambda_client = boto3.client('lambda', region_name=region)
    function_name = 'CloudSecurityS3Auditor'
    try:
        lambda_client.delete_function(FunctionName=function_name)
        print(f"  [+] Deleted Lambda function '{function_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"  [*] Lambda function '{function_name}' not found.")
        else:
            print(f"  [-] Lambda cleanup note: {e}")

    # 3. DynamoDB Table
    print("\n[3/7] Deleting Amazon DynamoDB Table...")
    dynamodb = boto3.client('dynamodb', region_name=region)
    table_name = 'SecurityEvents'
    try:
        dynamodb.delete_table(TableName=table_name)
        print(f"  [+] Deleted DynamoDB table '{table_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"  [*] DynamoDB table '{table_name}' not found.")
        else:
            print(f"  [-] DynamoDB cleanup note: {e}")

    # 4. SNS Topic
    print("\n[4/7] Deleting Amazon SNS Topic...")
    sns = boto3.client('sns', region_name=region)
    try:
        topics_res = sns.list_topics()
        for t in topics_res.get('Topics', []):
            if 'CloudSecurityAlerts' in t['TopicArn']:
                sns.delete_topic(TopicArn=t['TopicArn'])
                print(f"  [+] Deleted SNS Topic: {t['TopicArn']}")
    except ClientError as e:
        print(f"  [-] SNS cleanup note: {e}")

    # 5. AWS IoT Core (Principals, Certificates, Policies, Thing)
    print("\n[5/7] Deleting AWS IoT Core Resources...")
    iot = boto3.client('iot', region_name=region)
    thing_name = 'SecurityAlertLamp'
    policy_name = 'CloudSecurityAlertLampPolicy'

    # Detach & delete principals/certificates from Thing
    try:
        principals = iot.list_thing_principals(thingName=thing_name).get('principals', [])
        for principal_arn in principals:
            iot.detach_thing_principal(thingName=thing_name, principal=principal_arn)
            print(f"  [+] Detached principal {principal_arn} from thing.")

            # Detach policies from certificate
            try:
                attached_policies = iot.list_attached_policies(target=principal_arn).get('policies', [])
                for pol in attached_policies:
                    iot.detach_policy(policyName=pol['policyName'], target=principal_arn)
                    print(f"  [+] Detached policy {pol['policyName']} from certificate.")
            except Exception:
                pass

            # Deactivate and delete certificate
            cert_id = principal_arn.split('/')[-1]
            try:
                iot.update_certificate(certificateId=cert_id, newStatus='INACTIVE')
                iot.delete_certificate(certificateId=cert_id, forceDelete=True)
                print(f"  [+] Deactivated & deleted certificate: {cert_id}")
            except Exception as ce:
                print(f"  [-] Certificate cleanup note: {ce}")

        # Delete Thing
        iot.delete_thing(thingName=thing_name)
        print(f"  [+] Deleted IoT Thing '{thing_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"  [*] IoT Thing '{thing_name}' not found.")
        else:
            print(f"  [-] IoT Thing cleanup note: {e}")

    # Delete IoT Policy
    try:
        iot.delete_policy(policyName=policy_name)
        print(f"  [+] Deleted IoT Policy '{policy_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"  [*] IoT Policy '{policy_name}' not found.")
        else:
            print(f"  [-] IoT Policy cleanup note: {e}")

    # 6. Test Public S3 Buckets
    print("\n[6/7] Removing Test Public S3 Buckets...")
    s3 = boto3.client('s3')
    bucket_prefix = "test-public-vulnerable-lamp-"
    try:
        buckets = s3.list_buckets().get('Buckets', [])
        for b in buckets:
            b_name = b['Name']
            if b_name.startswith(bucket_prefix):
                try:
                    s3.delete_bucket_policy(Bucket=b_name)
                except Exception:
                    pass
                s3.delete_bucket(Bucket=b_name)
                print(f"  [+] Deleted test vulnerable bucket: {b_name}")
    except Exception as e:
        print(f"  [-] S3 cleanup note: {e}")

    # 7. Custom IAM Role (if created, skip LabRole)
    print("\n[7/7] Cleaning up custom IAM Role (if applicable)...")
    iam = boto3.client('iam')
    custom_role = 'CloudSecurityAuditorRole'
    try:
        attached = iam.list_attached_role_policies(RoleName=custom_role).get('AttachedPolicies', [])
        for p in attached:
            iam.detach_role_policy(RoleName=custom_role, PolicyArn=p['PolicyArn'])
            print(f"  [+] Detached policy {p['PolicyArn']} from {custom_role}.")
        iam.delete_role(RoleName=custom_role)
        print(f"  [+] Deleted custom IAM Role '{custom_role}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print(f"  [*] Custom IAM Role '{custom_role}' not present (or using AWS LabRole).")
        else:
            print(f"  [-] IAM cleanup note: {e}")

    print_header("ALL AWS RESOURCES REMOVED SUCCESSFULLY!")

def main():
    parser = argparse.ArgumentParser(
        description="AWS Teardown & Pause Utility for Cloud Security Alert Lamp"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--pause',
        action='store_true',
        help='Pause scheduled scans (disables EventBridge trigger, stops Lambda execution)'
    )
    group.add_argument(
        '--resume',
        action='store_true',
        help='Resume scheduled scans (enables EventBridge trigger)'
    )
    group.add_argument(
        '--delete-all',
        action='store_true',
        help='Permanently delete ALL AWS resources created for this project'
    )

    args = parser.parse_args()

    # Authenticate
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        account_id = identity['AccountId']
        print(f"[+] Authenticated AWS Account: {account_id}")
    except Exception as e:
        print(f"[-] ERROR: Failed to authenticate with AWS: {e}")
        print("    Ensure AWS credentials are configured in your terminal.")
        sys.exit(1)

    region = boto3.Session().region_name or 'us-east-1'
    events = boto3.client('events', region_name=region)

    if args.pause:
        pause_schedule(events)
    elif args.resume:
        resume_schedule(events)
    elif args.delete_all:
        confirm = input("\nWARNING: This will permanently delete Lambda, DynamoDB, IoT Thing, and SNS topics.\nAre you sure? (y/N): ")
        if confirm.lower() == 'y':
            delete_all_resources(region)
        else:
            print("[*] Aborted by user. No resources deleted.")

if __name__ == '__main__':
    main()
