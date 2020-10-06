import utils_config
import requests
import json

config_file = "config.json"
config = utils_config.load_config(config_file)
utils_config.serialize_config(config)

api_url = config.api_url

"""
    Dato un codice fermata, vengono fornite le informazioni relative a quella fermata contattando direttamente il server atm
"""
def get_stop_info(stop_code):
    data = {"url": "tpPortal/geodata/pois/stops/" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data)
    data_json = resp.json()
    descrizione = data_json["Description"]
    Lines = data_json["Lines"]
    for item in Lines:
        Line = item["Line"]
        line_code = Line["LineCode"]
        line_code = Line["LineCode"]
        line_description = Line["LineDescription"]
        wait_time = item["WaitMessage"]
        time_table = item["BookletUrl"]

    result = "**" + descrizione + "**" + "\n" + line_code + " " + line_description + ": " + "**" + wait_time + "**" + "\n\n" + "Puoi consultare gli orari su:" + time_table
    return result

"""
dato un codice fermata, fornisce le coordinate geografiche di quella fermata
WIP
"""
def geodata_stop(stop_code):
    data = {"url": "tpPortal/geodata/pois/stops" + stop_code + "?lang=it".format()}
    resp = requests.post(api_url,data = data)
    data_json = json.loads(resp.text)
    return


