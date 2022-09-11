# %%
import boto3
import os

# %%
aws_profile = os.environ.get('AWS_PROFILE')
if aws_profile is None:
    os.environ['AWS_PROFILE'] = 'jorge-admin'
    aws_profile = os.environ.get('AWS_PROFILE')

# %%
s3_client = boto3.client('s3')
region = 'sa-east-1'
location = {'LocationConstraint': region}
bucket_name = 'master-lambda-gharchive'
# print the names of the buckets
for bucket in s3_client.list_buckets()['Buckets']:
    print(bucket['Name'])

# %%
is_already_created = False
for bucket in s3_client.list_buckets()['Buckets']:
    if bucket['Name'] == 'master-lambda-gharchive':
        is_already_created = True
        break
if not is_already_created:
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    print(f'Bucket {bucket_name} created')
else:
    print(f'Bucket {bucket_name} already exists')
# %%
string_object = 'Hello World!'
bytes_object = bytes(string_object, 'utf-8')
# put bytes object
s3_client.put_object(Bucket=bucket_name, Key='hello-world', Body=bytes_object)
# %%
# get bytes object in string format
response = s3_client.get_object(Bucket=bucket_name, Key='hello-world')
bytes_body = response['Body'].read()
string_body = bytes_body.decode('utf-8')
string_body
