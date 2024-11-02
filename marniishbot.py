import telebot
import os

TOKEN = '8084928104:AAGQ0JIApYW_yGYVYxmWTGBPpIW642zMMqQ'
bot = telebot.TeleBot(TOKEN)
readme = 'README.md'

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Приветствую Вас!\nЭто бот официального сайта Марийского НИИСХ –\nфилиала ФГБНУ ФАНЦ Северо-Востока')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, f'{url_readme}')

bot.infinity_polling()

# Обработка команд c параметром
@bot.message_handler(commands=['say'])
def say(message):
	# Получить то, что после команды
	text = ' '.join(message.text.split(' ')[1:])
	bot.reply_to(message, f'{text.upper()}! А ну, пошёл! Гад!')

# Например, вот, передача файлов
@bot.message_handler(commands=['file'])
def photo(message):
	with open('1.jpg', 'rb') as data:
		bot.send_photo(message.chat.id, data)

@bot.message_handler(content_types=['text'])
def reverse_text(message):
	if 'пчий' in message.text.lower():
		bot.reply_to(message, 'В тексте есть пчи')
		return

# Если нужно аудио, видео, изображение или что-то другое, то меняем соответствующие content_types и send_sticker
@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
	FILE_ID = 'CAACAgIAAxkBAANbZyT6Or116v5ToHcbIdGDXAFJzC8AAloAA8A2TxML_A9P3EYZ4TYE'
	bot.send_sticker(message.chat.id, FILE_ID)

bot.infinity_polling()
