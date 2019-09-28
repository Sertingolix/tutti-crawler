import json, os, boto3
import traceback

from send import send_message, send_message_item
from crawl_tutti import crawl_tutti
from handle_request import handle_message

#generate Telegram API url
TOKEN=os.environ['TELEGRAM_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#get table 
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Tutti')

def lambda_handler(event, context):

    try:
        #distinguish betwee cloudwatch trigger (every 15 minutes)
        #and a telegramm message/command
        if 'body' not in event:
            print('crawl tutti.ch')
            crawl_tutti(URL, table)
        else:
            print('do db updates or handle commands')
            
            data = json.loads(event['body'])
            
            handle_message(data = data, URL = URL, table = table)
            

    except Exception as e:
        tb = traceback.format_exc()
        print(e)
    else:
        tb = "No error"
    finally:
        print(tb)
    return {"statusCode": 200}
