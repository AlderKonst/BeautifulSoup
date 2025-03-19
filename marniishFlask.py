from flask import Flask, render_template, request
import json  # Импортируем библиотеку для работы с JSON-файлами
import requests  # Импортируем библиотеку для выполнения HTTP-запросов
app = Flask(__name__)
menu = {
    '/': 'Главная',
    '/contacts/': 'Контакты',
    '/form/': 'Форма поиска',
}
@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/contacts/')
def contacts():
    return render_template('contacts.html', menu=menu)

@app.route('/form/', methods=['GET'])
def form_get():
    return render_template('form.html', menu=menu)

@app.route('/form/', methods=['POST'])
def form_post():
    text = request.form['finding']

    with open('NIIparser.json', 'r', encoding='utf-8') as j:
        parser = json.load(j)  # Загружаем данные из JSON

        if text == 'menu':
            url_name = ['Меню сайта:']  # Заголовок меню
            for line in parser[0]['Меню сайта']:  # Проходим по элементам меню
                for url, name in line.items():  # Извлекаем URL и имя
                    if name == '':  # Если имя пустое, т.е. главная страница
                        url_name.extend(['Главная', f'Адрес сайта: {url}', ''])  # Добавляем ссылку с названием главной страницы
                    else:
                        url_name.extend([name, f'Адрес сайта: {url}', ''])  # Добавляем ссылку с названием пункта меню
            result = url_name

        elif text == 'trends':
            result = ['Основные направления деятельности института:'] + parser[1]['Направления деятельности']  # Формируем строку с направлениями деятельности

        elif text == 'links':
            url_name = ['Полезные ссылки на сайте:']  # Заголовок полезных ссылок
            for line in parser[2]['Полезные ссылки']:  # Проходим по полезным ссылкам
                for url, name in line.items():  # Извлекаем URL и название сайта
                    url_name.extend([name, f'Ссылка: {url}', ''])  # Добавляем ссылку с названием сайта
            result = url_name

        elif text == 'news':
            result = ['Новости текущего года:'] + parser[3]['Новости текущего года']  # Формируем строку с новостями текущего года

    return render_template('results.html', menu=menu, result=result)

if __name__ == "__main__":
    app.run(debug=True)