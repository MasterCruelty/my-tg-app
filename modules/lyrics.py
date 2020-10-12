import urllib.request
from bs4 import BeautifulSoup

def get_lyrics_formated(artista,canzone):
    artista = artista.lower()
    artista = artista.replace(" ","")
    canzone = canzone.lower()
    canzone = canzone.replace(" ","")
    url = "https://azlyrics.com/lyrics/" + artista + "/" + canzone + ".html"
    page = urllib.request.urlopen(url)
    zuppa = BeautifulSoup(page,"html.parser")
    lyrics_tags = zuppa.find_all("div",attrs= {"class": None, "id": None})
    lyrics = [tag.getText() for tag in lyrics_tags]
    result = "\n".join(lyrics)
    return result


