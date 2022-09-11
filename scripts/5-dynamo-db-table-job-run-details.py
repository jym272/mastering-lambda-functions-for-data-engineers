# %%
import time
from datetime import datetime

import boto3

# %%
dynamodb = boto3.resource('dynamodb')
# %%
# list of all tables
for table in dynamodb.tables.all():
    print(table.name)
# %%
# create table if not exists,
table_name = 'job_run_details'
# composite key (partition key and sort key): partition key is job_id, sort key is run_id
primary_key = 'job_id'
sort_key = 'run_id'

try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': sort_key,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            },
            {
                'AttributeName': sort_key,
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f'Table {table_name} created')
except Exception as e:
    print(f'Table {table_name} already exists')
    print(e)
# %%
job_run_details_table = dynamodb.Table(table_name)
# %%

# %%
# new item
run_time = int(time.mktime(datetime.now().timetuple()))

new_item = {
    'job_id': 'job-1',
    'run_id': run_time,
    'job_run_bookmark_details': {
        'processed_file_name': '2022-06-03-0.json.gz',
    }
}
# insert new item
job_run_details_table.put_item(Item=new_item)
# %%
# check all items in table jobs
job_table = dynamodb.Table('jobs')
for item in job_table.scan()['Items']:
    print(item)

# check all items in table job_run_details_table
print(' Job Run Details Table '.center(80, '-'))
for item in job_run_details_table.scan()['Items']:
    print(item)

# %%
# get the item with key job_id = job-1
item = job_table.get_item(Key={'job_id': 'job-1'})
print(item['Item'])
# %%
