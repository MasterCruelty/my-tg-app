import requests
import json
import utils.get_config

"""
    url => url github da cui recuperare il json

    Funzione di supporto per restituire il json sui contagi da covid19
"""
def covid_format_json(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    return data

"""
    number => numero da formattare

    Funzione di supporto per formattare i numeri con i separatori per le migliaia.
"""
def format_values(number):
    formated = '{:,}'.format(int(number))
    formated = str(formated).replace(",",".")
    return formated

"""
    repo => json ricavato dalla get al repo github 
    se True il json è vuoto e quindi il problema è esterno al bot, altrimenti è tutto ok.
"""
def check_repo(repo):
    if(repo == []):
        return True
    else:
        return False
"""
    client,message => parametri necessari per poter usare sendMessage del modulo 'get_config'
    query => regione richiesta, di default è l'Italia intera.

    Restituisce i dati principali sui contagi da covid19.
"""
def covid_cases(client,message,query):
    regioni = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json')
    italia  = covid_format_json('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json')
    trovata = False
    if(check_repo(regioni) or check_repo(italia)):
        return utils.get_config.sendMessage(client,message,"__Errore repository sorgente__")
    for item in regioni:
        if(query.title()[0:5] in item["denominazione_regione"]):
            regione = item["denominazione_regione"]
            nuovi_positivi = str(item["nuovi_positivi"])
            var_positivi = str(item["variazione_totale_positivi"])
            ricoverati = str(item["ricoverati_con_sintomi"])
            terapia_intensiva = str(item["terapia_intensiva"])
            ingressi_ti = str(item["ingressi_terapia_intensiva"])
            isolamento = str(item["isolamento_domiciliare"])
            deceduti = str(item["deceduti"])
            giorno = str(item["data"])[0:10]
            trovata = True
            break
        elif(query == "/covid"):
            for item in italia:
                regione = "Italia"
                nuovi_positivi = str(item["nuovi_positivi"])
                var_positivi = str(item["variazione_totale_positivi"])
                ricoverati = str(item["ricoverati_con_sintomi"])
                terapia_intensiva = str(item["terapia_intensiva"])
                ingressi_ti = str(item["ingressi_terapia_intensiva"])
                isolamento = str(item["isolamento_domiciliare"])
                deceduti = str(item["deceduti"])
                giorno = str(item["data"])[0:10]
                trovata = True
            break
    if(trovata):
        result = "I nuovi positivi in data **" + giorno +"** in __**" + regione + "**__  sono: **" + format_values(nuovi_positivi) + "**\nAttualmente vi sono:\n\n __pazienti ricoverati con sintomi:__ **" +format_values(ricoverati) +"**\n __pazienti in terapia intensiva:__ **" + format_values(terapia_intensiva) + "**\n __pazienti in isolamento domiciliare:__ **" + format_values(isolamento) + "**\n __pazienti deceduti:__ **" + format_values(deceduti) + "**\n\n" + "__ingressi t.i. :__ **" + format_values(ingressi_ti) + "**\n__variazione positivi:__ **" + format_values(var_positivi) + "**"
        return utils.get_config.sendMessage(client,message,result)
    else:
        return utils.get_config.sendMessage(client,message,"__Regione non trovata__")
