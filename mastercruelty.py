import time
from datetime import date
from datetimerange import DateTimeRange
from pyrogram import Client 
from utils.utility import *
from utils.dbfunctions import *
from utils.get_config import get_config_file,get_username,get_text_message,get_chat,get_id_msg,get_id_user
from utils.sysfunctions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
comandi = config["lista_comandi"]
comandi_admin = config["lista_comandi_admin"]
comandi_super = config["lista_comandi_super"] 
app = Client("my_account", api_id, api_hash)
time_range = DateTimeRange("16:40:00","17:20:00")

@app.on_message()
def print_updates(client,message):
    #recupero parametri principali del messaggio dal json
    chat = get_chat(message)
    id_messaggio = get_id_msg(message)
    utente = get_id_user(message)
    nome_chat = message["chat"]["title"]
    nome_utente = message["from_user"]["first_name"]
    time_message = time.strftime("%H:%M:%S")
    file_id = "Nullo"
    username = get_username(message) 
    messaggio = get_text_message(message)

    #rappresentazione grafica del messaggio corrente sul terminale
    visualizza(chat,nome_chat,utente,nome_utente,username,messaggio)

    #Restituisce il json del messaggio
    if "/getmessage" in str(message) and (isAdmin(utente) or isSuper(utente)):
        return get_message(client,message)

    #funzionalità super admin
    cmd_super = comandi_super.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_super and isSuper(utente):
        query = parser(messaggio)
        fetch_super_command(match[0],query,client,message)
        return

    #funzionalità admin
    cmd_admin = comandi_admin.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_admin and isAdmin(utente):
        query = parser(messaggio)
        fetch_admin_command(match[0],query,client,message)
        return

    #funzionalità per gli utenti
    lista_comandi = comandi.split(";")
    match = messaggio.split(" ")
    if match[0] in lista_comandi and isUser(utente):
        query = parser(messaggio)
        fetch_command(match[0],query,client,message)
        return

app.run()
