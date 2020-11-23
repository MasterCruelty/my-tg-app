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
from utils.manageusers import *


config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")
endsearchmsg = False
db.connect()

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
    def list_user():
        result = "Lista utenti saltati:\n\n"
        query = User.select()
        for user in query:
            result += str(user.id_user) + ";" + user.name + ";" + user.username + "\n"
        return result
    def all_user():
        result = 0
        query = User.select()
        for user in query:
            result += 1
        return "Totale utenti registrati: " + str(result)
    def set_user(json_user):
        userid = json_user["id"]
        nome_utente = json_user["first_name"]
        username_utente = "@" + json_user["username"]
        user = User(id_user = userid, name = nome_utente, username = username_utente)
        user.save()
        query = User.select().where(User.id_user == userid)
        for user in query:
            result = "Utente salvato:\n" + str(user.id_user) + "\n" + user.name + "\n" + user.username
        return result
    def del_user(json_user):
        userid = json_user["id"]
        query = User.delete().where(User.id_user == userid).execute()
        result = str(userid) + " eliminato."
    def isSuper(id_utente):
        check = SuperAdmin.select().where(SuperAdmin.id_user == id_utente)
        for superadmin in check:
            return True
        return False
    def isAdmin(id_utente):
        check = Admin.select().where(Admin.id_user == id_utente)
        for admin in check:
            return True
        return False
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
    if "/wiki" in messaggio:
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
    if "/poll" in messaggio:
        messaggio = parser(messaggio)
        poll = messaggio.split("/")
        domanda = poll[0]
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        app.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/covid") :
       result = covid_daily()
       app.send_message(chat,result,reply_to_message_id=id_messaggio)
       return
    if messaggio.startswith("/atm"):
        stop = parser(messaggio)
        result = get_stop_info(stop)
        app.send_message(chat,result,disable_web_page_preview=True,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/lyrics"):
        messaggio = parser(messaggio)
        parametri = messaggio.split(",")
        result = get_lyrics_formated(parametri[0],parametri[1])
        app.send_message(chat,result,reply_to_message_id=id_messaggio)
        return
    if messaggio.startswith("/map"):
        address = parser(messaggio)
        coordinates = showmaps(address)
        app.send_location(chat,coordinates[0],coordinates[1])
        return
    if messaggio.startswith("/km"):
        messaggio = parser(messaggio)
        addresses = messaggio.split(',')
        km = distanza(addresses[0],addresses[1])
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if messaggio.startswith("/route"):
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
