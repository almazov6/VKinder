# VKinder

Vkinder - это приложение для знакомств VKontakte. 

- Пользователь приложение запускает чат командой 'Начать' ( запуск __def hello()__  здесь и далее в основном коде). 
- Бот приветствует пользователя, проверяет заполнена ли в аккаунте пользователя вся необходимая для корректной работы приложения информация. Поиск осуществляется по полу возрасту и городу проживания пользователя. Если заполнено не все, то бот предлагает ввести недостающие данные через 'Редактировать профиль' (запуск __def change_profile()__). 
- Пользователь нажимает кнопку 'Знакомства' (запуск __def starting()__ ), и бот выводит в чат вариант, подходящий пользователю. Появляются кнопки меню: 
 
  'Следующий', 
  
  'Перейти в профиль', 
  
  'Добивить в избранное', 
  
  'В начало'.

- При добавлении в избранное у пользователя появляется возможность: 
  + посмотреть список избранных вариантов (запуск __def shown_list()__), 
  + удалить вариант из списка избанных , введя vk_id варианта (запуск __def del_shown_list()__);
  +  вернуться в главное меню (запуск __def start()__).
   

 
***
*** 
## Проект включает в себя:
README.md
***

Основной код содержится в __vkinder.py__.
***
### Пакет VK:
Модуль __user__ предоставляет класс User, содержащий следующие методы и функции:

1. '\____init__\__': инициализация объекта класса User;
2. '__user_info__':  взаимодействуя с методом __users_get__ класса Vkapi, возвращает информацию о пользователе приложения. Если информация о пользователе пришла неполная, выводит сообщение 'Не заполнено'.
3. '__check_user_info__': проверяет, есть ли в базе данных информация о пользователе.

***
Модуль __vkapi__ предоставляет класс Vkapi для взаимодействия с VK API. Содержит следующие методы и функции:

1. '\____init__\__: инициализация объекта класса Vkapi;
2. '__get_commot_params__': возвращает параметры запроса: vk-токен и версию VK API;
3. '__users_get__': возвращает информацию о пользователе приложения в формате json;
4. '__user_search__': осуществляет глобальный поиск вариантов в VK для показа пользователю по заданным параметрам и возвращает в формате json;
5. '__photos_get__': ищет для показа три самые популярные фотографии найденного варианта при условии открытого доступа к альбомам;
6. '__messages_send__': отправляет в чат отобранные фотографии варианта.
***
Модуль __configpars__  предоставляет класс ConfigParser, содержащий метод '__configparser__' для поиска  vk токена по файлу с конфигурациями __setting.ini__.
***
### Пакет __data_base__:
***
Модуль __db_connect__ отвечает за связь между приложением и базой данных. Содержит следующие функции:

1. '__create_db__': создает три таблицы в базе данных. Структура таблиц: [схема базы данных](/VKINDER/data_base_structure.png);
2. '__add_user__': добавляет информацию о пользователе приложения в базу данных;
3. '__get_user__': принимает в качестве аргумента vk_id пользователя приложения и выдает из базы информацию о нем для дальшейшего использования;
4. '__get_user_id__': принимает в качестве аргумента vk_id пользователя приложения, возвращает id пользователя в базе данных;
5. '__add_shown__': добавляет информацию о показанном варианте в базу данных при нажатии кнопки 'Добавить в избранное';
6. '__get_shown__': выводит список избранных с ссылкой на аккаунт и самой популярной фотографией;
7. '__check_shown__': принимает в качестве аргумента vk_id показанного варианта и проверяет на наличие в списке избранных;
8. '__delete_shown_user__': удаляет из списка избранных в базе данных по vk_id варианта;
9. '__change_gender__': вносит в базу данных информацию о поле пользователя приложения, если информация о пользователе неполная;
10. '__change_age__': вносит в базу данных информацию о возрасте пользователя приложения, если информация о пользователе неполная;
11. '__change_city__': вносит в базу данных информацию о городе пользователя приложения, если информация о пользователе неполная;
12. '__add_photos__': добавляет фотографии избранного варианта в базу данных.
13. '__get_photos__': Возвращает идентификатор фотографии.

***
В __db_configs.py__ следует поместить данные для подключения к базе данных.
***

 





    
