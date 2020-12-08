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
        if wait_time[i] is None:
            wait_time[i] = "Non disponibile"
        result += line_code[i] + " " + line_description[i] + ": " + "**" + wait_time[i] + "**" + "\n"
    for i in range(len(line_code)):
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
cattura eventuali eccezioni sulle richieste
"""
def handle_except(resp):
    try:
        data_json = resp.json()
    except:
        result = "404: page not found"
        return result
    return data_json

