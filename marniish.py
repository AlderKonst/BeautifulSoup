import requests  # Импортируем библиотеку для работы с HTTP-запросами
from bs4 import BeautifulSoup  # Импортируем библиотеку для парсинга HTML
import json  # Импортируем библиотеку для работы с JSON-файлами

domain = 'http://марниисх.рф'  # Определяем URL сайта нашего НИИ
news_url = f'{domain}/News.html' # Страница нашего НИИ, посвящённой новостям 2022 года
tags_lst = [['Меню сайта', domain, 'ul', 'side', 'a'],  # Группа тегов для меню сайта
            ['Направления деятельности', domain, 'section', 'areas', 'strong'],  # Группа тегов для направлений деятельности
            ['Полезные ссылки', domain, 'div', 'references', 'a'],  # Группа тегов для полезных ссылок
            ['Новости текущего года', news_url, 'div', 'pages', 'h3']]  # Группа тегов для новостей 2024 года
head_lst = [{tags_lst[0][0]: []},  # 'Меню сайта'
            {tags_lst[1][0]: []},  # 'Направления деятельности'
            {tags_lst[2][0]: []},  # 'Полезные ссылки'
            {tags_lst[3][0]: []}]  # 'Новости 2024 года'
for i in range(len(tags_lst)):  # Проходим по всем группам тегов
    result = requests.get(tags_lst[i][1])  # Отправляем GET запрос по указанному URL
    result.encoding = 'utf-8'  # Устанавливаем кодировку ответа
    soup = BeautifulSoup(result.text, 'html.parser')  # Парсим исходный HTML-код
    tag_1 = soup.find(tags_lst[i][2], class_ = tags_lst[i][3])  # Находим первый элемент 1-го тега (tags[1]) с классом (tags[2])
    tag_2 = tag_1.find_all(tags_lst[i][4])  # Из найденного элемента извлекаем все соответствующие подтеги вида tags[3]
    tag_nums = [n for n in range(len(tag_2))]  # Создаём порядковый список по количеству найденных пунктов тегов
    for n in tag_nums:  # Проходимся по всем найденным пунктам
        if i == 0:
            text = tag_2[n].text  # Сохраняем текст пункта
            href = tag_2[n].get('href')  # Извлекаем атрибут href
            url = f'{tags_lst[i][1]}/{href}'  # Формируем полный URL страницы сайта
            result = requests.get(url)  # Отправляем GET-запрос по сформированному URL
            result.encoding = 'utf-8'  # Устанавливаем кодировку ответа
            soup = BeautifulSoup(result.text, 'html.parser')  # Парсим содержимое новой страницы
            header = soup.title.text[:-72] # Извлекаем заголовок страницы, обрезаем последние 72 символа
            tag_nums[n] = {url: header}  # Добавляем в список url и заколовок
            head_lst[i][tags_lst[i][0]] = tag_nums  # Добавляем словарь в список результатов
        elif i == 2:
            href = tag_2[n].get('href')  # Извлекаем атрибут href
            title = tag_2[n].get('title')  # Извлекаем атрибут title
            tag_nums[n] = {href: title}  # Добавляем в список url и заколовок
            head_lst[i][tags_lst[i][0]] = tag_nums  # Добавляем словарь в список результатов
        else:
            text = tag_2[n].text  # Сохраняем текст пункта
            tag_nums[n] = text  # Добавляем в список url и заголовок
            head_lst[i][tags_lst[i][0]] = tag_nums  # Добавляем словарь в список результатов

with open('NIIparser.json', 'w', encoding='utf-8') as file:  # Сохраняем результат в JSON файл
    json.dump(head_lst, file, ensure_ascii=False,  indent=4)  # С адекватной поддержкой киррилицы и с отступами