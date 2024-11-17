from flask import Flask, render_template, request  # Импортируем необходимые модули Flask
import json  # Импортируем библиотеку для работы с JSON-файлами
import requests  # Импортируем библиотеку для выполнения HTTP-запросов

app = Flask(__name__)  # Создаем экземпляр приложения Flask

menu = {  # Определяем меню сайта
    '/': 'Главная',  # Главная страница
    '/contacts/': 'Контакты',  # Страница контактов
    '/form/': 'Форма поиска',  # Страница формы поиска
}

@app.route('/')  # Декоратор для главной страницы
def index():
    return render_template('index.html', menu=menu)  # Отправляем шаблон главной страницы с меню

@app.route('/contacts/')  # Декоратор для страницы контактов
def contacts():
    return render_template('contacts.html', menu=menu)  # Отправляем шаблон страницы контактов с меню

@app.route('/form/', methods=['GET'])  # Декоратор для формы поиска (GET)
def form_get():
    return render_template('form.html', menu=menu)  # Отправляем шаблон формы поиска с меню

@app.route('/form/', methods=['POST'])  # Декоратор для обработки формы поиска (POST)
def form_post():
    text = request.form['finding']  # Получаем текст из формы

    with open('NIIparser.json', 'r', encoding='utf-8') as j:  # Открываем JSON файл для чтения
        parser = json.load(j)  # Загружаем данные из JSON

        if text == 'menu':  # Если введен запрос на меню
            url_name = ['Меню сайта:']  # Заголовок меню
            for line in parser[0]['Меню сайта']:  # Проходим по элементам меню
                for url, name in line.items():  # Извлекаем URL и имя
                    if name == '':  # Если имя пустое, т.е. главная страница
                        url_name.extend(['Главная', f'Адрес сайта: {url}', ''])  # Добавляем ссылку с названием главной страницы
                    else:
                        url_name.extend([name, f'Адрес сайта: {url}', ''])  # Добавляем ссылку с названием пункта меню
            result = url_name  # Сохраняем результат

        elif text == 'trends':  # Если введен запрос на тренды
            result = ['Основные направления деятельности института:'] + parser[1]['Направления деятельности']  # Формируем строку с направлениями деятельности

        elif text == 'links':  # Если введен запрос на полезные ссылки
            url_name = ['Полезные ссылки на сайте:']  # Заголовок полезных ссылок
            for line in parser[2]['Полезные ссылки']:  # Проходим по полезным ссылкам
                for url, name in line.items():  # Извлекаем URL и название сайта
                    url_name.extend([name, f'Ссылка: {url}', ''])  # Добавляем ссылку с названием сайта
            result = url_name  # Сохраняем результат

        elif text == 'news':  # Если введен запрос на новости
            result = ['Новости текущего года:'] + parser[3]['Новости текущего года']  # Формируем строку с новостями текущего года

    return render_template('results.html', menu=menu, result=result)  # Отправляем результаты в шаблон

if __name__ == "__main__":  # Проверяем, запущен ли скрипт напрямую
    app.run(debug=True)  # Запускаем приложение в режиме отладки