from pyrogram import Client
import utils.controller as uct
import utils.get_config as ugc
import utils.dbfunctions as udb
import random
import time
import os

"""
Ricerca ogni messaggio che matcha con la keyword richiesta nella chat in cui viene lanciato il comando
"""
@Client.on_message()
def search_msg(client,message,search):
    udb.stop_msg_false()
    endsearchmsg = False
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
    result = ""
    client.send_message(chat,"Cerco i messaggi...",reply_to_message_id=id_messaggio)
    count = 0
    for message in client.search_messages(chat, query = search):
        if not endsearchmsg and "/searchmsg" not in str(message):
            id_msg =  message.id
            if str(chat).startswith("-100"):
                try:
                    result += "<a href=\"https://t.me/c/"+str(chat).replace("-100","")+"/"+str(id_msg)+"\">"+ message.text[0:15]+"...</a>" + "\n"
                    count += 1
                    client.edit_message_text(chat,id_messaggio+1,"Cerco i messaggi...\n"+"Messaggi trovati: "+str(count))
                except:
                    continue
            else:
                client.send_message(chat,"Trovato",reply_to_message_id=id_msg)
                endsearchmsg = udb.isTrueStop()
                time.sleep(2)
    client.send_message(chat,"Trovati tutti i messaggi.\n"+ result,reply_to_message_id=id_messaggio)

"""
Lancia un sondaggio in automatico non anonimo
"""
@Client.on_message()
def poll_function(query,client,message):
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
    poll = query.split("/")
    domanda = poll[0]
    opzioni = poll[1]
    opzioni = opzioni.split(",")
    client.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)

"""
Preso come argomento un path intero, invia quel file su telegram(utile per backuppare file di configurazione o .db)
"""
@Client.on_message()
def send_file(client,message,path):
    chat = ugc.get_chat(message)
    try:
        client.send_document(chat,document = path,caption = "__Ecco il file richiesto__",reply_to_message_id=message.id)
    except:
        client.send_message(chat,"__Errore file non trovato.__",False,False,reply_to_message_id=message.id)

"""
Esegue un comando dalla shell della macchina su cui è hostato lo userbot e manda l'output del comando sulla stessa chat.
"""
@Client.on_message()
def exec_file(client,message,src):
    chat = ugc.get_chat(message)
    try:
        os.system(src + " > out.txt")
        out = open("out.txt",'r')
        client.send_message(chat,"__Eseguito come richiesto.__\n**output:**\n__" + out.read() + "__",reply_to_message_id=message.id)
    except Exception as ex:
        client.send_message(chat,"__Probabilmente l'output del comando è troppo lungo, ma il comando è stato eseguito.__\n" + str(ex),reply_to_message_id=message.id)
    out.close()

"""
Restituisce il numero di messaggi complessivo nella chat in cui viene lanciato il comando
"""
@Client.on_message()
def count_messages(client,message):
    chat = ugc.get_chat(message)
    totmsg = client.get_chat_history_count(chat)
    result = "Totale messaggi in questa chat: " + str(totmsg)
    return ugc.sendMessage(client,message,result)

"""
Restituisce sotto forma di messaggio Telegram l'id della chat corrente
"""
@Client.on_message()
def id_chat(client,message):
    chat_id = message.chat.id
    return ugc.sendMessage(client,message,chat_id)

"""
Restituisce l'id dell'utente a cui appartiene il messaggio risposto
"""
def get_id(client,message):
    content = message.reply_to_message.from_user
    result = content.id
    return ugc.sendMessage(client,message,result)

"""
Restituisce il json dell'utente richiesto(id utente come argomento)
"""
@Client.on_message()
def get_user(client,message,query):
    info_user = client.get_users(query)
    return ugc.sendMessage(client,message,info_user)

"""
Restituisce il json intero di un messaggio. Se il json supera la capacità di un messaggio Telegram, viene inviato sotto forma di file.
"""
@Client.on_message()
def get_message(client,message):
    check = uct.check_group(client,message)
    if(check):
        chat = ugc.get_chat(message)
        uct.save_json(message)
        client.send_document(chat,document = "json_message.json",caption = "__Ecco il json prodotto dal messaggio__",reply_to_message_id=message.id)

"""
Veloce controllo se l'app è online
"""
def ping(client,message):
    return ugc.sendMessage(client,message,"pong")

"""
documentazione dei comandi utente direttamente su Telegram
"""
#array per filtrare il comando help richiesto in help.json
help_array = ["wiki","lyrics","covid","poll","atm","mappe"]
def help(query,client,message):
    help_file = ugc.get_config_file("help.json")
    if query in help_array:
        help_request = help_file[query][0:]
        help_request = str(help_request).replace("(","").replace(")","").replace('"','').replace(r'\n','\n')
        return ugc.sendMessage(client,message,help_request)
    else:
        help_request = help_file["default"]
        return ugc.sendMessage(client,message,help_request)

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
    return ugc.sendMessage(client,message,result)
