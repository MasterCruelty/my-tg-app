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
    chat = message["chat"]["id"]
    client.send_message(chat,result,"html",disable_web_page_preview=True,reply_to_message_id=message["message_id"])
    return
