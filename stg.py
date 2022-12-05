from config import *

def lang_set(chat_id):
    k = kmarkup()
    msg = "Select a language:"
    k.row(btn("English", callback_data=f"set_lang||en"))
    k.row(btn("Русский", callback_data=f"set_lang||ru"))
    send(chat_id, msg, reply_markup=k)

def start_msg(chat_id):
    k = kmarkup()
    msg = Texts(chat_id).get_text("start_msg")
    k.row(btn(Texts(chat_id).get_text("wallet_btn"), callback_data="wallet"))
    send(chat_id, msg, reply_markup=k)

def wallet(chat_id):
    k = kmarkup()
    msg = Texts(chat_id).get_text("wallet").format(**{"bal": str(database.balance(chat_id))})
    k.row(btn(Texts(chat_id).get_text("update_wallet_btn"), callback_data="update_wallet"))
    k.row(back(chat_id, "home"))
    send(chat_id, msg, reply_markup=k)

