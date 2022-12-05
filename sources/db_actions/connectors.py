import psycopg2
import iluxaMod as ilm
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

database = ilm.postgreSQL_connect(user="db_sale", password="armageddon", database="db_sale", host="illyashost.ddns.net")
database.init_DB(stages=True, sub=True, settings=True, staff=True, balance=True, stdout=False)
db = database.db
sql = database.sql

def db_admin():
    adb = psycopg2.connect(user="postgres", password="armageddon", host="illyashost.ddns.net", port=5432)
    adb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    asql = adb.cursor()
    return adb, asql

def db_user(username, password):
    adb = psycopg2.connect(database=username, user=username, password=password, host="illyashost.ddns.net", port=5432)
    adb.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    asql = adb.cursor()
    return adb, asql

def db_close(adb):
    try:
        adb.close()
    except:
        pass
