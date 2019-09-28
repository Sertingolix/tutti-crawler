from botocore.vendored import requests


def send_message(text, chat_id, URL):
    print('send arbitrary message')
    
    final_text = text 
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    print(url)
    requests.get(url)

def send_query_message(text, message_id, chat_id, URL):
    print('send query message')
    
    final_text = text 
    force_reply = '{force_reply:true,selective:true}'
    url = URL + "sendMessage?text={}&chat_id={}&reply_to_message={}&reply_markup={}".format(final_text, chat_id,message_id,force_reply)
    
    print(requests.get(url))

def send_reply_message(text, message_id, chat_id, URL):
    print('send query message')
    
    final_text = text 
    force_reply = '{force_reply:true,selective:true}'
    url = URL + "sendMessage?text={}&chat_id={}&reply_to_message={}".format(final_text, chat_id,message_id)
    
    print(requests.get(url))

def rem_uml(text):
    #remove umlaute
    return text.lower().replace('ö','oe').replace('ü','ue').replace('ä','ae')
    
def send_message_item(item, chat_id, URL):
    print('send item message')
    id_ = str(int(item['id']))
    url = 'https://www.tutti.ch/de/vi/'+id_+'/'
    final_text = url 
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    print(url)
    requests.get(url)