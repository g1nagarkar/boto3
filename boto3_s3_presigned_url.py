import json
import boto3
from botocore.exceptions import ClientError
import requests

try:
    # Configure AWS credentials using boto3 session
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='ap-south-1'
    )

    s3 = session.client('s3')
    
    # Create an S3 bucket
    bucket_name = 'boto3-my-bucket'
    location = {'LocationConstraint': 'ap-south-1'}
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket '{bucket_name}' created in S3.")
    except ClientError as e:
        print(f"Error creating bucket {bucket_name}: {e}")
          
    print("-------------------------------------------------------------------------------------")
    # Generate a pre-signed URL to upload a file to an S3 bucket
        
    file_name = 'aa.jpg'
    try:
        response_upload = s3.generate_presigned_post(bucket_name, file_name,
                                                    ExpiresIn=3600)
        print(f"Pre-signed URL object for upload using post method: {response_upload}")
    except ClientError as e:
        print(f"Error generating pre-signed URL for upload: {e}")
        
        
    # Upload a file to an S3 bucket
    try:
        with open(file_name, 'rb') as f:
            files = {'file': (file_name, f)}
            http_response = requests.post(response_upload['url'], data=response_upload['fields'], files=files)
            if http_response.status_code == 204:
                print(f"File {file_name} uploaded successfully.")
            else:
                print(f"File upload failed with status code: {http_response.status_code}")
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        
    print("-------------------------------------------------------------------------------------")
    new_file = 'README.md'
    
    try:
        response_url = s3.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name, 'Key': new_file},
                                                    ExpiresIn=3600)
        print(f"Pre-signed URL for upload using put_object: {response_url} ")
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
    
    new_file_path = './README.md'

    # Open the file in binary mode
    with open(new_file_path, 'rb') as f:
        # Make a PUT request to upload the file
        response = requests.put(response_url, data=f)

    # Check the status of the upload
    if response.status_code == 200:
        print(f"File {new_file} successfully uploaded.")
    else:
        print(f"File upload failed with status code: {response.status_code}")       
    
    print("-------------------------------------------------------------------------------------") 

    # Generate a pre-signed URL to share an S3 object for download.
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': new_file,},
                                                    ExpiresIn=3600)
        print(f"Pre-signed URL for download: {response}")
        
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        
    print("-------------------------------------------------------------------------------------")
    # Generate a pre-signed URL to list an S3 object .
    try:
        response = s3.generate_presigned_url('list_objects_v2',
                                                    Params={'Bucket': bucket_name,},
                                                    ExpiresIn=3600)
        print(f"Pre-signed URL to list buckets : {response}")
        
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
    
except Exception as e:
    print(f'Unexpected error: {e}')