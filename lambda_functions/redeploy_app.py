import os
import boto3
import zipfile

from utils.aws import aws_init_profile
bucket_name = 'lambda-deploy-app-from-pycharm'
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')
lambda_function_name = 'masterLambdaGHArchive'


def redeploy():
    aws_init_profile()
    with zipfile.ZipFile('app.zip', 'w') as zip_function:
        zip_function.write('lambda_functions/app.py', 'app.py')
    # save app.zip in the bucket
    s3_client.upload_file('app.zip', bucket_name, 'app.zip')
    print(f'File app.zip uploaded')
    # delete app.zip
    os.remove('app.zip')
    response = lambda_client.update_function_code(
        FunctionName=lambda_function_name,
        S3Bucket=bucket_name,
        S3Key='app.zip',
        Publish=True
    )
    # print response status
    print(response['ResponseMetadata']['HTTPStatusCode'])


redeploy()  # ctrl + enter
# %%
