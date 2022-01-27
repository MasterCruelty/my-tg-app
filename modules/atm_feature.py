import requests
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from pyrogram import Client

config = get_config_file("config.json")
api_url = config["api_url"]
api_get = config["api_get"]
headers = { "Origin": "https://giromilano.atm.it/",
            "Referer": "https://giromilano.atm.it/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
          }

"""
Restituisce l'elenco delle fermate dato l'indirizzo richiesto con i codici fermata corrispondenti
"""
def search_line(line_number,client,message):
    stops = search_stop(line_number)
    result = str(len(stops)) + " risultati:\n<i>digita /atm 'codice' per sapere i dettagli di una fermata in particolare.</i>\n\n"
    for item in stops:
        if item["Lines"] == []:
            result += "**" + item["Description"] + "(" + item["Municipality"] + ")**" + " | codice: " + "<code>" + item["CustomerCode"] + "</code>\n\n"
        result += "__**Linea " + item["Lines"][0]["Line"]["LineCode"]  + " " + item["Lines"][0]["Line"]["LineDescription"]+"__**\n"
        result += "**" + item["Description"] + "(" + item["Municipality"] + ")**" + " | codice: " + "<code>" + item["CustomerCode"] + "</code>\n\n"
    return sendMessage(client,message,result)


"""
    Dato un codice fermata, vengono fornite le informazioni relative a quella fermata contattando direttamente il server atm
    Dedicato ai dati delle fermate di mezzi di superficie/metro. Riporta dati parziali su altri tipi di richieste.
"""
def get_stop_info(stop_code,client,message):
    resp = get_json_atm(stop_code)
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
dato un codice fermata, fornisce le coordinate geografiche di quella fermata.
Funziona con qualsiasi tipo di oggetto, dalla fermata del bus al parchimetro.
"""
@Client.on_message()
def geodata_stop(stop_code,client,message):
    resp = get_json_atm(stop_code)
    data_json = handle_except(resp)
    if str(data_json).startswith("404"):
        return sendMessage(client,message,data_json)
    coords = data_json["Location"]
    latitud = coords["Y"]
    longitud= coords["X"]
    client.send_location(get_chat(message),latitud,longitud,reply_to_message_id=get_id_msg(message))
    return

"""
Fa la richiesta al server atm e restituisce il json corrispondente.
"""
def get_json_atm(stop_code):
    data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data,headers = headers)
    return resp

"""
cerca qualsiasi fermata esistente a partire da un indirizzo
"""
def search_stop(query):
    data = {"url": "tpPortal/tpl/stops/search/" + query + "".format()}
    stops = []
    for stop in (requests.post(api_url,data = data,headers = headers)).json():
        stops.append(stop)
    return stops


"""
Controlla se un campo estratto del json è nullo per evitare eccezioni sul concatenamento di stringhe.
"""
def check_none(field):
    if field is None:
        return "Non disponibile"
    else:
        return field
"""
cattura eventuali eccezioni sulle richieste.
"""
def handle_except(resp):
    try:
        data_json = resp.json()
    except:
        result = "404: page not found"
        return result
    return data_json

