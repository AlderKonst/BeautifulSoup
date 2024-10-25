import requests  # Импортируем библиотеку для работы с HTTP-запросами
from bs4 import BeautifulSoup  # Импортируем библиотеку для парсинга HTML

url = 'http://марниисх.рф'  # Определяем URL сайта
result = requests.get(url)  # Отправляем GET запрос по указанному URL
result.encoding = 'utf-8'  # Устанавливаем кодировку ответа
# print(result.text)  # Выводим содержимое страницы

soup = BeautifulSoup(result.text, 'html.parser')  # Создаем объект BeautifulSoup для парсинга HTML
# print(soup.a)  # Выводим 1-й тег <a> страницы (тип не строка, а тип BeautifulSoup)
# print(soup.a.string)  # Выводим уже сам текст внутри этого тега (тут тоже тип не строка, а тип BeautifulSoup)
# print(soup.a.text)  # Тут тоже выводим текст внутри этого тега (тут уже тип строка)
# print(soup.a.get('href'))  # Выводим значение внутри его атрибута
# print(soup.find_all('a'))  # Выводим все теги с <a> страницы

# tags = soup.find_all('ul')  # Находим все теги <ul> на странице
# for tag in tags:  # Проходимся по каждому найденному тегу
#     print(tag.text)  # Выводим текст внутри каждого тега <ul>

div_class_vk = soup.find('div', class_='references')  # Находим первый элемент <div> с классом 'references'
# print(div_class_vk)  # Выводим найденный элемент
# a_id_maripogoda = div_class_vk('a', id='maripogoda')  # Находим все элементы <a> с id 'maripogoda' внутри найденного <div>
# print(a_id_maripogoda[0])  # Выводим первый найденный элемент <a>

# for i in range(len(div_class_vk.contents)):  # Проходим по всем дочерним элементам div_class_vk
#     print(i, div_class_vk.contents[i])  # Выводим индекс и сам элемент (для ориентации в следующей строке кода)

# print(div_class_vk.contents[9].contents[0])  # Выводим 1-й дочерний элемент 10-го элемента div_class_vk, если бы был неизвестен id

# for child in div_class_vk.children:  # Проходим по прямым потомкам (детям) элемента div_class_vk
#     print(child)  # Выводим каждого прямого потомка

for descendant in div_class_vk.descendants:  # Проходим по всем потомкам (внукам, правнукам и так далее) элемента div_class_vk
    print(descendant)  # Выводим каждого потомка
