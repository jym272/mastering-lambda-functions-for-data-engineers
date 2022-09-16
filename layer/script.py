# %%
import zipfile
from utils.aws import aws_init_profile
import boto3
import os
import subprocess

# %%
aws_init_profile()

# %%
s3_client = boto3.client('s3')
region = 'sa-east-1'
location = {'LocationConstraint': region}
bucket_name = 'lambda-layer-deploy-from-pycharm'
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
# %% Create python package with request lib in it
subprocess.call(['./layer/create_python_dir.sh'])

# %% Create zipFile and upload to S3 bucket
lambda_client = boto3.client('lambda')
name_of_zip_file = 'lambda-layer.zip'
with zipfile.ZipFile(name_of_zip_file, 'w') as zip_module:
    for root, dirs, files in os.walk('layer/venv/lib/python3.9/site-packages'):
        for file in files:
            zip_module.write(os.path.join(root, file), os.path.join(root, file).replace('layer/venv/lib/python3.9'
                                                                                        '/site-packages/', 'python/'))
print(f'File {name_of_zip_file} created')
s3_client.upload_file(name_of_zip_file, bucket_name, name_of_zip_file)
print(f'File {name_of_zip_file} uploaded to bucket {bucket_name}')
os.remove(name_of_zip_file)
print(f'File {name_of_zip_file} deleted')
# delete python dir
os.system('rm -rf layer/venv')
print(f'Dir layer/venv deleted')

# %%
# create a lambda layer and upload the zip file
lambda_client.publish_layer_version(
    LayerName='myLayer',
    Description='My layer',
    Content={
        'S3Bucket': bucket_name,
        'S3Key': name_of_zip_file
    },
    CompatibleRuntimes=['python3.9']
)


# %%
# list all lambda layers
for layer in lambda_client.list_layers()['Layers']:
    print(layer['LayerName'])
# %%
