from pprint import pprint
import vkapi as api

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
            city = user['city']['title']
        except KeyError:
            city = 'Не заполнено'
        try:
            birthday = user['bdate']
        except KeyError:
            birthday = 'Не заполнено'
        result = {
            'first_name': first_name,
            'last_name': last_name,
            'sex': 'Мужской' if sex == 2 else 'Женский',
            'city': city,
            'birthday': birthday
        }
        return result