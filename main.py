from config import *
import stg


@bot.message_handler(commands=['start'])
def start_msg(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if Lang(chat_id).get() != "None":
            k = kmarkup()
            msg = Texts(chat_id).get_text("start_msg")
            k.row(btn(Texts(chat_id).get_text(""), callback_data=""))
            send(chat_id, msg, reply_markup=k)
        else:
            stg.lang_set(chat_id)





@bot.message_handler(content_types=['text'])
def text_msgs(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        pass



@bot.callback_query_handler(func=lambda m: True)
def g_cals(call):
    chat_id = call.message.chat.id

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    if call.message.chat.type == "private":
        if call.data == "home":
            start_msg(call.message)
            dm()





bot.polling()