# %%
import boto3
import os
import zipfile

# %%
aws_profile = os.environ.get('AWS_PROFILE')
if aws_profile is None:
    os.environ['AWS_PROFILE'] = 'jorge-admin'
    aws_profile = os.environ.get('AWS_PROFILE')

# %%
s3_client = boto3.client('s3')
region = 'sa-east-1'
location = {'LocationConstraint': region}
bucket_name = 'lambda-deploy-app-from-pycharm'
# print the names of the buckets
for bucket in s3_client.list_buckets()['Buckets']:
    print(bucket['Name'])

# %%
is_already_created = False
for bucket in s3_client.list_buckets()['Buckets']:
    if bucket['Name'] == bucket_name:
        is_already_created = True
        break
if not is_already_created:
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    print(f'Bucket {bucket_name} created')
else:
    print(f'Bucket {bucket_name} already exists')

# %% --------------------------------------------- (REDEPLOY app.py 1/2) Zip app.py into app.zip
# zip app.py ito app.zip
with zipfile.ZipFile('app.zip', 'w') as zip_function:
    zip_function.write('lambda_functions/app.py', 'app.py')

# save app.zip in the bucket
s3_client.upload_file('app.zip', bucket_name, 'app.zip')
print(f'File app.zip uploaded')

# %%
# check all files in the bucket
for file in s3_client.list_objects(Bucket=bucket_name)['Contents']:
    print(file['Key'])

# %%
lambda_client = boto3.client('lambda')
# list all lambda functions
for function in lambda_client.list_functions()['Functions']:
    print(function['FunctionName'])
# %% --------------------------------------------- (REDEPLOY app.py 2/2) Modify a lambda function
# modify a lambda function
lambda_function_name = 'masterLambdaGHArchive'
lambda_client.update_function_code(
    FunctionName=lambda_function_name,
    S3Bucket=bucket_name,
    S3Key='app.zip',
    Publish=True
)
# %% --------------------------------------------- (UPDATE POLICIES) Update policies to lambda function
# iam role of the lambda function

role = lambda_client.get_function_configuration(FunctionName=lambda_function_name)['Role']
role

# %%
# add permissions to list buckets of s3 to the lambda function
iam_client = boto3.client('iam')
iam_client.attach_role_policy(
    RoleName=role.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)

# %%



