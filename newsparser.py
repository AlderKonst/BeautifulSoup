import requests  # Импортируем библиотеку для работы с HTTP-запросами
from bs4 import BeautifulSoup  # Импортируем библиотеку для парсинга HTML
from pprint import pprint

domain = 'http://марниисх.рф'  # Определяем URL сайта
result = requests.get(domain)  # Отправляем GET запрос по указанному URL
result.encoding = 'utf-8'  # Устанавливаем кодировку ответа
soup = BeautifulSoup(result.text, 'html.parser')  # Парсим исходный HTML-код
news_ul = soup.find_all('ul', class_ = 'side')  # Находим все элементы ul с классом 'side'
news_a = news_ul[0].find_all('a')  # Из первого найденного элемента извлекаем все ссылки (<a>)
titles = {}  # Создаем пустой словарь для хранения заголовков
for one_news_a in news_a:  # Проходимся по всем ссылкам
    text = one_news_a.text  # Сохраняем текст ссылки
    href = one_news_a.get('href')  # Извлекаем атрибут href
    url = f'{domain}/{href}'  # Формируем полный URL
    result = requests.get(url)  # Отправляем GET-запрос по сформированному URL
    result.encoding = 'utf-8'  # Устанавливаем кодировку ответа
    soup = BeautifulSoup(result.text, 'html.parser')  # Парсим содержимое новой страницы
    titles[url] = soup.title.text[:-54]  # Добавляем заголовок страницы в словарь, обрезаем последние 54 символа
pprint(titles)  # Печатаем результат
