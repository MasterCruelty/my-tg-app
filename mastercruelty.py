from pyrogram import Client #, MessageHandler   de-commentare se si torna a pyrogram 0.18
from modules.system import *
from modules.wiki import *
from modules.gmaps import *
from modules.atm_feature import *
from modules.lyrics import *
import time
from datetime import date
from datetimerange import DateTimeRange
import utils_config

#prendo api_id e api_hash da file di configurazione .json esterno al sorgente
config_file = "config.json"
config = utils_config.load_config(config_file)
utils_config.serialize_config(config)
api_id = config.api_id
api_hash = config.api_hash
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")

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
    if message["from_user"]["username"] is None:
        username = "Non impostato"
    else:
        username = "@" + message["from_user"]["username"]
    if message["text"] is None:
        file_id = recuperaFileID(message) 
        messaggio = "file multimediale con file_id: " + file_id 
    else:
        messaggio = message["text"]
    visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)
    #logger(chat,nome_utente,username,utente,messaggio) funzione usata in passato per salvare su txt i messaggi consecutivamente
    if "/wiki" in messaggio:
        search = messaggio[6:]
        parole = search.split(" ")
        lingua = parole[0]
        parole.remove(parole[0])
        word = ""
        for i in range(len(parole)):
            word += parole[i] + " "  
        if "all" in messaggio:
            parole.remove(parole[0])
            result = wikiall(lingua,word)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
        if "random" in messaggio:
            result = wikirandom(lingua)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
        else:
            result = wiki(lingua,word)
            app.send_message(chat,result,"html",False,False,id_messaggio)
            return
    if "/poll" in messaggio:
        messaggio = messaggio.replace("/poll","")
        poll = messaggio.split("/")
        domanda = poll[0]
        opzioni = poll[1]
        opzioni = opzioni.split(",")
        app.send_poll(chat,domanda,opzioni,is_anonymous=False,reply_to_message_id=id_messaggio)
    if messaggio.startswith("/covid") :
       result = covid_daily()
       app.send_message(chat,result,reply_to_message_id=id_messaggio)
    if messaggio.startswith("/atm"):
        stop = messaggio[5:]
        result = get_stop_info(stop)
        app.send_message(chat,result,disable_web_page_preview=True,reply_to_message_id=id_messaggio)
    if messaggio.startswith("/lyrics"):
        messaggio = messaggio[8:]
        parametri = messaggio.split(",")
        result = get_lyrics_formated(parametri[0],parametri[1]) 
        app.send_message(chat,result,reply_to_message_id=id_messaggio)
    if messaggio.startswith("/map"):
        address = messaggio[5:]
        coordinates = showmaps(address)
        app.send_location(chat,coordinates[0],coordinates[1])
    if messaggio.startswith("/km"):
        messaggio = messaggio[4:]
        addresses = messaggio.split(',')
        km = distanza(addresses[0],addresses[1])
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
        app.send_message(chat,result,"html",False,False,id_messaggio)
    if messaggio.startswith("/route"):
        messaggio = messaggio[7:]
        addresses = messaggio.split(',')
        route = directions(addresses[0],addresses[1])
        result = route
        app.send_message(chat,result,"html",False,False,id_messaggio)

#linee per pyrogram 0.18 (in caso di scalo di versione)
#my_handler = MessageHandler(print_updates)
#app.add_handler(my_handler)

app.run()

