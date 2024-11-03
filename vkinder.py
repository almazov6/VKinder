from vkton.ui import Button

import configpars
from vkton import Bot, Commands, Context

import user
from user import User
from vkapi import Vkapi
from vkton.ui import CarouselField

bot = Bot(configpars.cfg.configparser('VK'), group_id=228101541)


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
                Button('Знакомства', 'green')
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
            user.profile_user['birthday'] = user_message
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
            user.profile_user['sex'] = user_message
            Commands.go_back(ctx)
            #     Изменение пола в базе
        elif item == 'city':
            ctx.user.send(f'Город не заполнен, введи свой город')
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            user.profile_user['city'] = user_message
            Commands.go_back(ctx)


@Commands.command(keywords=['Знакомства'], back_to='starting')
def starting(ctx: Context):
    for item in Vkapi().groups_getMembers()['items']:
        id = item['id']
        first_name = item['first_name']
        city = item['city']['title']
        sex = item['sex']
        birthday = 'None'
        photo = item['photo_max']
        ctx.user.send(
            f'{first_name}, {city}, {birthday}',
            photo_url=photo,
            keys=[
                Button('Добавить в избранное', 'green'),
                Button('Написать сообщение', 'white'),
                Button('Добавить в черный список', 'red')
            ]
        )

bot.run()
