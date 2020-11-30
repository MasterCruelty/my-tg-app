from datetime import date
import time
import os
import re
import utils_config
import modules.wiki
import modules.gmaps
import modules.lyrics
import modules.atm_feature
import modules.covid
import utils.dbfunctions
import utils.sysfunctions

"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query):
    if match == "/wiki":
        return modules.wiki.execute_wiki(query)
    if match == "/map":
        return modules.gmaps.execute_map(query)
    if match == "/km":
        return modules.gmaps.execute_km(query)
    if match == "/route":
        return modules.gmaps.execute_route(query)
    if match == "/lyrics":
        return modules.lyrics.execute_lyrics(query)
    if match == "/atm":
        return modules.atm_feature.execute_atm_get_stop(query)
    if match == "/covid":
        return modules.covid.execute_covid()

def fetch_super_command(match,query,client,message):
    #db functions
    if match == "/setuser":
        return utils.dbfunctions.set_user(client,message,query)
    if match == "/deluser":
        return utils.dbfunctions.del_user(client,message,query)
    if match == "/listuser":
        return utils.dbfunctions.list_user(client,message)
    if match == "/alluser":
        return utils.dbfunctions.all_user(client,message)
    if match == "/setadmin":
        return utils.dbfunctions.set_admin(client,message,query)
    if match == "/deladmin":
        return utils.dbfunctions.del_admin(client,message,query)
    if match == "/listadmin":
        return utils.dbfunctions.list_admin(client,message)
    if match == "/alladmin":
        return utils.dbfunctions.all_admin(client,message)
    #system functions
    if match == "/hcount":
        return utils.sysfunctions.count_messages(client,message)
    if match == "/id":
        return utils.sysfunctions.id_chat(client,message)
    if match == "/getid":
        return utils.sysfunctions.get_id(client,message)
    if match == "/getuser":
        return utils.sysfunctions.get_user(client,message,query)
    if match == "/getmessage":
        return utils.sysfunctions.get_message(client,message)
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
    os.system("./ip_banned.sh")
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
