import time
from datetime import date
from datetimerange import DateTimeRange
from pyrogram import Client #, MessageHandler   de-commentare se si torna a pyrogram 0.18
from modules.covid import *
from modules.wiki import *
from modules.gmaps import *
from modules.atm_feature import *
from modules.lyrics import *
from utils.system import *
from utils.dbfunctions import *


config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")
endsearchmsg = False

@app.on_message()
def print_updates(client,message):
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
        return
    if messaggio.startswith("/listuser") and isSuper(utente):
        result = list_user()
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/alluser") and isSuper(utente):
        result = all_user()
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/setadmin") and isSuper(utente):
        admin_new = parser(messaggio)
        info_admin = app.get_users(admin_new)
        result = set_admin(info_admin)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/deladmin") and isSuper(utente):
        admin = parser(messaggio)
        info_admin = app.get_users(admin)
        result = del_admin(info_admin)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/listadmin") and (isAdmin(utente) or isSuper(utente)):
        result = list_admin()
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/alladmin") and (isAdmin(utente) or isSuper(utente)):
        result = all_admin()
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


    #funzionalità per gli utenti
    if "/wiki" in messaggio and isUser(utente):
        search = parser(messaggio)
        parole = search.split(" ")
        lingua = parole[0]
        parole.remove(parole[0])
        word = ""
        for i in range(len(parole)):
            word += parole[i] + " "
        if " all " in messaggio:
            parole.remove(parole[0])
            result = wikiall(lingua,word)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
        if "/comune" in messaggio:
            app.send_message(chat,"cerco un comune...","html",False,False,id_messaggio)
            try:
                result = comune()
            except:
                result = "operazione fallita"
            app.edit_message_text(chat,id_messaggio+1,result,"html",False,False)
            return
        if "random" in messaggio:
            result = wikirandom(lingua,1)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
        else:
            result = wiki(lingua,word)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
    if "/poll" in messaggio and isUser(utente):
        messaggio = parser(messaggio)
        poll = messaggio.split("/")
        domanda = poll[0]
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        app.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/covid") and isUser(utente):
       result = covid_daily()
       app.send_message(chat,result,reply_to_message_id=id_messaggio)
       return
    if messaggio.startswith("/atm") and isUser(utente):
        stop = parser(messaggio)
        result = get_stop_info(stop)
        app.send_message(chat,result,disable_web_page_preview=True,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/lyrics") and isUser(utente):
        messaggio = parser(messaggio)
        parametri = messaggio.split(",")
        result = get_lyrics_formated(parametri[0],parametri[1])
        app.send_message(chat,result,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/map") and isUser(utente):
        address = parser(messaggio)
        coordinates = showmaps(address)
        app.send_location(chat,coordinates[0],coordinates[1])
        return
    if messaggio.startswith("/km") and isUser(utente):
        messaggio = parser(messaggio)
        addresses = messaggio.split(',')
        km = distanza(addresses[0],addresses[1])
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/route") and isUser(utente):
        messaggio = parser(messaggio)
        addresses = messaggio.split(',')
        route = directions(addresses[0],addresses[1])
        result = route
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return

#linee per pyrogram 0.18 (in caso di scalo di versione)
#my_handler = MessageHandler(print_updates)
#app.add_handler(my_handler)

app.run()
