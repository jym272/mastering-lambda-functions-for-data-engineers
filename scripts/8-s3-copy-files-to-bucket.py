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
# list of files in the bucket
list_of_names = []
for file in s3_client.list_objects(Bucket=bucket_name)['Contents']:
    print(f'{file["LastModified"]} \t {file["Key"]}')
    list_of_names.append(file['Key'])
# %%

# copy all files from scripts/data to s3 master-lambda-gharchive bucket only if the file is not already in the bucket
relative_path = 'scripts/data'
for file in os.listdir(relative_path):
    if file not in list_of_names:
        s3_client.upload_file(f'{relative_path}/{file}', bucket_name, file)
        print(f'File {file} uploaded')
    else:
        print(f'File {file} already exists')

# %%
help(s3_client.upload_file)
