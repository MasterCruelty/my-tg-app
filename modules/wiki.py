import wikipedia
import re
from pyrogram import Client
import utils.get_config as ugc
import utils.controller as uct
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

#genero il link alla pagina wikipedia della pagina richiesta per saperne di più
def create_link(keyword,lang):
    wikipedia.set_lang(lang)
    page = wikipedia.page(keyword)
    link = "<a href="+page.url+">Guarda su Wikipedia</a>"
    return link

#Questa funzione esegue il comando wiki richiesto dall'app principale fetchato tramite la funzione in system.py
@Client.on_message()
def execute_wiki(query,client,message):
    if "/comune" in query:
        try:
            return comune(client,message)
        except:
            client.edit_message_text(ugc.get_chat(message),message.id+1,"Operazione fallita")
            return


#data la lingua restituisce una frase di una pagina wikipedia casuale
def wikirandom(sents,boole,client,message,lang="it"):
    wikipedia.set_lang(lang)
    wikipedia.set_rate_limiting(rate_limit = True)
    random = wikipedia.random()
    result = wikipedia.summary(random,sentences=sents)
    if boole:
        return result
    else:
        result += "\n"+create_link(random,lang)
        return ugc.sendMessage(client,message,result)
#Simpatica funzione che cerca un comune su Wikipedia e ne restituisce i dati evidenziando numero abitanti e numero pagine visitate per trovarlo.
#Il numero di abitanti viene recuperato direttamente dalla pagina html tramite l'uso della zuppa
@Client.on_message()
def comune(client,message):
    chat = ugc.get_chat(message)
    id_messaggio = ugc.get_id_msg(message)
    count = 0
    client.send_message(chat,"Cerco un comune...",reply_to_message_id=id_messaggio)
    wikipedia.set_lang("it")
    while(True):
        count += 1
        #Stampo solo per numeri pari dimezzando il numero di modifiche al messaggio.
        #Meno carico sulle richieste api di Telegram.
        if count % 2 == 0:
            client.edit_message_text(chat,id_messaggio+1,"Cerco un comune...\nVoci consultate: " + str(count))
        try:
            random = wikipedia.random()
            result = wikipedia.summary(random,1)
        except:
            continue 
        if (("è un comune" in result or "è una curazia" in result or "città" in result or "centro abitato" in result or "è una frazione" in result)):
            page = wikipedia.page(random)
            title = page.title
            page_source = page.html()
            zuppa = BeautifulSoup(page_source,"html.parser")
            table = zuppa.find('table',attrs={"class": 'sinottico'})
            text = table.get_text()
            text = text.split("\n")
            for i in range(len(text)):
                if text[i].startswith("Abitanti"):
                    abitanti = text[i]
                    break
            temp = abitanti.split("(")
            abitanti = temp[0]
            abitanti = abitanti.replace("Abitanti","")
            abitanti = abitanti.split("[")
            abitanti = abitanti[0]
            break
    result = "**" + title + "**" + "\n" + result + "\n\n" + "**" + "Abitanti:** " + "**" + abitanti + "**" + "\n\n__Voci consultate:__ " + str(count)
    title = title.replace(" ","_")
    link = "<a href="+page.url+">Guarda su Wikipedia</a>"
    client.edit_message_text(chat,id_messaggio+1,result + "\n" + link,disable_web_page_preview=True)
    return
