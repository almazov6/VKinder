import configpars
import vk_api
import user

from vkton.ui import Button
from vkton import Bot, Commands, Context
from vk_api.longpoll import VkLongPoll, VkEventType
from user import User
from vkapi import Vkapi

bot = Bot(configpars.cfg.configparser('VK'), group_id=228101541)
api = vk_api.VkApi(token=configpars.cfg.configparser('VK'))
longpoll = VkLongPoll(api)
vk = Vkapi()


@Commands.command(keywords=['Начать'], back_to='hello')
def hello(ctx: Context):
    id = ctx.user.id
    name = User(id).user_info()
    if len(User(
            id).check_user_info()) == 0:  # Проверка, что профиль полностью заполнен
        ctx.user.send(
            f'Привет {name['first_name']}! Я VKinder, твой виртуальный помощник для знакомств.'
            f'Твой профиль полностью заполнен. Ты можешь начать поиск',
            keys=[
                [Button('Знакомства', 'green')],
                [Button('Список избранных', 'white')]

            ])
    else:
        ctx.user.send(
            f'Привет {name['first_name']}! Я VKinder, твой виртуальный помощник для знакомств.'
            f'В твоём профиле не хватает некоторых данных, давай это изменим.',
            keys=[
                Button('Редактировать профиль', 'red')
            ])


@Commands.command(keywords=['Редактировать профиль'], back_to='hello')
def change_profile(ctx: Context):
    id = ctx.user.id
    for item in User(id).check_user_info():
        if item == 'birthday':
            ctx.user.send(
                f'Дата рождения не заполнена, напиши свой возраст')
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            user.profile_user['birthday'] = user_message.content
            Commands.go_back(ctx)
        #     Изменение даты рождения в базе
        elif item == 'sex':
            ctx.user.send(
                f'Пол не заполнен, выбери свой пол',
                keys=[
                    Button('Мужской', 'white'),
                    Button('Женский', 'white')
                ]
            )
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            user.profile_user['sex'] = user_message.content
            Commands.go_back(ctx)
            #     Изменение пола в базе
        elif item == 'city':
            ctx.user.send(f'Город не заполнен, введи свой город')
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            user.profile_user['city'] = user_message.content
            Commands.go_back(ctx)


@Commands.command(keywords=['Знакомства'], back_to='starting')
def starting(ctx: Context):
    users = vk.user_search(
        user.profile_user['city'],
        user.profile_user['sex'],
        user.profile_user['birthday'],
        user.profile_user['birthday'] + 5,
    )
    for item in range(len(users)):
        ctx.user.send(f'{users[item]['first_name']} '
                      f'{users[item]['last_name']}, '
                      f'{users[item]['city']['title']}',
                      photo_url=f'photo{users[item]['photo_id']}',
                      keys=[
                          [Button('Следующий', 'white')],
                          [Button('Перейти в профиль', 'white',
                                  link=f'https://vk.com/id{users[item]['id']}')],
                          [Button('Добавить в избранное', 'green')],
                          [Button('В начало', 'white')],
                      ])
        user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
        if user_message.content == 'В начало':
            break
        elif user_message.content == 'Следующий':
            continue
        elif user_message.content == 'Добавить в избранное':
            pass
    Commands.redirect(ctx, 'start')


@Commands.command(keywords=['В начало'], back_to='start')
def start(ctx: Context):
    ctx.user.send('f', keys=[
        [Button('Знакомства', 'green')],
        [Button('Список избранных', 'white')]
    ])


bot.run()
