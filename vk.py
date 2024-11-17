import requests  # Импортируем библиотеку requests для работы с HTTP-запросами
from pprint import pprint  # Импортируем pprint для удобного форматирования вывода
import json  # Импортируем json для работы с JSON-данными (почему-то серым отображает)
import sqlite3 # Импортирует sqlite3 для работы с базами данных

token = ('vk1.a.yxxhoAU0X_NN86KDgr58ONhwvxX0TY4KPBM2Ut07EUKbsRlrW_db4PjxJNK2PcEMe0V2'
         'QvXgXLk0SD36rBFcBzvg0R-FQhxCnv-xn_wC93frumLrJy8_LEoZngLo0G_Bo4L_yr22z7rfQM'
         'mXm9f3X7_bvG914Ho25oHv-R3jkrq2vVHTM02I9ohTVK4lU1QbldY0LdFkgJ1MiZfY9Gnqww')  # Токен доступа к API ВКонтакте
method = 'users.search'  # Метод API для поиска пользователей
url = f'https://api.vk.com/method/{method}'  # Формируем URL для запроса к API
params = {  # Параметры запроса к API
    'access_token': token,  # Токен доступа
    'q': 'Свечников',  # Запрос на поиск по имени (по моей фамилии)
    'v': '5.199',  # Версия API
    'hometown': 'Йошкар-Ола',  # Мой город Йошкар-Ола для фильтрации результатов
    'fields': 'education, home_town'  # Поля, которые нужно вернуть в ответе (образование и город)
}

response = requests.get(url, params=params)  # Отправляем GET-запрос к API с указанными параметрами
response.encoding = 'UTF-8'  # Устанавливаем кодировку ответа на UTF-8 на всякий
result = response.json() # Сохраняем в переменной результаты поиска в в формате JSON

sql = sqlite3.connect('vk.sqlite') # Подключаемся к базе
cursor = sql.cursor() # Создаём курсор

for n, user in enumerate(result['response']['items']):
    cursor.execute("insert or ignore into first_name (name) VALUES (?)", # Делаем SQL-запрос на внесение записи
                   (user['first_name'],)) # Вносимые значения (имя)
    cursor.execute("insert or ignore into university_name (id, name) VALUES (?, ?)",  # Делаем SQL-запрос на внесение записи
                   (user['university'], user['university_name']))  # Вносимые значения (номер и название универа)
    cursor.execute("insert or ignore into svecha_yoshka (id, first_name_id, university_id) VALUES (?, ?, ?)",
                   # Делаем SQL-запрос на внесение записи
                   (user['id'], n+1, user['university']))  # Вносимые значения (VK ID, id имени и универа)
    sql.commit() # Вносим собранные изменения в базу данных

query = ('select s.id, f.name, u.name '
         'from svecha_yoshka s, first_name f, university_name u '
         'where s.first_name_id = f.id and s.university_id = u.id')  # Текст SQL-запроса на отображение таблоданных

cursor.execute(query) # Проводим сам запрос и получаем данные
pprint(cursor.fetchall()) # Выводим список кортежей в более менее читаемом виде