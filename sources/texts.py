import os
from sources.db_actions.connectors import *
import iluxaMod as ilm

pickle = ilm.tools.pickle

pickle("db_actions/langs").pick([''])

texts_list = [
    # start_msg
    {
        "text_id": "start_msg",
        "ru": "<b>Добро пожаловать</b>",
        "en": ""
    },
    # wallet
    {
        "text_id": "wallet",
        "ru": """<b>Кошелек</b>

Текущий баланс: {bal}""",
        "en": ""
    },
    # send_link
    {
        "text_id": "send_link",
        "ru": """<b>Пополнение баланса</b>

<b>Требуется отправить:</b> {to_send}$
<b>На биткоин адрес:</b>
<code>{btc_address}</code>

После отправки средств, вам будет выдан код транзакции или ссылка на транзакцию.
Пришлите сюда полученные ссылку либо код транзакции""",
        "en": ""
    },
    # update_wallet
    {
        "text_id": "update_wallet",
        "ru": """<b>Пополнение баланса</b>

Введите сумму, которую требуется пополнить (в долларах США)""",
        "en": ""
    },
    # sended_to_admins
    {
        "text_id": "sended_to_admins",
        "ru": """<b>Пополнение баланса</b>

Заявка на пополнение баланса была отправлена на рассмотрение.
Мы уведомим вас, когда заявку одобрят либо же отклонят""",
        "en": ""
    },
    # admins_template
    {
        "text_id": "admins_template",
        "ru": """<b>Пополнение баланса</b>

<b>Пользователь:</b> {user_id} 
<b>Сумма:</b> {count}

<b>Ссылка:</b> {link}""",
        "en": ""
    },

    # allow_wallet
    {
        "text_id": "allow_wallet",
        "ru": """<b>Пополнение баланса совершено успешно</b>

Ваш баланс был успешно пополнен""",
        "en": ""
    },

    # deni_wallet
    {
        "text_id": "deni_wallet",
        "ru": """<b>Пополнение баланса провалено</b>

Ваш баланс не был пополнен. Скорее всего вы ввели не верные данные, или вовсе ничего не отправили""",
        "en": ""
    },




    # wallet_btn
    {
        "text_id": "wallet_btn",
        "ru": "Кошелек",
        "en": "Wallet"
    },
    # back_btn
    {
        "text_id": "back_btn",
        "ru": "Назад",
        "en": "Back"
    },
    # update_wallet_btn
    {
        "text_id": "update_wallet_btn",
        "ru": "Пополнить баланс",
        "en": ""
    }
]
pickle("db_actions/langs").pick(texts_list)


class Lang:
    def __init__(self, user_id):
        self.user_id = user_id


    def get(self):
        sql.execute(f"SELECT * FROM langs WHERE user_id = '{str(self.user_id)}'")
        if sql.fetchone() is None:
            for user_id, lang in sql.fetchall():
                if user_id == self.user_id:
                    return lang
        else:
            sql.execute(f"INSERT INTO langs VALUES ('{str(self.user_id)}', 'None')")
            db.commit()
            return "None"

    def set(self, value):
        sql.execute(f"SELECT * FROM langs WHERE user_id = '{str(self.user_id)}'")
        if sql.fetchone() is None:
            sql.execute(f"UPDATE langs SET lang = '{str(value)}' WHERE user_id = '{str(self.user_id)}'")
            db.commit()
        else:
            sql.execute(f"INSERT INTO langs VALUES('{str(value)}', '{str(self.user_id)}')")
            db.commit()


class Texts:
    def __init__(self, user_id):
        self.lang = Lang(user_id).get()
        self.texts_list = pickle("db_actions/langs").unpick()
    def get_text(self, text_id) -> str:
        for i in self.texts_list:
            if i["text_id"] == text_id:
                return i[self.lang]

