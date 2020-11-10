from datetime import date
import time
import os
import re

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
    nome_file = "json_messages.json"
    save = open(nome_file,'a')
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
