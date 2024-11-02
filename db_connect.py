import psycopg2 as db

try:
    connection = db.connect(
        datebase="",
        user="",
        password=""
    )
except Exception as error:
    print(f'Ошибка подключения к базе данных {error}')


# Черный список
def add_to_blacklist():
    pass


def remove_from_blacklist():
    pass


def show_blacklist():
    pass


# Список избранных
def add_to_favoritlist():
    pass


def remove_from_favoritlist():
    pass


def show_favoritlist():
    pass


# Юзер
def add_user(user_id, name, age, gender, city):
    with connection.cursor() as cur:
        cur.execute(f"""
    INSERT INTO Userlist(user_id, name, age, gender, city)
    VALUES ({user_id}, {name}, {age}, {gender}, {city})
    """)
    connection.commit()


def delete_account(user_id):
    pass


def change_gender(user_id):
    pass


def change_age(user_id):
    pass


def change_city(user_id):
    pass
