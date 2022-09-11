#%%
import boto3
import os
#%%
aws_profile = os.environ.get('AWS_PROFILE')
if aws_profile is None:
    os.environ['AWS_PROFILE'] = 'jorge-admin'
    aws_profile = os.environ.get('AWS_PROFILE')
print(aws_profile)
#%%
dynamodb = boto3.resource('dynamodb')
# list of all tables
for table in dynamodb.tables.all():
    print(table.name)
# %%
table_name = 'jobs'
jobs_table = dynamodb.Table(table_name)
# %%
# all items in table
for item in jobs_table.scan()['Items']:
    print(item)
# %%
# delete the item with job_id = 'job-1' if exists
job_id = 'job-1'
response = jobs_table.delete_item(
    Key={
        'job_id': job_id
    }
)
print(response)
# %%
item_job_details = {
    'job_id': 'ghactivity-ingest',
    'job_description': 'Ingest ghactivity data to S3',
    'is_active': 'Y',
    'baseline_days': 3
    }
jobs_table.put_item(Item=item_job_details)
# %%