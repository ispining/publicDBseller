from config import *

def lang_set(chat_id):
    k = kmarkup()
    msg = "Select a language:"
    k.row(btn("English", callback_data=f"set_lang||en"))
    k.row(btn("Русский", callback_data=f"set_lang||ru"))
    send(chat_id, msg, reply_markup=k)
