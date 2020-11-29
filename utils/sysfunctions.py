from pyrogram import Client

@Client.on_message()
def count_messages(client,message):
    chat = message["chat"]["id"]
    totmsg = client.get_history_count(chat)
    result = "Totale messaggi in questa chat: " + str(totmsg)
    client.send_message(chat,result,"html",reply_to_message_id=message["message_id"])
    return

def execute_count_messages(client,message):
    return count_messages(client,message)
