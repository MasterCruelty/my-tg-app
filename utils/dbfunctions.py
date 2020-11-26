import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *

#Inizio della connessione con il db
db.connect()

"""
questa funzione fa una select dalla tabella User e restituisce i dati di tutti gli utenti
"""

def list_user():
    result = "Lista utenti salvati:\n\n"
    query = User.select()
    for user in query:
        result += str(user.id_user) + ";" + user.name + ";" + user.username + "\n"
    return result

"""
questa funzione fa una select dalla tabella User e restituisce gli id di tutti gli utenti registratii in una lista di int
"""

def list_id():
    result = []
    query = User.select()
    query += Admin.select()
    for user in query:
        result.append(user.id_user)
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
    result = "Utente " + str(userid) + " eliminato."
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
questa funzione fa una select dalla tabella Admin e restituisce i dati di tutti gli admin
"""

def list_admin():
    result = "Lista admin salvati:\n\n"
    query = Admin.select()
    for admin in query:
        result += str(admin.id_user) + ";" + admin.name + ";" + admin.username + "\n"
    return result

"""
questa funzione è simile a list_admin ma restituisce solo il numero degli utenti registrati nella tabella Admin
"""

def all_admin():
    result = 0
    query = Admin.select()
    for admin in query:
        result += 1
    return "Totale admin registrati: " + str(result)

"""
questa funzione permette di registrare un nuovo admin nella tabella Admin
"""

def set_admin(json_user):
    userid = json_user["id"]
    nome_utente = json_user["first_name"]
    username_utente = "@" + str(json_user["username"])
    admin = Admin(id_user = userid, name = nome_utente, username = username_utente)
    try:
        admin.save()
    except:
        return "Admin già registrato"
    query = Admin.select().where(Admin.id_user == userid)
    for admin in query:
        result = "Admin " + str(user.id_user) + " salvato!"
    return result

"""
Questa funzione elimina un admin  dalla tabella Admin
"""

def del_admin(json_user):
    userid = json_user["id"]
    query = Admin.delete().where(User.id_user == userid).execute()
    result = "Admin " + str(userid) + " eliminato."
    return result

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
