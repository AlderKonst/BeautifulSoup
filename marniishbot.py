import telebot  # Импортируем библиотеку для работы с Telegram Bot API
import json  # Импортируем библиотеку для работы с JSON-файлами
import requests  # Импортируем библиотеку для выполнения HTTP-запросов

TOKEN = '8113926683:AAGBpCiXQsV_zkzcB-CHTB1ba0T32Ix9PcE'  # Токен для доступа к боту
bot = telebot.TeleBot(TOKEN)  # Создаем объект бота
readme_url = 'README.md'  # Путь к файлу README
parser_json_url = 'NIIparser.json'  # Путь к JSON-файлу с данными

@bot.message_handler(commands=['start'])  # Обработчик команды /start
def send_welcome(message):
	bot.reply_to(message, 'Приветствую Вас!\nЭто бот официального сайта Марийского НИИСХ –\nфилиала ФГБНУ ФАНЦ Северо-Востока')

@bot.message_handler(commands=['help'])  # Обработчик команды /help
def get_help(message):
	with open(readme_url, 'r', encoding='utf-8') as readme:  # Открываем файл README
		content = readme.read()  # Читаем содержимое файла
		bot.reply_to(message, content)  # Отправляем содержимое пользователю

@bot.message_handler(commands=['menu'])  # Обработчик команды /menu
def get_menu(message):
	with open(parser_json_url, 'r', encoding='utf-8') as parser_json:  # Открываем JSON-файл
		parser = json.load(parser_json)  # Загружаем данные из JSON
		url_name = ['Меню сайта:']  # Заголовок меню
		for line in parser[0]['Меню сайта']:  # Проходим по элементам меню
			for url, name in line.items():  # Извлекаем URL и имя
				if name == '':  # Если имя пустое, т.е. главная страница
					url_name.append(f'Главная\nАдрес сайта:\n{url}')  # Добавляем ссылку с названием главной страницы
				else:
					url_name.append(f'{name}\nАдрес сайта:\n{url}')  # Добавляем ссылку с названием пункта меню
		bot.reply_to(message, '\n\n'.join(url_name))  # Отправляем список ссылок пользователю

@bot.message_handler(commands=['href'])  # Обработчик команды /href
def get_menu(message):
	with open(parser_json_url, 'r', encoding='utf-8') as parser_json:  # Открываем JSON-файл
		parser = json.load(parser_json)  # Загружаем данные из JSON
		url_name = ['Полезные ссылки на сайте:']  # Заголовок полезных ссылок
		for line in parser[2]['Полезные ссылки']:  # Проходим по полезным ссылкам
			for url, name in line.items():  # Извлекаем URL и название сайта
				url_name.append(f'{name}\nСсылка:\n{url}')  # Добавляем ссылку с названием сайта
		bot.reply_to(message, '\n\n'.join(url_name))  # Отправляем список полезных ссылок пользователю

@bot.message_handler(commands=['trend'])  # Обработчик команды /trend
def get_menu(message):
	with open(parser_json_url, 'r', encoding='utf-8') as parser_json:  # Открываем JSON-файл
		parser = json.load(parser_json)  # Загружаем данные из JSON
		activity = 'Основные направления деятельности института:\n' + '\n\n'.join(parser[1]['Направления деятельности'])  # Формируем строку с направлениями деятельности
		bot.reply_to(message, activity)  # Отправляем информацию о направлениях пользователю

@bot.message_handler(commands=['news'])  # Обработчик команды /news
def get_menu(message):
	with open(parser_json_url, 'r', encoding='utf-8') as parser_json:  # Открываем JSON-файл
		parser = json.load(parser_json)  # Загружаем данные из JSON
		news = 'Новости текущего года:\n' + '\n\n'.join(parser[3]['Новости текущего года'])  # Формируем строку с новостями текущего года
		bot.reply_to(message, news)  # Отправляем новости пользователю

@bot.message_handler(commands=['expo'])  # Обработчик команды /expo
def expo(message):
	img_url = 'http://марниисх.рф/img/Expo.jpg'  # URL изображения со стендом НИИ для отправки
	img = requests.get(img_url, verify=False)  # Получаем изображение по URL (без проверки сертификата)
	bot.send_photo(message.chat.id, img.content)  # Отправляем изображение в чат

bot.infinity_polling()  # Запускаем бесконечный опрос для обработки сообщений бота