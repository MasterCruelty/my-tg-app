from pyrogram import Client
import utils.utility
import utils.get_config
import random

@Client.on_message()
def count_messages(client,message):
    chat = message["chat"]["id"]
    totmsg = client.get_history_count(chat)
    result = "Totale messaggi in questa chat: " + str(totmsg)
    return utils.get_config.sendMessage(client,message,result)

@Client.on_message()
def id_chat(client,message):
    chat_id = message["chat"]["id"]
    return utils.get_config.sendMessage(client,message,chat_id)

def get_id(client,message):
    content = message["reply_to_message"]["from_user"]
    result = content["id"]
    return utils.get_config.sendMessage(client,message,result)

@Client.on_message()
def get_user(client,message,query):
    info_user = client.get_users(query)
    return utils.get_config.sendMessage(client,message,info_user)

@Client.on_message()
def get_message(client,message):
    chat = message["chat"]["id"]
    try:
        client.send_message(chat,message,"html",reply_to_message_id=message["message_id"])
    except:
        utils.utility.save_json(message)
        client.send_document(chat,"json_message.json",None,None,"Ecco il json prodotto dal messaggio","html",reply_to_message_id=message["message_id"])
    return

@Client.on_message()
def play_lotto(client,message):
    numbers = []
    while len(numbers) < 6:
        n = random.randint(1,90)
        if n not in numbers:
            numbers.append(n)
    result = ' '.join(str(n) for n in numbers)
    return utils.get_config.sendMessage(client,message,result)
