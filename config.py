from sources.db_actions.connectors import *
from sources.texts import Lang, Texts


tg = ilm.tgBot("")
bot = tg.bot
bot.parse_mode = "HTML"

send = tg.send
kmarkup = tg.kmarkup
btn = tg.btn

admin_g = 0

def back(chat_id, callback_data):
    return tg.back(callback_data=callback_data, bname=Texts(chat_id).get_text("back_btn"))


def preDB():
    sql.execute(f"""CREATE TABLE IF NOT EXISTS langs (
    user_id TEXT,
    lang TEXT)""")
    db.commit()



class DBcreator:
    def __init__(self, role_name, password=None):
        self.role_name = role_name
        self.password = password

    def batabase_exists(self):
        adb, asql = db_admin()
        dbs = []
        asql.execute("SELECT * FROM pg_catalog.pg_tables")
        for i in asql.fetchall():
            if i[0] not in dbs:
                dbs.append(i[0])
        db_close(adb)
        if self.role_name in dbs:
            return True
        else:
            return False

    # 1
    def create_role(self):
        adb, asql = db_admin()
        if self.role_name != None:
            asql.execute(f"""CREATE ROLE {self.role_name} WITH 
            LOGIN 
            NOSUPERUSER 
            INHERIT
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION
            PASSWORD '{self.password}'""")
            adb.commit()
        else:
            print("[-] Cant create role without password")
        db_close(adb)

    # 2
    def create_db_for_role(self,
                           db_name: str,
                           connections: int = -1,
                           owner: str = "postgres"):
        adb, asql = db_admin()
        if connections == -1:
            asql.execute(f"""CREATE DATABASE {db_name}
    WITH 
    OWNER = {owner}
    ENCODING = 'UTF8'
    """)
            adb.commit()
        else:
            asql.execute(f"""CREATE DATABASE {db_name}
    WITH 
    OWNER = {owner}
    ENCODING = 'UTF8'
    CONNECTION LIMIT = {connections}""")
            adb.commit()

        asql.execute(f"GRANT ALL ON DATABASE {db_name} TO {self.role_name}")
        adb.commit()
        asql.execute(f"GRANT ALL ON DATABASE {db_name} TO {owner} WITH GRANT OPTION")
        adb.commit()
        asql.execute(f"REVOKE ALL ON DATABASE {db_name} FROM public")
        adb.commit()

        db_close(adb)




