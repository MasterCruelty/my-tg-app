**IT/ENG**

# Librerie/Libraries

**[IT]**

La libreria principale è *pyrogram* perchè ci permette di lavorare con le API di telegram molto facilmente.<br/>
Ho usato *utils-config* cosi che si possano mettere chiavi o altri argomenti statici in un file .json e poi importarle in seguito.<br/>
*requests* per tutte le funzionalità che hanno richiesto di fare get o post nel web.<br/>
*json* per giocare con gli oggetti json.<br/>
Ho usato il modulo *geopy* per giocare con le mappe e le coordinate dei luoghi. Anche *openrouteservice* è incluso in questo.<br/>
*os* è stato usato un paio di volte per eseguire qualche script da shell.<br/>
E infinte il modulo *wikipedia* per fetchare dati dalla famosa enciclopedia online.<br/>

**[ENG]**

The main library is *pyrogram*, which is the one that permits to work with Telegram API very easy.<br/>
I used *utils-config* to put keys and other static arguments stuffs in a file .json and then importing them.<br/>
*requests* for all features that required doing get or post through web.<br/>
*json* to play with json objects.<br/>
I used *geopy* module to play with maps and coordinates of places. *openrouteservice* was also included in this.<br/>
*os* was used a couple of times to execute some script from shell.<br/>
And then *wikipedia* module for fetching data from the famous web site.<br/>

# Come si usano le funzioni/How to use main functions

**[IT]**

```python
1. /wiki  : "/wiki <lingua> <parola chiave da cercare>" (modalità base)  
2. /poll  : "/poll <domanda>/<opzione 1>, <opzione 2>, <opzione N>"
3. /covid : è sufficiente scrivere /covid
4. /atm   : "/atm <codice fermata>
5. /map   : "/map <luogo>"
6. /km    : "/km <luogo 1>, <luogo 2>
7. /route : "/route <luogo 1>, <luogo 2>
8. /lyrics: "/lyrics <artista>, <canzone>"
```

**[ENG]**

```python
1. /wiki  : "/wiki <lang> <keyword to search>" (basic mode)
2. /poll  : "/poll <question>/<option 1>, <option 2>, <option N>"
3. /covid : just type /covid
4. /atm   : "/atm <stop code>
5. /map   : "/map <place>"
6. /km    : "/km <place 1>, <place 2>
7. /route : "/route <place 1>, <place 2>
8. /lyrics: "/lyrics <artist>, <song>
```
