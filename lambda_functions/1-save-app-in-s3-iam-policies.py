# %%
import boto3
import os
import zipfile

from utils.aws import aws_init_profile

# %%
aws_init_profile()

# %%
s3_client = boto3.client('s3')
region = 'sa-east-1'
location = {'LocationConstraint': region}
bucket_name = 'lambda-deploy-app-from-pycharm'
lambda_function_name = 'masterLambdaGHArchive'

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
lambda_client = boto3.client('lambda')
with zipfile.ZipFile('app.zip', 'w') as zip_function:
    zip_function.write('lambda_functions/app.py', 'app.py')

# save app.zip in the bucket
s3_client.upload_file('app.zip', bucket_name, 'app.zip')
print(f'File app.zip uploaded')
# delete app.zip
os.remove('app.zip')


# %%
# check all files in the bucket
for file in s3_client.list_objects(Bucket=bucket_name)['Contents']:
    print(file['Key'])

# %%
# list all lambda functions
for function in lambda_client.list_functions()['Functions']:
    print(function['FunctionName'])
# %% --------------------------------------------- (REDEPLOY app.py 2/2) Modify a lambda function
# modify a lambda function
lambda_client.update_function_code(
    FunctionName=lambda_function_name,
    S3Bucket=bucket_name,
    S3Key='app.zip',
    Publish=True
)
# %%
# iam role of the lambda function
iam_client = boto3.client('iam')
role = lambda_client.get_function_configuration(FunctionName=lambda_function_name)['Role']
role

# %%
# list all policies of the lambda function
for policy in iam_client.list_attached_role_policies(RoleName=role.split('/')[-1])['AttachedPolicies']:
    print(policy['PolicyName'])

# %% -----------------add AmazonS3ReadOnlyAccess------------ (UPDATE POLICIES) Update policies to lambda function
# add permissions to list buckets of s3 to the lambda function
iam_client.attach_role_policy(
    RoleName=role.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
# %%
# add permission to dynamodb:GetItem to the lambda function
iam_client.attach_role_policy(
    RoleName=role.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess'
)
# %%
# add permission to putobject in s3 to the lambda function
iam_client.attach_role_policy(
    RoleName=role.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)
# %%
# add permission to UpdateItem in dynamoDb to the lambda function
iam_client.attach_role_policy(
    RoleName=role.split('/')[-1],
    PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
)
# %%
# configurar environment var en lambda
# 'GH_ACTIVITY_INGEST' = 'ghactivity-ingest'
# 'AWS_PROFILE' = 'jorge-admin'
# 'BUCKET_NAME' = 'master-lambda-gharchive'
lambda_client.update_function_configuration(
    FunctionName=lambda_function_name,
    Environment={
        'Variables': {
            'GH_ACTIVITY_INGEST': 'ghactivity-ingest',
            'BUCKET_NAME': 'master-lambda-gharchive'
        }
    }
)
# %%
# increase memory of the lambda function to 512 MB
lambda_client.update_function_configuration(
    FunctionName=lambda_function_name,
    MemorySize=512
)
# %%
# increase timeout of the lambda function to 10 seconds
lambda_client.update_function_configuration(
    FunctionName=lambda_function_name,
    Timeout=10
)

# %%   ----------------------------------- Check layer/script.py
# list of layers
layer_version_arn = ''
layer_name= 'myLayer'
for layer in lambda_client.list_layers()['Layers']:
    print(layer)
    if layer['LayerName'] == layer_name:
        layer_version_arn = layer['LatestMatchingVersion']['LayerVersionArn']
        break
print(layer_version_arn)
# %%
# add layer to the lambda function
lambda_client.update_function_configuration(
    FunctionName=lambda_function_name,
    Layers=[
        layer_version_arn,
    ]
)

# %%
# delete version of the layer from  1 to 12
for version in range(1, 13):
    lambda_client.delete_layer_version(
        LayerName=layer_name,
        VersionNumber=version
    )
print('Versions from 1 to 12 deleted')
