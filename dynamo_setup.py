import boto3
import json
import time


# boto3 is the AWS SDK library for Python.
# The "resources" interface allow for a higher-level abstraction than the low-level client interface.
# More details here: http://boto3.readthedocs.io/en/latest/guide/resources.html
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Tutti')


# The BatchWriteItem API allows us to write multiple items to a table in one request.
if True:
    with table.batch_writer() as batch:
        time = int(time.time()-10000)
        print(time)
        row = {"id": -1,
                "epoch_time": time,
        }
        print(row) 
        batch.put_item(Item=row)

if False:
    with table.batch_writer() as batch:
        row = {"id": 0,
                "chat_id": {229891194},
        }
        print(row) 
        batch.put_item(Item=row)
        
        row = {"id": 229891194,
                "keywords": {'car'},
        }
        print(row) 
        batch.put_item(Item=row)

#table.update_item(
#                Key={'id': 229891194},
#                UpdateExpression='add keywords :val',
#                ExpressionAttributeValues={':val': {'deletion'}}
#            )

#check if we can retrieve item
item = table.get_item(Key={'id': -1})
epoch_time = item.get('Item').get('epoch_time')
print(epoch_time)

