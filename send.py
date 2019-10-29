import os, json
from telegram import Bot,ForceReply,InputMediaPhoto

#generate Telegram API url
TOKEN=os.environ['TELEGRAM_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = Bot(TOKEN)

def send_photo(text,url, chat_id):
    print(url)
    bot.send_photo(chat_id=chat_id,photo=url,caption=text)
    
def send_message(text, chat_id):
    print('send arbitrary message')
    
    final_text = text 
    try:
        bot.send_message(chat_id=chat_id,text=final_text)
    except Exception as e:
        print(e)

def send_query_message(text, chat_id):
    print('send query message')
    
    final_text = text 
    bot.send_message(chat_id,final_text,reply_markup=ForceReply())

def send_reply_message(text, message_id, chat_id):
    print('send query message')
    
    final_text = text 
    #force_reply = '{force_reply:true,selective:true}'
    #url = URL + "sendMessage?text={}&chat_id={}&reply_to_message={}".format(final_text, chat_id,message_id)
    bot.send_message(chat_id,final_text,reply_to_message=message_id)


def send_message_item(item, chat_id):
    #item = json.loads(item)
    
    chat_id = int(chat_id)
    
    print('send item message')
    id_ = str(int(item['id']))
    url = 'https://www.tutti.ch/de/vi/'+id_+'/'
    
    subject = str(item['subject'])
    body = str(item['body'])
    price = str(item['price'])

    #map image names to urls
    image_names = item['image_names']
    image_names = ['https://c.tutti.ch/images/'+pic for pic in image_names]
    
    caption =  subject +'\n'+ body +'\n\nprice:'+price+'\n'+ url 
    
    #send caption always
    bot.send_message(chat_id,caption,disable_web_page_preview=True)
        
    if len(image_names)<=1:
        bot.send_photo(chat_id=chat_id,photo=image_names[0])
    else:
        pics = [InputMediaPhoto(image) for image in image_names[0:10]]
            
        bot.send_media_group(chat_id=chat_id,media = pics)
    
    
        
if __name__ == "__main__":
    import json
    chat_id =  -396501681
    with open('./test.json') as json_file:
        item = json.load((json_file))
    send_message_item(item, chat_id)
    