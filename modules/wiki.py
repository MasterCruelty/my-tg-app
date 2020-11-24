import wikipedia
import re
from pyrogram import Client
import sys
sys.path.append(sys.path[0] + "/..")
from utils.system import get_config_file

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
app = Client("my_account", api_id, api_hash,no_updates = True)
app.start()
def execute_wiki(chat,id_messaggio,query):
    parole = query.split(" ")
    lingua = parole[0]
    parole.remove(parole[0])
    word = ""
    for i in range(len(parole)):
        word += parole[i] + " "
    if " all " in query:
        parole.remove(parole[0])
        result = wikiall(lingua,word)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    if "/comune" in query:
        app.send_message(chat,"cerco un comune...","html",False,False,id_messaggio)
        try:
            result = comune()
        except:
            result = "operazione fallita"
        app.edit_message_text(chat,id_messaggio+1,result,"html",False,False)
        return
    if "random" in query:
        result = wikirandom(lingua,1)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return
    else:
        result = wiki(lingua,word)
        app.send_message(chat,result,"html",False,False,id_messaggio)
        return

#data la lingua e la parola chiave da cercare, restituisce una frase della voce trovata
def wiki(lang,keyword):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 1) 
   return result
#data la lingua e la parola chiave da cercare, restituisce il numero massimo di frasi(limite della libreria) della voce trovata
def wikiall(lang,keyword):
   wikipedia.set_lang(lang)
   if "random" in keyword:
       result = wikirandom(lang,10)
       return result
   result = wikipedia.summary(keyword,sentences = 10)
   result = result.replace("==","****")
   return result
#data la lingua restituisce una frase di una pagina wikipedia casuale
def wikirandom(lang,sents):
    wikipedia.set_lang(lang)
    random = wikipedia.random()
    result = wikipedia.summary(random,sentences=sents)
    return result
def comune():
    i = 0
    while(True):
        i += 1
        try:
            result = wikirandom("it",1)
        except:
            continue 
        if ("abitanti" in result and "comune" in result):
            page = result.split(" ")
            for i in range(len(page)):
                if page[i] == "abitanti":
                    abitanti = page[i-1]
                    if page[i-2].isdigit():
                        abitanti = page[i-2] + page[i-1]
            break
    return result + "\n\n" + "Abitanti: " + abitanti + "\n\nVoci consultate: " + str(i)
