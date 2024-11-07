import datetime
import VK.vkapi as api
import data_base.db_connect as database

from datetime import datetime


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def user_info(self):
        user = api.Vkapi().users_get(self.user_id)['response'][0]
        first_name = user['first_name']
        last_name = user['last_name']
        try:
            sex = user['sex']
        except KeyError:
            sex = 0
        try:
            city = user['city']['title']
        except KeyError:
            city = 'Не заполнено'
        try:
            birthday = datetime.date.today().year - int(user['bdate'][-4:])
        except KeyError:
            birthday = 0
        result = {
            'first_name': first_name,
            'last_name': last_name,
            'sex': sex,
            'city': city,
            'birthday': birthday
        }
        return result

    def check_user_info(self) -> list:
        arr = []
        for item in database.get_user(self.user_id).items():
            if item[1] == 'Не заполнено' or item[1] == 0:
                arr.append(item[0])
        return arr
