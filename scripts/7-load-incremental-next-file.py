# %%
import boto3
import os
from datetime import datetime
from datetime import timedelta
import requests

# %%
aws_profile = os.environ.get('AWS_PROFILE')
if aws_profile is None:
    os.environ['AWS_PROFILE'] = 'jorge-admin'
    aws_profile = os.environ.get('AWS_PROFILE')
print(aws_profile)
# %%
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
# details of the job with job_id = 'ghactivity-ingest' if exists
job_id = 'ghactivity-ingest'
details_of_ghactivity_ingest = jobs_table.get_item(
    Key={
        'job_id': job_id
    }
)['Item']
baseline_days = details_of_ghactivity_ingest['baseline_days']
details_of_ghactivity_ingest
# %%
three_days_ago = datetime.now().date() - timedelta(days=3)
three_days_ago_string = datetime.strftime(three_days_ago, '%Y-%m-%d')
start_file = f'{three_days_ago_string}-0.json.gz'
print(start_file)
# %%
item_job_details = {
    'job_id': 'ghactivity-ingest',
    'job_description': 'Ingest ghactivity data to S3',
    'is_active': 'Y',
    'baseline_days': 3,
    'job_run_bookmark_details': {
        'last_run_file_name': start_file
    }
}
jobs_table.put_item(Item=item_job_details)
# %%
job_run_bookmark_details = details_of_ghactivity_ingest['job_run_bookmark_details']
job_run_bookmark_details


# %%
def next_file_to_process(last_run_file_name):
    datetime_part = last_run_file_name.split('.')[0]
    # increment by a hour
    last_run_datetime = datetime.strptime(datetime_part, '%Y-%m-%d-%H')
    next_run_datetime = last_run_datetime + timedelta(hours=1)
    next_run_datetime_string = datetime.strftime(next_run_datetime, '%Y-%m-%d-%-H')
    next_run_file_name = f'{next_run_datetime_string}.json.gz'
    return next_run_file_name


next_file_to_process(job_run_bookmark_details['last_run_file_name'])
# %%
file_name = job_run_bookmark_details['last_run_file_name']
for i in range(3):
    response = requests.get(f'https://data.gharchive.org/{file_name}')
    path = 'scripts/data/' + file_name
    with open(path, 'wb') as f:
        f.write(response.content)
    file_name = next_file_to_process(file_name)
# %%

