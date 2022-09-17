import boto3
from datetime import datetime
from datetime import timedelta
import requests
import os
import json

bucket_name = os.environ.get('BUCKET_NAME')


def next_file_to_process(last_run_file_name):
    datetime_part = last_run_file_name.split('.')[0]
    last_run_datetime = datetime.strptime(datetime_part, '%Y-%m-%d-%H')
    next_run_datetime = last_run_datetime + timedelta(hours=1)
    next_run_datetime_string = datetime.strftime(next_run_datetime, '%Y-%m-%d-%-H')
    next_run_file_name = f'{next_run_datetime_string}.json.gz'
    return next_run_file_name


def get_jobs_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'jobs'
    jobs_table = dynamodb.Table(table_name)
    return jobs_table


def get_current_file():
    jobs_table = get_jobs_table()
    job_run_bookmark_details = jobs_table.get_item(
        Key={
            'job_id': os.environ.get('GH_ACTIVITY_INGEST')
        }
    )['Item']['job_run_bookmark_details']
    return job_run_bookmark_details['last_run_file_name']


def initialized_bucket():
    s3_client = boto3.client('s3')
    region = 'sa-east-1'
    location = {'LocationConstraint': region}
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


def put_next_file_in_bucket_and_update_db(next_file):
    s3_client = boto3.client('s3')
    url = f'https://data.gharchive.org/{next_file}'
    response = requests.get(url)
    response_s3 = s3_client.put_object(Bucket=bucket_name, Key=next_file, Body=response.content)

    if response_s3['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'File {next_file} saved in S3')
    else:
        print(f'Error saving file {next_file} in S3')

    jobs_table = get_jobs_table()
    response_dynamo = jobs_table.update_item(
        Key={
            'job_id': os.environ.get('GH_ACTIVITY_INGEST')
        },
        UpdateExpression='SET job_run_bookmark_details.last_run_file_name = :val1',
        ExpressionAttributeValues={
            ':val1': next_file
        }
    )
    if response_dynamo['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'Last run file name updated to {next_file} in the jobs table')
    else:
        print(f'Error updating last run file name in dynamodb')


def init():
    current_file = get_current_file()
    file_to_process = next_file_to_process(current_file)
    initialized_bucket()
    put_next_file_in_bucket_and_update_db(file_to_process)
    return file_to_process


def lambda_main(event, context):
    last_run_file_name = init()

    return {
        'statusCode': 200,
        'body': json.dumps(f'Last run file name: {last_run_file_name}')
    }
