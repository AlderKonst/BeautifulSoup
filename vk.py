import requests  # Импортируем библиотеку requests для работы с HTTP-запросами
from pprint import pprint  # Импортируем pprint для удобного форматирования вывода
import json  # Импортируем json для работы с JSON-данными

token = ('vk1.a.yxxhoAU0X_NN86KDgr58ONhwvxX0TY4KPBM2Ut07EUKbsRlrW_db4PjxJNK2PcEMe0V2'
         'QvXgXLk0SD36rBFcBzvg0R-FQhxCnv-xn_wC93frumLrJy8_LEoZngLo0G_Bo4L_yr22z7rfQM'
         'mXm9f3X7_bvG914Ho25oHv-R3jkrq2vVHTM02I9ohTVK4lU1QbldY0LdFkgJ1MiZfY9Gnqww')  # Токен доступа к API ВКонтакте

method = 'users.search'  # Метод API для поиска пользователей
url = f'https://api.vk.com/method/{method}'  # Формируем URL для запроса к API

params = {  # Параметры запроса к API
    'access_token': token,  # Токен доступа
    'q': 'Свечников',  # Запрос на поиск по имени (по моей фамилии)
    'v': '5.199',  # Версия API
    'hometown': ['Йошкар-Ола'],  # Мой город Йошкар-Ола для фильтрации результатов
    'fields': 'education, home_town'  # Поля, которые нужно вернуть в ответе (образование и город)
}

result = requests.get(url, params=params)  # Отправляем GET-запрос к API с указанными параметрами
result.encoding = 'UTF-8'  # Устанавливаем кодировку ответа на UTF-8 на всякий
pprint(result.json())  # Выводим ответ в формате JSON с удобным форматированием