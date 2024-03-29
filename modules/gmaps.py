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
not_found = "__Error 404: not found__"


"""
    query => le due località su cui calcolare la distanza con la virgola come separatore.
    client, message => dati per comunicare con pyrogram in sendMessage.
    Funzione che formatta l'input, esegue la funzione per calcolare la distanza tra i due luoghi e restituisce il risultato tramite messaggio.
"""
def execute_km(query,client,message):
    addresses = query.split(',')
    try:
        km = distanza(addresses[0],addresses[1])
    except IndexError:
        return sendMessage(client,message,"__Errore: distanza non calcolabile.__")
    if(km == "None"):
        result = not_found
    else:
        result = "La distanza tra i due luoghi è di " + str(km) + " km."
    try:
        return sendMessage(client,message,result)
    except AttributeError:
        return km

def execute_route(client,message,query):
    #uso il carattere '/' come separatore per recuperare modalità di trasporto e dopo uso ',' per recuperare i due luoghi
    try:
        first_split = query.split('/')
        mode = first_split[0]
        addresses = first_split[1].split(',')
    except:
        return sendMessage(client,message,"__Errore formato__\nprova /help mappe.__")
    route = directions(client,message,addresses[0],addresses[1],mode)
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
    check = False
    if "-i" in address:
        check = True
        address = address.replace("-i","")
    geolocate = Nominatim(user_agent="my-tg-app")
    location  = geolocate.geocode(address,timeout=10000)
    if location == None:
        try:
            return sendMessage(client,message,not_found)
        except AttributeError:
            print("errore generico")
    coordinates = []
    caption = "__**" + location.address + "\n\nTipologia luogo: " + location.raw["type"] + "\n\nImportanza: " + str(round(location.raw["importance"],2)) + "**__"
    caption += "\n\n__Importanza è un valore compreso tra 0 e 1 circa, calcolato in base al rank del luogo negli articoli di Wikipedia.__\n"
    url = "https://www.openstreetmap.org/#map=16/{}/{}".format(location.latitude, location.longitude)
    caption += "<a href=" + url + ">Guarda su OpenStreetMap</a>"
    if check == True:
        return sendMessage(client,message,caption)
    try:
        coordinates.append(location.latitude)
        coordinates.append(location.longitude)
    except AttributeError:
        return sendMessage(client,message,"__Error 404: not found__")
    try:
        client.send_location(get_chat(message),coordinates[0],coordinates[1],reply_to_message_id=get_id_msg(message))
        return sendMessage(client,message,caption)
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
def directions(client,message,address1,address2,query):
    coord1 = showmaps(address1,client = None,message = None)
    coord2 = showmaps(address2,client = None,message = None)
    coord1 = coord1[::-1]
    coord2 = coord2[::-1]
    coords = ((coord1[0],coord1[1]),(coord2[0],coord2[1]))
    client_geopy = openrouteservice.Client(key = api_geopy)
    #dizionario con le tre modalità di trasporto supportate dalla funzione
    modes = { 'macchina': 'driving-car', 'piedi': 'foot-walking', 'bicicletta':'cycling-road'}
    if query in modes:
        profile = modes[query]
    try:
        travel = client_geopy.directions(coords,profile=profile,format='json',preference = 'fastest',units='km',language="it")
    except:
        return "__Destinazione troppo lontana__"
    client_geopy = openrouteservice.Client(key = api_geopy)
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
            tragitto = "Tra " + str(tragitto) + " metri "
        else:
            tragitto = round(item["distance"],2)
            tragitto = "Tra " + str(tragitto) + " km "
        if "Arrivo" in item["instruction"]:
            istruzioni += item["instruction"] + "\n"
        else:
            istruzioni += tragitto + item["instruction"] + "\n"
    tts = gTTS(istruzioni,lang="it")
    tts.save("istruzioni.mp3")
    client.send_document(get_chat(message),document = "istruzioni.mp3",caption = "Istruzioni per raggiungere la destinazione con: " + query, reply_to_message_id=get_id_msg(message))
    result = "La tua destinazione si trova a " + str(distanza) + " km raggiungibile in circa "  + str(time_travel)
    return result
