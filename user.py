from datetime import datetime
from pprint import pprint
import datetime
import vkapi as api

profile_user = {
            'first_name': 'Владимир',
            'last_name': 'Алмазов',
            'sex': 2,
            'city': 1,
            'birthday': 19
        }

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
            sex = 'Не заполнено'
        try:
            city = user['city']['id']
        except KeyError:
            city = 'Не заполнено'
        try:
            birthday = datetime.date.today().year - int(user['bdate'][-4:])
        except KeyError:
            birthday = 'Не заполнено'
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
        for item in profile_user.items():
            if item[1] == 'Не заполнено':
                arr.append(item[0])
        return arr