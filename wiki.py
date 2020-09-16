import wikipedia
import os

def wiki(lang,keyword):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 1) 
   return result

def wikiall(lang,keyword):
   wikipedia.set_lang(lang)
   result = wikipedia.summary(keyword,sentences = 10)
   result = result.replace("==","****")
   return result

def wikirandom(lang):
    wikipedia.set_lang(lang)
    random = wikipedia.random()
    result = wikipedia.summary(random,sentences=1)
    return result
