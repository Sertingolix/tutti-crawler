from send import send_message, send_message_item, send_query_message, send_reply_message

help = 'You can create a new alert by typing /new folwed by a keyword you want to be alerted for\n by typing /start all alerts are deleted and you can start over'

def handle_message(data, URL, table):
    print(data)
    message = str(data["message"]["text"])
    chat_id = data["message"]["chat"]["id"]
    message_id = data["message"]["message_id"]
    #first_name = data["message"]["chat"]["first_name"]
    
    if '/start' in message:
        handle_start(chat_id = chat_id, URL = URL, table = table)
        return
    if '/new' in message:
        handle_new(message=message, message_id = message_id, chat_id = chat_id, URL = URL, table = table)
        return
    if '/delete' in message:
        handle_delete(message=message, message_id = message_id, chat_id = chat_id, URL = URL, table = table)
        return
    if '/list' in message:
        handle_list(chat_id = chat_id, URL = URL, table = table)
        return
    
    #reply = 'sorry I did not quite get that' + help
    send_message('debug:\n'+message, chat_id,URL)
    
    
    return

def handle_new(message, message_id, chat_id, URL, table):
    #remove new_alert command
    message = message.split()
    print(message)
    
    #make sure keyword submitted
    if len(message)==1:
        send_reply_message('use \'/new keyword\' to submit a new keyword',message_id, chat_id,URL)
        return
    
    #everything but the command is the keyword
    keyword = ' '.join(message[1:])
    print(keyword)
    
    table.update_item(
                Key={'id': chat_id},
                UpdateExpression='add keywords :val',
                ExpressionAttributeValues={':val': {keyword}}
            )
            
    msg = 'You will get an alert as soon as new products for ' + keyword + ' are available'
    send_message(msg, chat_id,URL)        
    #send_query_message('For which keyword would you like to creat an alert?',message_id, chat_id,URL)

def handle_delete(message, message_id, chat_id, URL, table):
    #remove delete command
    message = message.split()
    print(message)
    
    #make sure keyword submitted
    if len(message)==1:
        send_reply_message('use \'/delete keyword\' to delete a keyword',message_id, chat_id,URL)
        return
    
    #everything but the command is the keyword
    keyword = ' '.join(message[1:])
    print(keyword)
    
    #delete keyword from users list
    table.update_item(
                Key={'id': chat_id},
                UpdateExpression='delete keywords :val',
                ExpressionAttributeValues={':val': {keyword}}
            )
def handle_list(chat_id, URL, table):
    keywords = table.get_item(Key={'id': chat_id}).get('Item').get('keywords')
    real_keawords = [keyword for keyword in keywords if 'placeholder-keyword' not in keyword]
    
    msg = 'your current keywords are: \n'+ ' '.join(real_keawords)
    send_message(msg, chat_id,URL)
    
def handle_start(chat_id, URL, table):
    #add user to known users
    table.update_item(
                Key={'id': 0},
                UpdateExpression='add chat_id :val',
                ExpressionAttributeValues={':val': {chat_id}}
            )
            
    # create user entry
    with table.batch_writer() as batch:
        row = {"id": chat_id,
                "keywords": {'placeholder-keyword'},
        }
        batch.put_item(Item=row)
        
    #send welcome message
    welcome_msg = 'Welcome to the Tutti alert Bot \n' + help
    send_message(welcome_msg, chat_id,URL)