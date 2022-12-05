from config import *
import stg


@bot.message_handler(commands=['start'])
def start_msg(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if Lang(chat_id).get() != "None":
            stg.start_msg(chat_id)
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
        cd = call.data.split("||")
        if call.data == "home":
            start_msg(call.message)
            dm()
        elif call.data == "wallet":
            stg.wallet(chat_id)
            dm()

        elif cd[0] == "set_lang":
            Lang(chat_id).set(cd[1].lower())
            start_msg(call.message)
            dm()




bot.polling()