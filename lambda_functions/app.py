# lambda_function_name = 'masterLambdaGHArchive'
import json
import boto3


def lambda_main(event, context):
    # TODO implement
    s3_client = boto3.client('s3')
    list_of_buckets = []
    for bucket in s3_client.list_buckets()['Buckets']:
        list_of_buckets.append(bucket['Name'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambdaa!'),
        'list_of_buckets': list_of_buckets
    }
