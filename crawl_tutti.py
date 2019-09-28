from send import send_message, send_message_item
from botocore.vendored import requests
import json


def get_tutti_json(whole_switzerland=True):
    #crawl tutti for the most recent products
    header = {
            "X-Tutti-Hash": "a275c2cc-8f54-4444-87a1-8b743dc868d4",
            "X-Tutti-Source": "web LIVE-190611-29"
    }
    
    if whole_switzerland:
        # whole switzerland: 
        r = requests.get(url="https://api.tutti.ch/v10/list.json?limit=30&o=1&region=4&sp=1&with_all_regions=true", headers=header)
    else:
        # zurich:
        r = requests.get(url="https://api.tutti.ch/v10/list.json?limit=30&o=1&region=23&sp=1&with_all_regions=false",headers=header)
    
    if r.status_code == requests.codes.ok:
        data = json.loads(r.text)
        return int(data['epoch_time']), data['items']
    else:
        return None, {}

def get_new_items(items, time):
    # only keep items which are new
    items = list(items)
    items = [item for item in items if item['epoch_time']>time]
    return items
    
def crawl_tutti(URL, table):
    
    item = table.get_item(Key={'id': -1})
    crawled_up_to = item.get('Item').get('epoch_time')
    
    time, items = get_tutti_json()
    
    if time is None:
        # error crawling trying again later
        return
    
    #update craled up to point
    table.update_item(
                Key={'id': -1},
                UpdateExpression='set epoch_time = :val',
                ExpressionAttributeValues={':val': time}
            )#ToDO change time to not update time use crawled_up_to
    
    #remove items already known
    items = get_new_items(items, crawled_up_to)
    
    #get all chats we need to search through
    item = table.get_item(Key={'id': 0})
    users = item.get('Item').get('chat_id')
    
    for user in users:
        keywords = table.get_item(Key={'id': user}).get('Item').get('keywords')
        
        for keyword in keywords:
            
            for item in items:
                #concatenate text for search
                item_text = item['subject'] +' '+ item['body']
                item_text = item_text.lower()
                
                if keyword in item_text:
                    print('notify user about item')
                    print(keyword)
                    send_message_item(item, user, URL)
    

        
        
if __name__ == "__main__":
    import os, boto3
    #generate Telegram API url
    TOKEN=os.environ['TELEGRAM_TOKEN']
    URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    
    #get table 
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('Tutti')

    print('for testing purposes')
    crawl_tutti(URL,table)