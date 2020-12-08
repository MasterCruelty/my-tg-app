import utils_config
from pyrogram import Client

"""
carica il file di configurazione
"""
def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)

"""
funzione d'appoggio per inviare messaggi 
"""
@Client.on_message()
def sendMessage(client,message,result):
    client.send_message(get_chat(message),result,disable_web_page_preview=True,reply_to_message_id=get_id_msg(message))
    return

def get_id_user(message):
    try:
        result = message["from_user"]["id"]
        return result
    except:
        return "id utente non disponibile"
"""
Restituisce l'id della chat
"""
def get_chat(message):
    return message["chat"]["id"]

"""
Restituisce username dell'utente
"""
def get_username(message):
    if message["from_user"]["username"] is None:
        return "Non impostato"
    else:
        return "@" + message["from_user"]["username"]

"""
Restituisce il campo testo del messaggio
"""
def get_text_message(message):
    if message["text"] is None:
        return "File multimediale"
    else:
        return message["text"]
"""
Restituisce l'id del messaggio
"""
def get_id_msg(message):
    return message["message_id"]
