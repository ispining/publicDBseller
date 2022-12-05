from config import *
import stg


@bot.message_handler(commands=['start'])
def start_msg(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        k = kmarkup()



@bot.message_handler(content_types=['text'])
def text_msgs(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        pass



@bot.callback_query_handler(func=lambda m: True)
def g_cals(call):
    chat_id = call.message.chat.id
    if call.message.chat.type == "private":
        pass




bot.polling()