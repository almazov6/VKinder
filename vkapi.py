from pprint import pprint

import configpars
import requests

API_BASE_URL = 'https://api.vk.com/method'


class Vkapi:
    def __init__(self, token=configpars.ConfigParser.configparser('VK'),
                 version='5.199'):
        self.token = token
        self.version = version

    def get_commot_params(self):
        return {
            'access_token': self.token,
            'v': self.version
        }

    def users_get(self, user_id):
        params = self.get_commot_params()
        params.update({
            'user_ids': user_id,
            'fields': 'bdate, city, sex'
        })
        response = requests.get(f'{API_BASE_URL}/users.get', params=params)
        return response.json()

    def user_search(self, city_id, sex, age_from, age_to):
        params = self.get_commot_params()
        params.update({
            'access_token': configpars.ConfigParser.configparser('USR'),
            'fields': 'photo_id, city',
            'has_photo': 1,
            'city': city_id,
            'sex': 1 if sex == 2 else 2,
            'age_from': age_from,
            'age_to': age_to

        })
        response = requests.get(f'{API_BASE_URL}/users.search', params=params)
        return response.json()['response']['items']

    def photos_get(self, user_id):
        params = self.get_commot_params()
        params.update({
            'access_token': configpars.ConfigParser.configparser('SVK'),
            'owner_id': user_id,
            'extended': 1
        })
        response = requests.get(f'{API_BASE_URL}/photos.get', params=params)
        return response.json()

# vk = Vkapi()
#
# pprint(vk.photos_get(58595130))