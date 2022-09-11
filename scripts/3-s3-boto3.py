#%%
import boto3
import os
#%%
aws_profile = os.environ.get('AWS_PROFILE')
if aws_profile is None:
    os.environ['AWS_PROFILE'] = 'jorge-admin'
    aws_profile = os.environ.get('AWS_PROFILE')

#%%
s3_client = boto3.client('s3')
region = 'sa-east-1'
location = {'LocationConstraint': region}
bucket_name = 'master-lambda-gharchive'
# print the names of the buckets
for bucket in s3_client.list_buckets()['Buckets']:
    print(bucket['Name'])
#%%
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

#%%




