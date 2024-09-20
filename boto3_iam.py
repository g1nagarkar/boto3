import boto3
from botocore.exceptions import ClientError

try:
    # Configure AWS credentials using boto3
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY',
        aws_secret_access_key='YOUR_SECRET_KEY',
        region_name='ap-south-1'
    )

    iam = session.client('iam')
    user_name = "shaktiman"
    
    # Step 1: Create new IAM user
    try:
        iam.create_user(UserName=user_name)
        print(f"IAM user {user_name} created.")
    except ClientError.exceptions.EntityAlreadyExistsException as e:
        print(f"IAM user {user_name} already exists.")
    except ClientError as e:
        print(f"Error creating user {user_name}: {e}")
        exit(1)  # Exit if user creation fails

    # Step 2: Attach policy to newly created user
    try:
        iam.attach_user_policy(
            UserName=user_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
        print(f'Policy attached to {user_name}.')
    except ClientError.exceptions.NoSuchEntityException as e:
        print(f"Policy {e} does not exist.")
    except ClientError as e:
        print(f"Error attaching policy to user {user_name}: {e}")

    # Step 3: List all IAM users
    try:
        user_list = iam.list_users()
        print("Listing all IAM users:")
        for user in user_list['Users']:
            print(f'User Name: {user["UserName"]}')
    except ClientError.exceptions.ServiceFailureException as e:
        print(f"Error listing users: {e}")
    except ClientError as e:
        print(f"Error listing users: {e}")

    # Step 4: Describe the user's attached managed policies
    try:
        managed_policies = iam.list_attached_user_policies(UserName=user_name)
        if managed_policies['AttachedPolicies']:
            for policy in managed_policies['AttachedPolicies']:
                print(f"Managed policy - {policy['PolicyName']} (ARN: {policy['PolicyArn']})")
        else:
            print(f"No managed policies attached to {user_name}.")
    except ClientError as e:
        print(f"Error listing managed policies for user {user_name}: {e}")

    # Step 5: Describe the user's inline policies
    try:
        inline_policies = iam.list_user_policies(UserName=user_name)
        if inline_policies['PolicyNames']:
            for policy in inline_policies['PolicyNames']:
                print(f"Inline policy - {policy}")
        else:
            print(f"No inline policies attached to {user_name}.")
    except ClientError as e:
        print(f"Error listing inline policies for user {user_name}: {e}")

    # Step 6: Detach the policy from the user
    try:
        iam.detach_user_policy(
            UserName=user_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
        print("Policy detached successfully.")
    except ClientError as e:
        print(f"Error detaching policy from user {user_name}: {e}")

    # Step 7: Delete the IAM user
    try:
        iam.delete_user(UserName=user_name)
        print(f'IAM user {user_name} deleted.')
    except ClientError as e:
        print(f"Error deleting user {user_name}: {e}")

except Exception as e:
    print(f'Unexpected error: {e}')
