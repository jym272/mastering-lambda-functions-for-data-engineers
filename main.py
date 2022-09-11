import os

import boto3

# session = boto3.Session(profile_name='jorge-admin')
# s3 = session.resource('s3')

s3_client = boto3.client('s3')
aws_profile = os.environ.get('AWS_PROFILE')
region = 'sa-east-1'
location = {'LocationConstraint': region}


def createBucket(bucket_name):
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
def deleteBucket(bucket_name):
    s3_client.delete_bucket(Bucket=bucket_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f'Hello, {aws_profile}!')
    for bucket in s3_client.list_buckets()['Buckets']:
        print(bucket['Name'])
    # createBucket('master-lambda-gharchive')
