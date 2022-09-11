#%%
import boto3
import os
from datetime import datetime
from datetime import timedelta
import requests
import pandas as pd
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
three_days_ago = datetime.now().date() - timedelta(days=3)
three_days_ago_string = datetime.strftime(three_days_ago, '%Y-%m-%d')
next_file_to_process = f'{three_days_ago_string}-0.json.gz'
print(next_file_to_process)
# %%
response = requests.get(f'https://data.gharchive.org/{next_file_to_process}')

path = 'scripts/data/' + next_file_to_process
with open(path, 'wb') as f:
    f.write(response.content)
# %%
# read json with pandas
df = pd.read_json(path, lines=True)
# %%
df.count()
# %%
head = df.head(3)
