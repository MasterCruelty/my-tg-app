import urllib.request
from bs4 import BeautifulSoup

def get_lyrics_formated(artista,canzone):
    artista = format_input(artista)
    canzone = format_input(canzone)
    url = "https://azlyrics.com/lyrics/" + artista + "/" + canzone + ".html"
    page = handle_except(url) 
    if "404" in str(page):
        return page
    """try:
        page = urllib.request.urlopen(url)
    except:
        result = "404: page not found"
        return result"""
    zuppa = BeautifulSoup(page,"html.parser")
    lyrics_tags = zuppa.find_all("div",attrs= {"class": None, "id": None})
    lyrics = [tag.getText() for tag in lyrics_tags]
    result = "\n".join(lyrics)
    return result

def format_input(string):
    string = string.lower()
    string = string.replace(" ","")
    return string

def handle_except(url):
    try:
        page = urllib.request.urlopen(url)
    except:
        result = "404: page not found"
        return result
    return page

