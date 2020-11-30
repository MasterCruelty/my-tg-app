import wikipedia
import re
from pyrogram import Client
import utils.get_config
#Questa funzione esegue il comando wiki richiesto dall'app principale fetchato tramite la funzione in system.py
@Client.on_message()
def execute_wiki(query,client,message):
    chat = message["chat"]["id"]
    id_messaggio = message["message_id"]
    parole = query.split(" ")
    lingua = parole[0]
    parole.remove(parole[0])
    word = ""
    for i in range(len(parole)):
        word += parole[i] + " "
    if " all " in query:
        parole.remove(parole[0])
        result = wikiall(lingua,word,client,message)
        return result 
    if "/comune" in query:
        try:
            comune(client,message)
            return
        except:
            client.edit_message_text(chat,id_messaggio+1,"Operazione fallita ")
            return
    if "random" in query:
        result = wikirandom(lingua,1,False,client,message)
        return result
    else:
        result = wiki(lingua,word,client,message)
        return result

#data la lingua e la parola chiave da cercare, restituisce una frase della voce trovata
def wiki(lang,keyword,client,message):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 1) 
   return utils.get_config.sendMessage(client,message,result)
#data la lingua e la parola chiave da cercare, restituisce il numero massimo di frasi(limite della libreria) della voce trovata
def wikiall(lang,keyword,client,message):
   wikipedia.set_lang(lang)
   if "random" in keyword:
       result = wikirandom(lang,10,client,message)
       return result
   result = wikipedia.summary(keyword,sentences = 10)
   result = result.replace("==","****")
   return utils.get_config.sendMessage(client,message,result)
#data la lingua restituisce una frase di una pagina wikipedia casuale
def wikirandom(lang,sents,boole,client,message):
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
            result = wikirandom("it",1,True,client,message)
        except:
            continue 
        if ("abitanti" in result and ("comune" in result or "città" in result or "centro abitato" in result)):
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
