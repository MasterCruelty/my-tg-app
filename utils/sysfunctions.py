from pyrogram import Client
import utils.utility
import utils.get_config
import utils.dbfunctions
import random
import time

"""
Ricerca ogni messaggio che matcha con la keyword richiesta nella chat in cui viene lanciato il comando
"""
@Client.on_message()
def search_msg(client,message,search):
    utils.dbfunctions.stop_msg_false()
    endsearchmsg = False
    chat = utils.get_config.get_chat(message)
    id_messaggio = utils.get_config.get_id_msg(message)
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
                endsearchmsg = utils.dbfunctions.isTrueStop()
                time.sleep(2)
    client.send_message(chat,"Trovati tutti i messaggi.\n"+ result,"html",False,False,id_messaggio)

"""
Lancia un sondaggio in automatico non anonimo
"""
@Client.on_message()
def poll_function(client,message,query):
    chat = utils.get_config.get_chat(message)
    id_messaggio = utils.get_config.get_id_msg(message)
    poll = query.split("/")
    domanda = poll[0]
    opzioni = poll[1]
    opzioni = opzioni.split(",")
    client.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
    return

"""
Restituisce il numero di messaggi complessivo nella chat in cui viene lanciato il comando
"""
@Client.on_message()
def count_messages(client,message):
    chat = utils.get_config.get_chat(message)
    totmsg = client.get_history_count(chat)
    result = "Totale messaggi in questa chat: " + str(totmsg)
    return utils.get_config.sendMessage(client,message,result)

"""
Restituisce sotto forma di messaggio Telegram l'id della chat corrente
"""
@Client.on_message()
def id_chat(client,message):
    chat_id = message["chat"]["id"]
    return utils.get_config.sendMessage(client,message,chat_id)

"""
Restituisce l'id dell'utente a cui appartiene il messaggio risposto
"""
def get_id(client,message):
    content = message["reply_to_message"]["from_user"]
    result = content["id"]
    return utils.get_config.sendMessage(client,message,result)

"""
Restituisce il json dell'utente richiesto(id utente come argomento)
"""
@Client.on_message()
def get_user(client,message,query):
    info_user = client.get_users(query)
    return utils.get_config.sendMessage(client,message,info_user)

"""
Restituisce il json intero di un messaggio. Se il json supera la capacità di un messaggio Telegram, viene inviato sotto forma di file.
"""
@Client.on_message()
def get_message(client,message):
    chat = utils.get_config.get_chat(message)
    try:
        client.send_message(chat,message,"html",reply_to_message_id=message["message_id"])
    except:
        utils.utility.save_json(message)
        client.send_document(chat,"json_message.json",None,None,"Ecco il json prodotto dal messaggio","html",reply_to_message_id=message["message_id"])
    return

"""
Veloce controllo se l'app è online
"""
def ping(client,message):
    return utils.get_config.sendMessage(client,message,"pong")

"""
Restituisce 6 numeri tutti diversi tra loro tutti nel range da 1 a 90
"""
@Client.on_message()
def play_lotto(client,message):
    numbers = []
    while len(numbers) < 6:
        n = random.randint(1,90)
        if n not in numbers:
            numbers.append(n)
    result = ' '.join(str(n) for n in numbers)
    return utils.get_config.sendMessage(client,message,result)
