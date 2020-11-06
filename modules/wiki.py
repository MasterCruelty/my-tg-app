import wikipedia

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
