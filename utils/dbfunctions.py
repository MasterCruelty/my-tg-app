import sys
sys.path.append(sys.path[0] + "/..")
from utils.manageusers import *

#Inizio della connessione con il db
db.connect()

"""
questa funzione fa una select dalla tabella User e restituisce i dati di tutti gli utenti
"""

def list_user():
    result = "Lista utenti saltati:\n\n"
    query = User.select()
    for user in query:
        result += str(user.id_user) + ";" + user.name + ";" + user.username + "\n"
    return result

"""
questa funzione è simile a list_user ma restituisce solo il numero degli utenti registrati nella tabella User
"""

def all_user():
    result = 0
    query = User.select()
    for user in query:
        result += 1
    return "Totale utenti registrati: " + str(result)

"""
questa funzione permette di registrare un nuovo utente nella tabella User
"""

def set_user(json_user):
    userid = json_user["id"]
    nome_utente = json_user["first_name"]
    username_utente = "@" + str(json_user["username"])
    user = User(id_user = userid, name = nome_utente, username = username_utente)
    try:
        user.save()
    except:
        return "Utente già registrato"
    query = User.select().where(User.id_user == userid)
    for user in query:
        result = "Utente " + str(user.id_user) + " salvato!"
    return result

"""
Questa funzione elimina un utente dalla tabella User
"""

def del_user(json_user):
    userid = json_user["id"]
    query = User.delete().where(User.id_user == userid).execute()
    result = str(userid) + " eliminato."
    return result

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella User
"""

def isUser(id_utente):
    if isSuper(id_utente) or isAdmin(id_utente):
        return True
    else:
        check = User.select().where(User.id_user == id_utente)
        for user in check:
            return True
        return False

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella Admin
"""

def isAdmin(id_utente):
    if isSuper(id_utente):
        return True
    else:
        check = Admin.select().where(Admin.id_user == id_utente)
        for admin in check:
            return True
        return False

"""
Questa funzione controlla se un certo utente Telegram è SuperAdmin
"""

def isSuper(id_utente):
    check = SuperAdmin.select().where(SuperAdmin.id_user == id_utente)
    for superadmin in check:
        return True
    return False

#chiusura della connessione con il db
db.close()
