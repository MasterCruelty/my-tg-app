from datetime import date
import time
import os
import re
import requests
import json

"""
funzione che tra le 16.40 e le 17.20 controlla se è stato effettuato un nuovo commit su salute.gov.it
"""
def check_covid():
    file_commit = open('files/commit_covid.txt','r')
    content = file_commit.read()
    file_commit.close()
    commit =  os.popen("git ls-remote https://github.com/pcm-dpc/COVID-19.git HEAD | awk '{ print $1}' > files/commit_covid.txt")
    file_commit = open('files/commit_covid.txt','r')
    content_new = file_commit.read()
    file_commit.close() 
    if content == content_new:
        return False
    else:
        return True
    
"""
    funzione che prende ogni giorno il json aggiornato contenente i dati dei contagiati in Italia.
    Direttamente da salute.gov.it
"""
def covid_daily():
    url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'
    resp = requests.get(url)
    data = json.loads(resp.text)
    for item in data:
        nuovi_positivi = str(item["nuovi_positivi"])
        ricoverati = str(item["ricoverati_con_sintomi"])
        terapia_intensiva = str(item["terapia_intensiva"])
        isolamento = str(item["isolamento_domiciliare"])
        deceduti = str(item["deceduti"])
        giorno = str(item["data"])[0:10]
    result = "I nuovi positivi in data " + giorno +" sono: " + nuovi_positivi + "\nAttualmente vi sono:\n" + ricoverati + " pazienti ricoverati con sintomi\n" + terapia_intensiva + " pazienti in terapia intensiva\n" + isolamento + " pazienti in isolamento domiciliare\n" + deceduti + " pazienti deceduti"
    return result
"""
	funzione per loggare i messaggi in arrivo da qualunque chat
"""
def logger(chat,nome_utente,username,utente,messaggio):
    if str(chat).startswith("-"):
        return
    data_messaggio = time.strftime("%d/%m/%Y")
    orario_messaggio = time.strftime("%H:%M:%S")
    path = 'Logger/Logger_' + data_messaggio.replace('/','_')
    try:
        file_logger = open(path,'r')
        file_logger.close()
        file_logger = open(path,'a')
        stringa = str(chat) + ";" + nome_utente + ";" + username + ";" + str(utente) + ";" + str(orario_messaggio) + ";" + messaggio + "\n\n"
        try:
            file_logger.write(stringa)
        except:
            file_logger.write(stringa.encode('utf-8'))
    except:
        print(">>>>Il file logger in data odierna non esiste<<<< ==> Scrivo la prima riga di default")
        file_logger = open(path,'w')
        file_logger.write('File di log data: ' + data_messaggio + '\n\nID CHAT||||NOME UTENTE||||USERNAME||||ID UTENTE||||ORA_MESSAGGIO||||MESSAGGIO\n\n')
        stringa = str(chat) + ";" + nome_utente + ";" +  username + ";" + str(utente) + ";" + str(orario_messaggio) + ";" + messaggio + "\n\n"
        try:
            file_logger.write(stringa)
        except:
            file_logger.write(stringa.encode('utf-8'))
        file_logger.close()
    print(">>>>Log messaggio salvato con successo<<<<")
    return

"""
	funzione per backuppare le chat di gruppo
"""
def backup_chat_gruppi(chat_id,nome_chat,utente,nome_utente,username,messaggio):
    nome_file = "database_chat_gruppi/database_chat_" + str(chat_id) + ".txt"
    save_chat = open(nome_file,'a')
    stringa = "ID CHAT: " + str(chat_id) + 'NOME CHAT: '+ nome_chat + ' | ID UTENTE: ' + str(utente) +' | NOME: '+ nome_utente+ ' | Nickname: '+ username  + '\nContenuto del messaggio: \n' + messaggio + '\n________________________________________________________________________________________________\n\n'
    try:
            save_chat.write(stringa)
    except:
            print ('>>>>Chat name is unicode type<<<< ==> Saved message from '+ str(chat_id))
            nome_file = "Files/database_chat_esterne/database_chat_" + str(chat_id) + ".txt"
            save_chat = open(nome_file,'a')
            save_chat.write(stringa.encode('utf-8'))
    save_chat.close()
    print ('>>>>Salvataggio messaggio chat_gruppo effettuato<<<<')

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
"""
	funzione che salva su file.json il json di un singolo messaggio in arrivo
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
