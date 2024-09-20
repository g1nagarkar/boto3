import boto3
from botocore.exceptions import ClientError


try:
    # Configure AWS credentials using boto3 session
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='us-west-2'
    )

    ec2 = session.client('ec2')

    # Step 1: Get all EC2 instances and their running states
    try:
        response = ec2.describe_instances()
        if not response['Reservations']:
            print("No EC2 instances found.")
        else:
            print("Listing EC2 instances and their states:")
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    print(f'Instance ID: {instance["InstanceId"]}, State: {instance["State"]["Name"]}')
    except ClientError as e:
        print(f"Error describing EC2 instances: {e}")

    # Step 2: Start a specific EC2 instance
    instance_id = 'i-0123456789abcdef'  # Replace with your instance ID
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        print(f'EC2 Instance {instance_id} started.')
    except ClientError as e:
        print(f"Error starting instance {instance_id}: {e}")

    # Step 3: Stop a specific EC2 instance
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f'EC2 Instance {instance_id} stopped.')
    except ClientError as e:
        print(f"Error stopping instance {instance_id}: {e}")

except Exception as e:
    print(f'Unexpected error: {e}')
