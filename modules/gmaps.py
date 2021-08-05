from geopy.geocoders import Nominatim
from geopy.distance  import geodesic
import openrouteservice
from openrouteservice import convert
from pyrogram import Client
import time
import json
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import *
from gtts import gTTS


config = get_config_file("config.json")
api_geopy = config["api_geopy"]



"""
    query => le due località su cui calcolare la distanza con la virgola come separatore.
    client, message => dati per comunicare con pyrogram in sendMessage.
    Funzione che formatta l'input, esegue la funzione per calcolare la distanza tra i due luoghi e restituisce il risultato tramite messaggio.
"""
def execute_km(query,client,message):
    addresses = query.split(',')
    km = distanza(addresses[0],addresses[1])
    if(km == "None"):
        result = "__Error 404: not found__"
    else:
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
    return sendMessage(client,message,result)

def execute_route(query,client,message):
    addresses = query.split(',')
    route = directions(client,message,addresses[0],addresses[1])
    result = route
    return sendMessage(client,message,result)

"""
    address => indirizzo di cui si vuole sapere la localizzazione.
    client, message => dati per comunicare con pyrogram in send_location.
    Funzione che dato un indirizzo restituisce tramite messaggio la posizione geografica tramite le API dirette di Telegram.
    Viene usata anche come funzione ausiliaria in 'distanza', in quel caso restituisce solo l'array con le due coppie di coordinate.
"""
@Client.on_message()
def showmaps(address,client,message):
    geolocate = Nominatim(user_agent="my-tg-app")
    location  = geolocate.geocode(address,timeout=10000)
    coordinates = []
    try:
        coordinates.append(location.latitude)
        coordinates.append(location.longitude)
    except:
        return sendMessage(client,message,"__Error 404: not found__")
    try:
        client.send_location(get_chat(message),coordinates[0],coordinates[1],reply_to_message_id=get_id_msg(message))
    except:
        return coordinates

"""
    address1 => il primo luogo.
    address2 => il secondo luogo.
    Data una coppia di coordinate geografiche, viene calcolata la distanza in linea d'aria dei due luoghi in km.
"""
def distanza(address1,address2):
    try:
        coord1 = showmaps(address1,client = None,message = None)
        coord2 = showmaps(address2,client = None,message = None)
    except:
        return "None"
    departure = (coord1[0],coord1[1])
    arrive = (coord2[0],coord2[1])
    result = geodesic(departure,arrive).miles
    result = (result * 1.609344)
    return round(result,2)

@Client.on_message()
def directions(client,message,address1,address2):
    coord1 = showmaps(address1,client = None,message = None)
    coord2 = showmaps(address2,client = None,message = None)
    coord1 = coord1[::-1]
    coord2 = coord2[::-1]
    coords = ((coord1[0],coord1[1]),(coord2[0],coord2[1]))
    client_geopy = openrouteservice.Client(key = api_geopy)
    travel = client_geopy.directions(coords,profile='driving-car',format='json',preference = 'fastest',units='km',language="it")
    dis_time = travel['routes'][0]['summary']
    distanza = dis_time['distance']
    distanza = round(distanza,2)
    time_travel = round((float(dis_time['duration']) / 60),2)
    if(time_travel > 60):
        time_travel = str(round(time_travel / 60,2)) + " ore."
    else:
        time_travel = str(time_travel) + " minuti."
    steps = travel['routes'][0]['segments'][0]["steps"]
    istruzioni = ""
    for item in steps:
        if float(item["distance"]) < 1:
            tragitto = int((float(item["distance"]) * 1000))
            tragitto = str(tragitto) + " metri"
        else:
            tragitto = round(item["distance"],2)
            tragitto = str(tragitto) + " km"
        if "Arrivo" in item["instruction"]:
            istruzioni += item["instruction"] + "\n"
        else:
            istruzioni += item["instruction"] + " per " + tragitto + "\n"
    tts = gTTS(istruzioni,lang="it")
    tts.save("istruzioni.mp3")
    client.send_document(get_chat(message),document = "istruzioni.mp3",caption = "Istruzioni per raggiungere la destinazione", reply_to_message_id=get_id_msg(message))
    result = "La tua destinazione si trova a " + str(distanza) + " km raggiungibile in circa "  + str(time_travel)
    return result
