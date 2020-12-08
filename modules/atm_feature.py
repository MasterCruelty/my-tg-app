import requests
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from pyrogram import Client

config = get_config_file("config.json")
api_url = config["api_url"]

"""
    Dato un codice fermata, vengono fornite le informazioni relative a quella fermata contattando direttamente il server atm
    Dedicato ai dati delle fermate di mezzi di superficie/metro. Riporta dati parziali su altri tipi di richieste.
"""
def get_stop_info(stop_code,client,message):
    data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    descrizione = data_json["Description"]
    Lines = data_json["Lines"]
    line_code, line_description, wait_time, time_table = ([] for i in range(4))
    for item in Lines:
        Line = item["Line"]
        line_code.append(Line["LineCode"])
        line_description.append(Line["LineDescription"])
        wait_time.append(item["WaitMessage"])
        time_table.append(item["BookletUrl"])

    result = "**" + descrizione + "**" + "\n"
    for i in range(len(line_code)):
        wait_time[i] = check_none(wait_time[i])
        result += line_code[i] + " " + line_description[i] + ": " + "**" + wait_time[i] + "**" + "\n"
    result += "\n"
    for i in range(len(line_code)):
        time_table[i] = check_none(time_table[i])
        result += "Orari linea " + line_code[i] + ": " + time_table[i] + "\n"
    return sendMessage(client,message,result)

"""
dato un codice fermata, fornisce le coordinate geografiche di quella fermata
"""
@Client.on_message()
def geodata_stop(stop_code,client,message):
    data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    coords = data_json["Location"]
    latitud = coords["Y"]
    longitud= coords["X"]
    client.send_location(get_chat(message),latitud,longitud,reply_to_message_id=get_id_msg(message))
    return

"""
Controlla se un campo estratto del json è nullo per evitare eccezioni sul concatenamento di stringhe
"""
def check_none(field):
    if field is None:
        return "Non disponibile"
    else:
        return field
"""
cattura eventuali eccezioni sulle richieste
"""
def handle_except(resp):
    try:
        data_json = resp.json()
    except:
        result = "404: page not found"
        return result
    return data_json

