import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def db_admin():
    db = psycopg2.connect(user="postgres", password="armageddon", host="illyashost.ddns.net", port=5432)
    db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    sql = db.cursor()
    return db, sql


def db_user(username, password):
    db = psycopg2.connect(database=username, user=username, password=password, host="illyashost.ddns.net", port=5432)
    db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    sql = db.cursor()
    return db, sql


def db_close(db):
    try:
        db.close()
    except:
        pass


class DBcreator:
    def __init__(self, role_name,password=None):
        self.role_name = role_name
        self.password = password

    # 1
    def create_role(self):
        db, sql = db_admin()
        if self.role_name != None:
            sql.execute(f"""CREATE ROLE {self.role_name} WITH 
            LOGIN 
            NOSUPERUSER 
            INHERIT
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION
            PASSWORD '{self.password}'""")
            db.commit()
        else:
            print("[-] Cant create role without password")
        db_close(db)

    # 2
    def create_db_for_role(self,
                           db_name: str,
                           connections: int = -1,
                           owner: str = "postgres"):
        db, sql = db_admin()
        if connections == -1:
            sql.execute(f"""CREATE DATABASE {db_name}
    WITH 
    OWNER = {owner}
    ENCODING = 'UTF8'
    """)
            db.commit()
        else:
            sql.execute(f"""CREATE DATABASE {db_name}
    WITH 
    OWNER = {owner}
    ENCODING = 'UTF8'
    CONNECTION LIMIT = {connections}""")
            db.commit()

        sql.execute(f"GRANT ALL ON DATABASE {db_name} TO {self.role_name}")
        db.commit()
        sql.execute(f"GRANT ALL ON DATABASE {db_name} TO {owner} WITH GRANT OPTION")
        db.commit()
        sql.execute(f"REVOKE ALL ON DATABASE {db_name} FROM public")
        db.commit()

        db_close(db)

    def try_as_user(self):
        db, sql = db_user(self.role_name, self.password)
        result = []
        sql.execute("SELECT * FROM pg_catalog.pg_tables")
        for i in sql.fetchall():
            if i[0] not in result:
                result.append(i[0])

        db_close(db)
        return result

