import vk_api
import data_base.db_connect as database

from vkton.ui import Button
from vkton import Bot, Commands, Context
from vk_api.longpoll import VkLongPoll

from VK.config import VK_TOKEN
from VK.user import User
from VK.vkapi import Vkapi

bot = Bot(VK_TOKEN, group_id=228101541)
api = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(api)
vk = Vkapi()


@Commands.command(keywords=['Начать'], back_to='hello')
def hello(ctx: Context):
    id_user = ctx.user.id
    user_info = User(id_user).user_info()
    if database.get_user_id(id_user) == 0:
        database.add_user(
            id_user,
            user_info['first_name'],
            user_info['last_name'],
            user_info['sex'],
            user_info['birthday'],
            user_info['city'],
        )
    if len(User(
            id_user).check_user_info()) == 0:  # Проверка, что профиль полностью заполнен
        ctx.user.send(
            f'Привет {user_info['first_name']}! Я VKinder, твой виртуальный помощник для знакомств.'
            f'Твой профиль полностью заполнен. Ты можешь начать поиск',
            keys=[
                [Button('Знакомства', 'green')],
                [Button('Список избранных', 'white')]

            ])
    else:
        ctx.user.send(
            f'Привет {user_info['first_name']}! Я VKinder, твой виртуальный помощник для знакомств.'
            f'В твоём профиле не хватает некоторых данных, давай это изменим.',
            keys=[
                Button('Редактировать профиль', 'red')
            ])


@Commands.command(keywords=['Редактировать профиль'], back_to='hello')
def change_profile(ctx: Context):
    user_id = ctx.user.id
    for item in User(user_id).check_user_info():
        if item == 'age':
            ctx.user.send(
                f'Дата рождения не заполнена, напиши свой возраст')
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            database.change_age(user_id, int(user_message.content))
            ctx.user.send(
                f'Возраст успешно изменен.')
            Commands.go_back(ctx)
        elif item == 'sex':
            ctx.user.send(
                f'Пол не заполнен, выбери свой пол',
                keys=[
                    Button('Мужской', 'white'),
                    Button('Женский', 'white')
                ]
            )
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            gender = 2 if user_message.content == 'Мужской' else 1
            database.change_gender(user_id, gender)
            ctx.user.send('Пол успешно изменен.')
            Commands.go_back(ctx)
        elif item == 'city':
            ctx.user.send(f'Город не заполнен, введи свой город')
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            database.change_city(user_id, user_message.content)
            ctx.user.send('Город успешно изменен')
            Commands.go_back(ctx)


@Commands.command(keywords=['Знакомства'], back_to='starting')
def starting(ctx: Context):
    users = vk.user_search(
        database.get_user(ctx.user.id)['city'],
        database.get_user(ctx.user.id)['sex'],
        database.get_user(ctx.user.id)['age'] - 5 if
        database.get_user(ctx.user.id)[
            'age'] >= 23 else 18,
        database.get_user(ctx.user.id)['age'] + 5,
    )
    for item in range(len(users)):
        if vk.photos_get(users[item][
                             'id']) != 'Profile private' and not database.check_shown(
            users[item]['id']):
            ctx.user.send(f'{users[item]['first_name']} '
                          f'{users[item]['last_name']}',
                          keys=[
                              [Button('Следующий', 'white')],
                              [Button('Перейти в профиль', 'white',
                                      link=f'https://vk.com/id{users[item]['id']}')],
                              [Button('Добавить в избранное', 'green')],
                              [Button('В начало', 'white')],
                          ])
            for ind in range(len(vk.photos_get(users[item]['id']))):
                vk.messages_send(ctx.user.id, users[item]['id'],
                                 vk.photos_get(users[item]['id'])[ind][1])
            user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
            if user_message.content == 'В начало' or user_message.content == '':
                break
            elif user_message.content == 'Следующий':
                continue
            elif user_message.content == 'Добавить в избранное':
                database.add_shown(ctx.user.id,
                                   users[item]['id'],
                                   users[item]['first_name'],
                                   users[item]['last_name'],
                                   f'https://vk.com/id{users[item]['id']}',
                                   )
                database.add_photos(users[item]['id'])
                ctx.user.send('Профиль добавлен в избранное')
    Commands.redirect(ctx, 'start')


@Commands.command(keywords=['В начало'], back_to='start')
def start(ctx: Context):
    ctx.user.send('Вы вернулись в главное меню', keys=[
        [Button('Знакомства', 'green')],
        [Button('Список избранных', 'white')]
    ])


@Commands.command(keywords=['Список избранных'], back_to='start')
def shown_list(ctx: Context):
    if len(database.get_shown(ctx.user.id)) == 0:
        ctx.user.send(f'Список избранных контактов пуст')
    else:
        ctx.user.send(f'Список избранных аккаунтов')
        for item in database.get_shown(ctx.user.id):
            ctx.user.send(f'ID: {item[0]}, {item[1]} {item[2]}, {item[3]}',
                          keys=[
                              [Button('Удалить из списка', 'red')],
                              [Button('Список избранных', 'green')],
                              [Button('В начало', 'white')]
                          ])
            vk.messages_send(ctx.user.id, item[0], item[4])


@Commands.command(keywords=['Удалить из списка'], back_to='start')
def del_shown_list(ctx: Context):
    ctx.user.send(
        f'Напиши ID пользователя которого необходимо удалить из списка избранных')
    user_message = bot.wait_message(ctx.user, timeout=24 * 3600)
    database.del_shown_user(user_message.content)
    ctx.user.send(
        f'Пользователь успешно удален из списка избранных.')


bot.run()
