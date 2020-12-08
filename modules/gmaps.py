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


config = get_config_file("config.json")
api_geopy = config["api_geopy"]



def execute_km(query,client,message):
    addresses = query.split(',')
    km = distanza(addresses[0],addresses[1])
    result = "La distanza tra i due luoghi è di " + str(km) + " km."
    return sendMessage(client,message,result)

def execute_route(query,client,message):
    addresses = query.split(',')
    route = directions(addresses[0],addresses[1])
    result = route
    return sendMessage(client,message,result)

@Client.on_message()
def showmaps(address,client,message):
    geolocate = Nominatim(user_agent="map_app")
    location  = geolocate.geocode(address,timeout=10000)
    coordinates = []
    coordinates.append(location.latitude)
    coordinates.append(location.longitude)
    try:
        client.send_location(get_chat(message),coordinates[0],coordinates[1],reply_to_message_id=get_id_msg(message))
    except:
        return coordinates

def distanza(address1,address2):
    coord1 = showmaps(address1,client = None,message = None)
    coord2 = showmaps(address2,client = None,message = None)
    departure = (coord1[0],coord1[1])
    arrive = (coord2[0],coord2[1])
    result = geodesic(departure,arrive).miles
    result = (result * 1.609344)
    return round(result,2)


def directions(address1,address2):
    coord1 = showmaps(address1,client = None,message = None)
    coord2 = showmaps(address2,client = None,message = None)
    coord1 = coord1[::-1]
    coord2 = coord2[::-1]
    coords = ((coord1[0],coord1[1]),(coord2[0],coord2[1]))
    client = openrouteservice.Client(key = api_geopy)
    travel = client.directions(coords,profile='driving-car',format='json',preference = 'fastest',units='km',language="it")
    dis_time = travel['routes'][0]['summary']
    distanza = dis_time['distance']
    distanza = round(distanza,2)
    time_travel = float(dis_time['duration']) / 60
    time_travel = round(time_travel,2)
    if(time_travel > 60):
        time_travel = str(round(time_travel / 60,2)) + " ore."
    else:
        time_travel = str(time_travel) + " minuti."
    steps = travel['routes'][0]
    steps = steps['segments'][0]
    steps = steps["steps"]
    istruzioni = ""
    for item in steps:
        if float(item["distance"]) < 1:
            tragitto = float(item["distance"]) * 1000
            tragitto = int(tragitto)
            tragitto = str(tragitto) + " metri"
        else:
            tragitto = round(item["distance"],2)
            tragitto = str(tragitto) + " km"
        if "Arrivo" in item["instruction"]:
            istruzioni += item["instruction"] + "\n"
        else:
            istruzioni += item["instruction"] + " per " + tragitto + "\n"
    result = "La tua destinazione si trova a " + str(distanza) + " km raggiungibile in circa "  + str(time_travel)  + "\n\n" + istruzioni
    return result
