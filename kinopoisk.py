import requests  # Импортируем библиотеку для работы с HTTP-запросами
from bs4 import BeautifulSoup  # Импортируем библиотеку для парсинга HTML
import json  # Импортируем библиотеку для работы с JSON-файлами

feedback_statuses = ['good', 'bad'] # Список статусов отзывов
feedback_nums = {'10', '50', '100'} # Количество плохих или хороших отзывов
url_basic = 'https://www.kinopoisk.ru/film/258687/reviews/ord/date/status/'# Определяем базовую часть URL со страницей отзывов к фильму Интерстеллар
urls = [f'{url_basic}{feedback_status}/perpage/' for feedback_status in feedback_statuses] # Создаем список URL-строк
for feedback_num in feedback_nums: # Проходимся по всем числам отзывов
    feedbacks_dict = {} # Инициируем словарь отзывов с его статусом
    for n, url in enumerate(urls): # Проходимся по всем URL со статусом отзывов
        feedback_url = f'{url}{feedback_num}/' # Формируем URL одного отзывов
        result = requests.get(feedback_url) # Отправляем GET-запрос по указанному URL
        result.encoding = 'utf-8' # Устанавливаем кодировку ответа
        soup = BeautifulSoup(result.text, 'html.parser') # Парсим исходный HTML-код
        feedbacks = soup.find_all('div', class_ = f'response {feedback_statuses[n]}') # Находим все элементы div с классом 'response good' или 'response bad'
        feedbacks_status_dict = {} # Инициируем словарь с авторами и их отзывами
        for feedback in feedbacks: # Проходимся по всем отзывам
            author = feedback.find('p', class_ = 'profile_name').a.text # Извлекаем имя автора отзыва
            text = feedback.find('span', class_ = '_reachbanner_').text # Извлекаем текст отзыва
            feedbacks_status_dict[author] = text # Добавляем в словарь автора и его отзыв
        feedbacks_dict[feedback_statuses[n]] = feedbacks_status_dict # Добавляем словарь отзывов с одним статусом в общий словарь
    with open(f'Interstellar{feedback_num}.json', 'w', encoding='utf-8') as file: # Сохраняем результат в JSON файл
        json.dump(feedbacks_dict, file, ensure_ascii=False, indent=4) # С адекватной поддержкой киррилицы и с отступами
