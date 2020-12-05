from pyrogram import Client
import utils.utility
import utils.get_config
import random

@Client.on_message()
def search_msg(client,message,search):
    endsearchmsg = False
    result = ""
    client.send_message(chat,"Cerco i messaggi...","html",reply_to_message_id=id_messaggio)
    count = 0
    for message in client.search_messages(chat, query = search):
        if not endsearchmsg and "/searchmsg" not in str(message):
            id_msg =  message.message_id
            if str(chat).startswith("-100"):
                try:
                    result += "<a href=\"https://t.me/c/"+str(chat).replace("-100","")+"/"+str(id_msg)+"\">"+ message.text[0:15]+"...</a>" + "\n"
                    count += 1
                    client.edit_message_text(chat,id_messaggio+1,"Cerco i messaggi...\n"+"Messaggi trovati: "+str(count))
                except:
                    continue
            else:
                client.send_message(chat,"Trovato","html",reply_to_message_id=id_msg)
                time.sleep(2)
    client.send_message(chat,"Trovati tutti i messaggi.\n"+ result,"html",False,False,id_messaggio)

def stop_msg():
    #wip

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
