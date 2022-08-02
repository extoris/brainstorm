import datetime
import sqlite3

import pytz

CONN = sqlite3.connect('brainstorm.db')
cur = CONN.cursor()


def get_cursor():
    return cur

# ----------------------------Words------------------------------------------

def get_random_string(database):
    conn = sqlite3.connect(database)
    with conn as cursor:
        return cursor.execute('SELECT * FROM voices ORDER BY RANDOM() LIMIT 1').fetchall()[0]

def get_example_words(database):
    conn = sqlite3.connect(database)
    with conn as cursor:
        return [item for sublist in cursor.execute('SELECT translate text FROM voices ORDER BY RANDOM() LIMIT 4').fetchall() for item in sublist]



# -----------------------------Users-----------------------------------------
def dp_all_users_list():
    cur.execute("""SELECT telegram_user_id FROM users;""")
    result = cur.fetchall()
    users_telegram_id_list = [i[0] for i in result]
    return users_telegram_id_list


def dp_user_create(telegram_user_id):
    cur.execute(f"""INSERT INTO users (telegram_user_id, date_reg)
VALUES ({telegram_user_id}, '{datetime.datetime.now()}');""")
    cur.connection.commit()
    return

# -----------------------------statistics-----------------------------------------
def dp_admin_stat():
    cur.execute("""SELECT telegram_user_id, date_reg FROM users;""")
    result = cur.fetchall()
    return result


def dp_admin_stat_actions():
    cur.execute("""SELECT telegram_user_id, time_action FROM actions;""")
    result = cur.fetchall()
    return result