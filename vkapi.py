from ast import Param
from http.client import responses
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

    def groups_getMembers(self):
        id = 228101541
        params = self.get_commot_params()
        params.update({
            'group_id': id,
            'fields': 'bdate, photo_max, city, sex'
        })
        response = requests.get(f'{API_BASE_URL}/groups.getMembers', params=params)
        return response.json()['response']