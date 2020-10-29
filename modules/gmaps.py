from geopy.geocoders import Nominatim
from geopy.distance  import geodesic
import openrouteservice
from openrouteservice import convert
import time
import json
import utils_config

config_file = "config.json"
config = utils_config.load_config(config_file)
utils_config.serialize_config(config)

api_geopy = config.api_geopy

def showmaps(address):
    geolocate = Nominatim(user_agent="map_app")
    location  = geolocate.geocode(address,timeout=10000)
    coordinates = []
    coordinates.append(location.latitude)
    coordinates.append(location.longitude)
    return coordinates

def distanza(address1,address2):
    coord1 = showmaps(address1)
    coord2 = showmaps(address2)
    departure = (coord1[0],coord1[1])
    arrive = (coord2[0],coord2[1])
    result = geodesic(departure,arrive).miles
    result = (result * 1.609344)
    return round(result,2)


def directions(address1,address2):
    coord1 = showmaps(address1)
    coord2 = showmaps(address2)
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
