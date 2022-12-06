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
        stage = database.stages(chat_id)
        cd = stage.split('||')
        if stage == "update_wallet":
            k = kmarkup()
            msg = Texts(chat_id).get_text("send_link")
            k.row(back(chat_id, f"update_wallet||{message.text}"))
            send(chat_id, msg, reply_markup=k)
            database.stages(chat_id, f"send_link||{message.text}")
        elif cd[0] == "send_link":
            count = cd[1]
            link = message.text

            ak = kmarkup()
            amsg = Texts(chat_id).get_text("admins_template").format(**{
                "user_id": str(chat_id),
                "count": str(count),
                "link": str(link)
            })
            ak.row(btn("Allow", callback_data=f"allow_wallet||{str(chat_id)}||{str(count)}"),
                   btn("Deni", callback_data=f"deni_wallet||{str(chat_id)}"))
            send(admin_g, amsg, reply_markup=ak)

            k = kmarkup()
            msg = Texts(chat_id).get_text("sended_to_admins")
            k.row(back(chat_id, "home"))
            send(chat_id, msg, reply_markup=k)
            database.stages(chat_id, "None")





@bot.callback_query_handler(func=lambda m: True)
def g_cals(call):
    chat_id = call.message.chat.id

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    cd = call.data.split("||")

    if call.message.chat.type == "private":

        if call.data == "home":
            start_msg(call.message)
            dm()
        elif call.data == "wallet":
            stg.wallet(chat_id)
            dm()
        elif call.data == "update_wallet":
            stg.update_wallet(chat_id)
            dm()

        elif cd[0] == "set_lang":
            Lang(chat_id).set(cd[1].lower())
            start_msg(call.message)
            dm()


    else:
        if cd[0] in ['allow_wallet', 'deni_wallet']:

            if cd[0] == "allow_wallet":
                user_id = int(cd[1])
                count = int(cd[2])

                database.balance(chat_id, int(database.balance(chat_id)) + count)

                send(chat_id, call.message.text + f"\n\n~ Confirmed by @{str(call.from_user.username)}")
                dm()


                k = kmarkup()
                msg = Texts(chat_id).get_text("allow_wallet")
                k.row(back(chat_id, "home"))
                send(user_id, msg, reply_markup=k)

            elif cd[0] == "deni_wallet":
                user_id = cd[1]


                send(chat_id, call.message.text + f"\n\n~ Denied by @{str(call.from_user.username)}")
                dm()

                k = kmarkup()
                msg = Texts(chat_id).get_text("deni_wallet")
                k.row(back(chat_id, "home"))
                send(user_id, msg, reply_markup=k)





bot.polling()