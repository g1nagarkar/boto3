import boto3
from botocore.exceptions import ClientError

try:
    # Configure AWS credentials using boto3 session
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='ap-south-1'
    )

    s3 = session.client('s3')

    # Step 1: List all S3 buckets
    try:
        response = s3.list_buckets()
        if response['Buckets']:
            print("Listing S3 buckets:")
            for bucket in response['Buckets']:
                print(f'Bucket Name: {bucket["Name"]}')
        else:
            print("No buckets found.")
    except ClientError as e:
        print(f"Error listing S3 buckets: {e}")

    # Step 2: Create an S3 bucket
    bucket_name = 'boto3-my-bucket'
    location = {'LocationConstraint': 'ap-south-1'}
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket '{bucket_name}' created in S3.")
    except ClientError as e:
        print(f"Error creating bucket {bucket_name}: {e}")

    # Step 3: Upload file to S3 bucket
    try:
        s3.upload_file('requirements.txt', bucket_name, 'requirements.txt')
        print("File 'requirements.txt' uploaded to S3.")
    except ClientError as e:
        print(f"Error uploading file to bucket {bucket_name}: {e}")
    except FileNotFoundError:
        print("Error: 'requirements.txt' file not found.")
    
    # Step 4: Download file from S3 bucket
    try:
        s3.download_file(bucket_name, 'requirements.txt', 'requirements_download.txt')
        print("File 'requirements.txt' downloaded from S3.")
    except ClientError as e:
        print(f"Error downloading file from bucket {bucket_name}: {e}")
    except FileNotFoundError:
        print("Error: 'requirements.txt' not found in the bucket.")

    # Step 5: Delete the file from S3 bucket
    try:
        s3.delete_object(Bucket=bucket_name, Key='requirements.txt')
        print(f"File 'requirements.txt' deleted from S3.")
    except ClientError as e:
        print(f"Error deleting file from bucket {bucket_name}: {e}")

    # Step 6: Delete the S3 bucket
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted from S3.")
    except ClientError as e:
        print(f"Error deleting bucket {bucket_name}: {e}")

except Exception as e:
    print(f'Unexpected error: {e}')
