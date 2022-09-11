# %%
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
# tableName = 'jobs'
# primaryKey = 'job_id'
# keyType = 'S'
table_name = 'jobs'
primary_key = 'job_id'
key_type = 'S'  # string
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': key_type
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
# describe the table jobs
job_table = dynamodb.Table(table_name)
print(job_table.creation_date_time)
print(job_table.item_count)
print(job_table.table_status)
print(job_table.table_arn)
print(job_table.table_name)
print(job_table.key_schema)
print(job_table.attribute_definitions)
print(job_table.provisioned_throughput)
# %%
now = datetime.now()
new_item = {
    'job_id': 'job-1',
    'job_description': 'Ingest ghactivity data to s3',
    'job_status': 'running',
    'job_start_time': now.strftime("%d/%m/%Y %H:%M:%S"),
    'is_active': 'Y'
}
# insert new item
job_table.put_item(Item=new_item)
# %%
# check all items in table jobs
for item in job_table.scan()['Items']:
    print(item)
# %%
# get the item with key job_id = job-1
item = job_table.get_item(Key={'job_id': 'job-1'})
print(item['Item'])
# %%