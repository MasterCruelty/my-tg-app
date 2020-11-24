from datetime import date
import time
import os
import re
import utils_config
#import sys
#sys.path.append(sys.path[0] + "/..")
import modules.wiki

"""
Funzione che preleva i dati dal file di configurazione json
"""
def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(chat,message_id,match,query):
    if match == "/wiki":
        modules.wiki.execute_wiki(chat,message_id,query)
    if match == "/map":
        modules.gmaps.execute_map(chat,message_id,query)
    if match == "/km":
        modules.gmaps.execute_km(chat,message_id,query)
    if match == "/route":
        modules.gmaps.execute_route(chat,message_id,query)
    if match == "/lyrics":
        modules.lyrics.execute_lyrics(chat,message_id,query)
    if match == "/atm":
        modules.atm_feature.execute_atm(chat,message_id,query)
    if match == "/covid":
        modules.covid.execute_covid(chat,message_id,query)

"""
funzione che aiuta a parsare i comandi nel sorgente principale senza sporcare troppo in giro
"""
def parser(message):
    temp = message.split(" ",1)
    result = temp[1]
    return result

"""
	funzione che salva su file il json del messaggio Telegram in arrivo
"""
def save_json(message):
    nome_file = "json_message.json"
    save = open(nome_file,'w')
    save.write(str(message))
    save.close()
"""
	funzione che esegue uno script shell per recuperare gli ip bannati sul raspberry pi
"""
def showIpBanned():
    #os.popen ("sudo zgrep 'Ban ' /var/log/fail2ban.log* > ip_banned.txt")
    os.popen("sudo fail2ban-client status sshd | grep -A 15 Actions > ip_banned.txt")
    file_banned = open("ip_banned.txt",'r')
    lista_banned = file_banned.read()
    return lista_banned

"""
	funzione per visualizzare a schermo i dati principali del messaggio in arrivo
"""
def visualizza(chat,nome_chat,utente,nome_utente,username,messaggio):
    print("id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username)
    try:
        print("chat_id: " + str(chat) + "\nnome_chat: " + nome_chat) 
    except:
        print("messaggio ricevuto da un channel o chat privata")
    print("\n\nMessaggio: " + messaggio + "\n" )
    print("**************************************************************************************")
    if str(chat):
        return "nome_chat: " + str(chat) +"id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username + "\n\n" + "Messaggio: " + messaggio 
"""
    da rifattorizzare: funzione per recuperare il file id del messaggio corrente
    plus: per rendere la funzione utile si dovrebbe gestire anche il parametro file_ref
"""
def recuperaFileID(message):
    try:
        try:
            file_id = message["photo"]["file_id"]
        except:
            try:
                file_id = message["animation"]["file_id"]
            except:
                try:
                    file_id = message["video_note"]["file_id"]
                except:
                    file_id = message["video"]["file_id"]
    except:
        print("formato multimediale non supportato da questa app")
        file_id = "Non supportato"
    print(">>>>file_id recuperato correttamente<<<< => " + file_id)
    return file_id        
