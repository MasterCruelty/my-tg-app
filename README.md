![License](https://img.shields.io/github/license/MasterCruelty/my-tg-app)
[![image](https://img.shields.io/github/stars/MasterCruelty/my-tg-app)](https://github.com/MasterCruelty/my-tg-app/stargazers)
[![image](https://img.shields.io/github/forks/MasterCruelty/my-tg-app)](https://github.com/MasterCruelty/my-tg-app/network/members)
![CodeSize](https://img.shields.io/github/languages/code-size/MasterCruelty/my-tg-app)
[![image](https://img.shields.io/github/issues/MasterCruelty/my-tg-app)](https://github.com/MasterCruelty/my-tg-app/issues)
![image](https://img.shields.io/github/languages/top/MasterCruelty/my-tg-app)
![image](https://img.shields.io/github/commit-activity/w/MasterCruelty/my-tg-app)
![image](https://img.shields.io/github/contributors/MasterCruelty/my-tg-app)

# my-tg-app

**IT/ENG**


# **[IT]**

# Come impostare

Per un corretto funzionamento è necessario compilare a dovere il file ```config.json```. Quindi è necessario essere in possesso dei seguenti dati:

* Api keys di Telegram: ```api_id``` e ```api_hash```.
* Bot token: ```bot_token```.
* Api url atm se si vogliono usare le loro api: ```api_url``` e ```api_get```.
* I dati telegram dell'amministratore del bot: ```id_super_admin```.
* Il percorso dove si trova il file .db: ```path_db```.
* Nome della sessione: ```session_name```.
* I nomi dei comandi utente, admin e superadmin: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

I dati del super admin servono a colui che potrà usare le funzioni di interazione con il database e altre funzioni particolari.
I nomi dei comandi da inserire nel ```config.json``` possono essere ricopiati dal codice oppure possono essere modificati sul codice e poi ricopiati nel file json.	

### Come funzionano i comandi utente dello userbot

Il funzionamento dei comandi è spiegato all'interno del file ```help.json```. Si tratta del file che viene usato dallo userbot per rispondere al comando ```/help <nome comando>```.
Le spiegazioni sono in Italiano, ma volendo si possono tradurre in qualsiasi lingua sostituendo i campi della struttura dati oppure addirittura renderlo multilingua, ma in quel caso c'è da sviluppare la componente che rende possibile il cambio di lingua.

### Come funzionano i comandi admin e super

* registrare un nuovo utente: ```/setuser``` <id_utente>
* registrare un nuovo admin: ```/setadmin``` <id_utente> 
* cancellare un utente: ```/deluser``` <id_utente>
* revocare i privilegi admin: ```/deladmin``` <id_utente> (l'utente sarà comunque ancora tra i registrati ma senza i poteri admin)
* mostrare tutti gli utenti registrati: ```/listuser```
* mostrare il numero di utenti registrati: ```/alluser```
* verificare se il bot è online: ```/ping```


### Dipendenze

* Pyrogram
* geopy
* bs4
* wikipedia


# **[ENG]**

# How to setup

The correct way to setup this bot is to compile the file  ```config.json```. So it's necessary to have these data:

* Telegram api keys: ```api_id``` e ```api_hash```.
* Telegram bot token: ```bot_token```.
* Atm api url if you wanna use their api: ```api_url``` e ```api_get```.
* Telegram data of the owner of the bot: ```id_super_admin```.
* The path where is the .db file: ```path_db```.
* The session name: ```session_name```.
* Name of user commands, admin commands and super admin commands: ```user_commands```, ```admin_commands``` e ```super_admin_commands```.

Data of super admin is needed because he's the only one who can use db functions and other special functions.
Name of commands to put inside ```config.json``` can be copied from source code or renamed inside source code and then copied in json file.	

### How the userbot's commands works

The features of the commands are explained inside ```help.json```. It is the file which is used by the userbot to reply at ```/help <command name>```.
This json file is only in Italian, but you can translate it in every languages by changing the correct fields with your translations or even making the userbot multi-language but in that case you have to develop the component for change the language runtime.

### How the admin/super commands works

* register a new user: ```/setuser``` <id_user>
* register a new admin: ```/setadmin``` <id_user> 
* delete a user: ```/deluser``` <id_user>
* delete an admin: ```/deladmin``` <id_user> (it will just revoke the admin power, it doesn't delete the user)
* How to list all user registered: ```/listuser``` 
* How to show ho many users are registered: ```/alluser```
* check if the bot is online: ```/ping```



### Dependencies

* Pyrogram
* geopy
* bs4
* wikipedia
