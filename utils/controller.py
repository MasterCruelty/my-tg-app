from pyrogram import Client
import utils_config
import modules.wiki
import modules.gmaps
import modules.lyrics
import modules.atm_feature
import modules.covid
import utils.dbfunctions as udb
import utils.sysfunctions as usys
import utils.get_config as ugc


dictionary = {      '/wiki'       : modules.wiki.execute_wiki,
                    '/map'        : modules.gmaps.showmaps,
                    '/km'         : modules.gmaps.execute_km,
                    '/lyrics'     : modules.lyrics.execute_lyrics,
                    '/atm'        : modules.atm_feature.get_stop_info,
                    '/geoatm'     : modules.atm_feature.geodata_stop,
                    '/searchatm'  : modules.atm_feature.search_line,
                    '/covid'      : modules.covid.covid_cases,
                    '/poll'       : usys.poll_function,
                    '/help'       : usys.help}

dictionary_admin = {'/hcount'     : usys.count_messages,
                    '/route'      : modules.gmaps.execute_route,
                    '/id'         : usys.id_chat,
                    '/getid'      : usys.get_id,
                    '/getuser'    : usys.get_user,
                    '/getmessage' : usys.get_message,
                    '/playlotto'  : usys.play_lotto,
                    '/searchmsg'  : usys.search_msg,
                    '/stopmsg'    : udb.stop_msg_true,
                    '/ping'       : usys.ping}

dictionary_super = {'/setuser'    : udb.set_user,
                    '/deluser'    : udb.del_user,
                    '/listuser'   : udb.list_user,
                    '/alluser'    : udb.all_user,
                    '/setadmin'   : udb.set_admin,
                    '/deladmin'   : udb.del_admin,
                    '/send'       : usys.send_file,
                    '/exec'       : usys.exec_file}
"""
Questa funzione prende come argomento il match e la richiesta dal main e dirotta la richiesta sul file dedicato a quel comando
"""
def fetch_command(match,query,client,message):
    if match in dictionary and check_group(client,message):
        return dictionary[match](query,client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi degli utenti admin
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    try:
        return dictionary_admin[match](client,message,query)
    except:
        return dictionary_admin[match](client,message)

"""
Analogamente a fetch_command ma per i comandi esclusivi del super admin
"""
def fetch_super_command(match,query,client,message):
    #db functions and send_file
    try:
        return dictionary_super[match](client,message,query)
    except:
        return dictionary_super[match](client,message)

"""
controlla che robbot non sia nella stessa chat, altrimenti esegue il comando
"""
@Client.on_message()
def check_group(client,message):
    try:
        check = client.get_chat_member(utils.get_config.get_chat(message),133326326)
        return False
    except:
        return True

"""
funzione che aiuta a parsare i comandi nel sorgente principale senza sporcare troppo in giro
"""
def parser(message):
    temp = message.split(" ",1)
    try:
        result = temp[1]
    except:
        result = temp[0]
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
