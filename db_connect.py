import psycopg2
from psycopg2 import sql
from psycopg2.sql import SQL, Identifier

conn = psycopg2.connect(database='example_db', user='vladimir',
                        password='26289058')


def create_db():
    with conn.cursor() as cur:
        # cur.execute("""
        # DROP TABLE users CASCADE;
        # DROP TABLE shown CASCADE;
        # DROP TABLE photos CASCADE
        # """);

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id SERIAL,
                    vk_id INTEGER NOT NULL PRIMARY KEY,
                    name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    sex INTEGER,
                    age INTEGER,
                    city VARCHAR(40) 
                    )
                    """);
        cur.execute(""" CREATE TABLE IF NOT EXISTS shown(
                    id serial PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(vk_id), 
                    vk_id_searched VARCHAR(10) NOT NULL,
                    name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    account_url VARCHAR(40),
                    statement VARCHAR(10) NOT NULL
                    )
                    """);

        cur.execute(""" CREATE TABLE IF NOT EXISTS photos(
                    shown_id INTEGER NOT NULL REFERENCES shown(id),
                    photo_url VARCHAR(100)
                    )
                    """);
        conn.commit()


def add_user(vk_id, name, last_name, sex, age, city):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users(vk_id, name, last_name, sex, age, city)
            VALUES(%s, %s, %s, %s, %s, %s)
            RETURNING vk_id, name, last_name, sex, age, city
            """, (vk_id, name, last_name, sex, age, city));
        conn.commit()


def get_user(vk_id_user):
    with (conn.cursor() as cur):
        cur.execute(f"""
            SELECT sex, age, city FROM users
            WHERE vk_id = '{vk_id_user}'
            """)
        ln = cur.fetchone()
        result = {
            'sex': ln[0],
            'age': ln[1],
            'city': ln[2],
        }
        return result


def get_user_id(vk_id_user):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT id FROM users WHERE vk_id = {vk_id_user}""")
        try:
            result = cur.fetchone()[0]
        except TypeError:
            result = 0
    return result


def add_shown(user_id, vk_id_searched, name, last_name, account_url):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO shown(user_id, vk_id_searched, name, last_name, account_url, statement)
            VALUES(%s, %s, %s, %s, %s, 'нейтрально')
            RETURNING user_id, vk_id_searched, name, last_name, account_url, statement
            """, (user_id, vk_id_searched, name, last_name, account_url));
        conn.commit()


def get_shown(vk_id):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT vk_id_searched ,name, last_name, account_url FROM shown WHERE user_id = {vk_id}""")
        result = cur.fetchall()
    return result


def check_shown(vk_id, flag=False):
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT id FROM shown 
            WHERE vk_id_searched = '{vk_id}';
            """)
        result = cur.fetchall()
        if len(result) != 0:
            flag = True
    return flag


def del_shown_user(shown_vk_id):
    with conn.cursor() as cur:
        cur.execute(f"""
                    DELETE FROM shown
                    WHERE vk_id_searched = '{shown_vk_id}';
                    """)
        conn.commit()


def like(vk_id_user):
    with conn.cursor() as cur:
        cur.execute(f"""
            UPDATE shown SET statement='like'
            WHERE id = (SELECT * FROM (SELECT shown.id FROM users
            RIGHT JOIN shown ON users.id = shown.user_id
            WHERE users.vk_id LIKE '{vk_id_user}') 
            ORDER BY id DESC LIMIT 1)
            """)


def dislike(vk_id_user):
    with conn.cursor() as cur:
        cur.execute(f"""
            UPDATE shown SET statement='dislike'
            WHERE id = (SELECT * FROM (SELECT shown.id FROM users
            RIGHT JOIN shown ON users.id = shown.user_id
            WHERE users.vk_id LIKE '{vk_id_user}') 
            ORDER BY id DESC LIMIT 1)        
            """)


def show_likes():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT name, last_name, account_url FROM shown
            WHERE statement LIKE 'like'
            """)
        result = cur.fetchone()
        print(f'{result[0]} {result[1]}, {result[2]}')


# на всякий случай, если с добавлением города получится
def change_gender(user_id, gender_numb):
    with conn.cursor() as cur:
        cur.execute(
            f"""UPDATE users SET sex = '{gender_numb}' WHERE vk_id = '{user_id}'""")
        conn.commit()


def change_age(user_id, age):
    with conn.cursor() as cur:
        stmt = sql.SQL(
            f"""UPDATE users SET age = '{age}' WHERE vk_id = '{user_id}'""").format(
            age=sql.Identifier(str(age)))
        cur.execute(stmt)
        conn.commit()


def change_city(user_id, city):
    with conn.cursor() as cur:
        stmt = sql.SQL(
            f"""UPDATE users SET city = '{city}' WHERE vk_id = '{user_id}'""").format(
            city=sql.Identifier(str(city)))
        cur.execute(stmt)
        conn.commit()


create_db()
