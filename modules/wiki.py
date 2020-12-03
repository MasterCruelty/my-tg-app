import wikipedia
import re
from pyrogram import Client
import utils.get_config
import utils.utility
from bs4 import BeautifulSoup



#Restituisce il parametro lingua
def get_lang(query):
    parole = query.split(" ")
    lingua = parole[0]
    return lingua
#restituisce le parole chiavi della ricerca eliminando la lingua
def get_keyword(query):
    words = query.split(" ")
    words.remove(words[0])
    search = ""
    for i in range(len(words)):
        search += words[i] + " "
    return search

#Questa funzione esegue il comando wiki richiesto dall'app principale fetchato tramite la funzione in system.py
@Client.on_message()
def execute_wiki(query,client,message):
    if "/comune" in query:
        try:
            return comune(client,message)
        except:
            chat = message["chat"]["id"]
            id_messaggio = message["message_id"]
            client.edit_message_text(chat,id_messaggio+1,"Operazione fallita ")
            return
    lingua = get_lang(query)
    if len(lingua) > 3 or lingua == "all":
        return exec_wiki_ita(query,client,message)
    word = get_keyword(query)
    if " all " in query:
        return wikiall(word,client,message,lingua)
    if "random" in query:
        return wikirandom(1,False,client,message,lingua)
    else:
        return wiki(word,client,message,lingua)

def exec_wiki_ita(query,client,message):
    if "all" in query:
        query = utils.utility.parser(query)
        return wikiall(query,client,message)
    if "random" in query:
        return wikirandom(1,False,client,message)
    else:
        return wiki(query,client,message)


#data la lingua e la parola chiave da cercare, restituisce una frase della voce trovata
def wiki(keyword,client,message,lang="it"):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 1) 
   return utils.get_config.sendMessage(client,message,result)
#data la lingua e la parola chiave da cercare, restituisce il numero massimo di frasi(limite della libreria) della voce trovata
def wikiall(keyword,client,message,lang="it"):
   wikipedia.set_lang(lang)
   if "random" in keyword:
       result = wikirandom(10,client,message,lang)
       return result
   result = wikipedia.summary(keyword,sentences = 10)
   result = result.replace("==","****")
   return utils.get_config.sendMessage(client,message,result)
#data la lingua restituisce una frase di una pagina wikipedia casuale
def wikirandom(sents,boole,client,message,lang="it"):
    wikipedia.set_lang(lang)
    wikipedia.set_rate_limiting(rate_limit = True)
    random = wikipedia.random()
    result = wikipedia.summary(random,sentences=sents)
    if boole:
        return result
    else:
        return utils.get_config.sendMessage(client,message,result)
#Simpatica funzione che cerca un comune su Wikipedia e ne restituisce i dati evidenziando numero abitanti e numero pagine visitate per trovarlo.
@Client.on_message()
def comune(client,message):
    chat = message["chat"]["id"]
    id_messaggio = message["message_id"]
    count = 0
    client.send_message(chat,"Cerco un comune...","html",reply_to_message_id=id_messaggio)
    while(True):
        count += 1
        client.edit_message_text(chat,id_messaggio+1,"Cerco un comune...\nVoci consultate: " + str(count))
        try:
            result = wikirandom(1,True,client,message)
        except:
            continue 
        if ("abitanti" in result and ("comune" in result or "città" in result or "centro abitato" in result or "è una frazione" in result)):
            page = result.split(" ")
            for i in range(len(page)):
                if page[i] == "abitanti":
                    abitanti = page[i-1]
                    if page[i-2].isdigit():
                        abitanti = page[i-2] + page[i-1]
            break
    result = result + "\n\n" + "Abitanti: " + abitanti + "\n\nVoci consultate: " + str(count)
    client.edit_message_text(chat,id_messaggio+1,result)
    return
