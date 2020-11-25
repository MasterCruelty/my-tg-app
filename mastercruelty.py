import time
from datetime import date
from datetimerange import DateTimeRange
from pyrogram import Client 
from utils.system import *
from utils.dbfunctions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
comandi = config["lista_comandi"]
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")
endsearchmsg = False

@app.on_message()
def print_updates(client,message):
    #print(message)
    #save_json(message) scommentare quando serve un json non a portata di mano
    chat = message["chat"]["id"]
    nome_chat = message["chat"]["title"]
    utente = message["from_user"]["id"]
    nome_utente = message["from_user"]["first_name"]
    id_messaggio = message["message_id"]
    time_message = time.strftime("%H:%M:%S")
    file_id = "Nullo"
    global endsearchmsg #this is useful to stop the search of messages
    
    if message["from_user"]["username"] is None:
        username = "Non impostato"
    else:
        username = "@" + message["from_user"]["username"]
    
    if message["text"] is None:
        messaggio = "file multimediale"
    else:
        messaggio = message["text"]

    #rappresentazione grafica del messaggio corrente sul terminale
    visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)

    #funzioni dedicate al database 
    if messaggio.startswith("/setuser") and isSuper(utente):
        utente_new = parser(messaggio)
        info_utente = app.get_users(utente_new)
        result = set_user(info_utente)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/deluser") and isSuper(utente):
        user = parser(messaggio)
        info_utente = app.get_users(user)
        result = del_user(info_utente)
        app.send_message(chat,result,"html",False,False,id_messaggio)
    if messaggio.startswith("/listuser") and isSuper(utente):
        result = list_user()
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/alluser") and isSuper(utente):
        result = all_user()
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return

       
    #alcune funzioni di sistema
    if messaggio.startswith("/hcount") and (isAdmin(utente) or isSuper(utente)):
        result = "Totale messaggi in questa chat: " + str(app.get_history_count(chat))
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/id") and (isAdmin(utente) or isSuper(utente)):
        result = app.get_chat(chat)
        result = result["id"]
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/getid") and (isAdmin(utente) or isSuper(utente)):
        content = message["reply_to_message"]["from_user"]
        result = content["id"]
        app.send_message(chat,result,"html",False,False,id_messaggio)
    if messaggio.startswith("/getuser") and (isAdmin(utente) or isSuper(utente)):
        search = parser(messaggio)
        result = app.get_users(search)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if "/getmessage" in str(message) and (isAdmin(utente) or isSuper(utente)):
        try:
            app.send_message(chat,message,"html",False,False,id_messaggio)
        except:
            save_json(message)
            app.send_document(chat,"json_message.json",None,None,"Ecco il json prodotto dal messaggio","html",None,False,False,id_messaggio)
        return
    if messaggio.startswith("/searchmsg") and (isAdmin(utente) or isSuper(utente)):
        search = parser(messaggio)
        for message in app.search_messages(chat, query = search):
            if not endsearchmsg and "/searchmsg" not in str(message):
                result = message.message_id
                app.send_message(chat,"Trovato","html",False,False,result)
                time.sleep(2)
        app.send_message(chat,"Trovati tutti i messaggi.","html",False,False,id_messaggio)
        endsearchmsg = False
        return
    if messaggio.startswith("/stopmsg") and (isAdmin(utente) or isSuper(utente)):
        endsearchmsg = True
        return
    if "/poll" in messaggio and isUser(utente):
        messaggio = parser(messaggio)
        poll = messaggio.split("/")
        domanda = poll[0]
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        app.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
        return

     
    #funzionalità per gli utenti
    lista_comandi = comandi.split(";")
    match = messaggio.split(" ")
    if match[0] in lista_comandi and isUser(utente):
        try:
            query = parser(messaggio)
        except:
            query = messaggio
        if query == "/comune":
            app.send_message(chat,"Cerco un comune...",reply_to_message_id=id_messaggio)
            result = fetch_command(match[0],query)
            app.edit_message_text(chat,id_messaggio+1,result)
        else:
            result = fetch_command(match[0],query)
            if type(result) == list:
                app.send_location(chat,result[0],result[1],reply_to_message_id = id_messaggio)
            else:
                app.send_message(chat,result,disable_web_page_preview=True,reply_to_message_id=id_messaggio)

app.run()
