import requests
import configpars
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent


vk_session = vk_api.VkApi(token =configpars.cfg.configparser('VK'))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 228101541)

for event in longpoll.listen():
    print(event.message.text)
