import wikipedia
import re

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
