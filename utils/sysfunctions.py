from pyrogram import Client
import utils.system

@Client.on_message()
def count_messages(client,message):
    chat = message["chat"]["id"]
    totmsg = client.get_history_count(chat)
    result = "Totale messaggi in questa chat: " + str(totmsg)
    client.send_message(chat,result,"html",reply_to_message_id=message["message_id"])
    return

@Client.on_message()
def id_chat(client,message):
    chat_id = message["chat"]["id"]
    client.send_message(chat_id,chat_id,"html",reply_to_message_id=message["message_id"])
    return

@Client.on_message()
def get_id(client,message):
    chat = message["chat"]["id"]
    content = message["reply_to_message"]["from_user"]
    result = content["id"]
    client.send_message(chat,result,"html",reply_to_message_id=message["message_id"])
    return

@Client.on_message()
def get_user(client,message,query):
    chat = message["chat"]["id"]
    info_user = client.get_users(query)
    client.send_message(chat,info_user,"html",reply_to_message_id=message["message_id"])
    return

@Client.on_message()
def get_message(client,message):
    chat = message["chat"]["id"]
    try:
        client.send_message(chat,message,"html",reply_to_message_id=message["message_id"])
    except:
        utils.system.save_json(message)
        client.send_document(chat,"json_message.json",None,None,"Ecco il json prodotto dal messaggio","html",reply_to_message_id=message["message_id"])
    return

def execute_get_message(client,message):
    return get_message(client,message)
