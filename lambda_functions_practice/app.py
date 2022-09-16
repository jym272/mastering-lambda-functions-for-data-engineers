# lambda_function_name = 'masterLambdaGHArchive'
import json
import boto3
import os
import subprocess
import requests
import pandas as pd


# event
# {
#     'bucket_name': 'lambda-deploy-app-from-pycharm',
# }


def check_pip_list():
    print('pip list:')
    pip_list = subprocess.run(['pip', 'list'], capture_output=True)
    print(pip_list.stdout.decode('utf-8'))


def print_env_variable(key):
    print(f'{key}: {os.environ[key]}')


def lambda_main(event, context):
    s3_client = boto3.client('s3')
    list_of_buckets = []
    names_of_files = []

    print_env_variable('BUCKET_NAME')
    check_pip_list()

    # check if bucket_name is provided in event
    if 'bucket_name' in event:
        bucket_name = event['bucket_name']
        # check if bucket_name exists
        for bucket in s3_client.list_buckets()['Buckets']:
            if bucket['Name'] == bucket_name:
                list_of_buckets.append(bucket['Name'])
                # check if bucket_name has files
                for file in s3_client.list_objects(Bucket=bucket_name)['Contents']:
                    names_of_files.append(file['Key'])
    else:
        for bucket in s3_client.list_buckets()['Buckets']:
            list_of_buckets.append(bucket['Name'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'list_of_buckets': list_of_buckets,
        'names_of_files': names_of_files
    }
