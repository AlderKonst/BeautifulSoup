import requests  # Импортируем библиотеку requests для работы с HTTP-запросами
from pprint import pprint  # Импортируем pprint для удобного форматирования вывода
import json  # Импортируем json для работы с JSON-данными (почему-то серым отображает)
from sqlalchemy import (Column, # Из SQLAlchemy импортируем колонки
                        Integer, # Из SQLAlchemy импортируем тип Integer
                        String, # Из SQLAlchemy импортируем тип String
                        create_engine, # Из SQLAlchemy импортируем метода создания БД
                        ForeignKey)  # Из SQLAlchemy импортируем метода указания внешних идентификаторов
from sqlalchemy.orm import (declarative_base, # Для декларативного создания таблицы
                            sessionmaker) # Импортируем метод создания сессий

with open('F:/UII/Token_vk.txt','r') as t: # Открываем файл с токеном
    token = t.read() # И записываем в переменную
token = (token)  # Токен доступа к API ВКонтакте
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

engine = create_engine('sqlite:///vk_orm.sqlite', echo=False) # Создаём и подключаемся к БД с выключенными инфами
Base = declarative_base() # Создаём класс Base из внутреннего метакласса в SQLAlchemy, где в конфигурацию включён наш БД

class FirstName(Base): # Класс для хранения имен
    __tablename__ = 'first_name' # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True, autoincrement=True) # Уникальный идентификатор
    name = Column(String(15), unique=True) # Имя, уникальное в пределах таблицы
    def __init__(self, name): # Конструктор класса
        self.name = name # Инициализация имени
    def __str__(self): # Метод для строкового представления объекта
        return f'{self.id}\t{self.name}' # Возвращает id и имя

class UniversityName(Base): # Класс для хранения названий университетов
    __tablename__ = 'university_name' # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True) # Уникальный идентификатор
    name = Column(String(35), unique=True) # Название университета, уникальное в пределах таблицы
    def __init__(self, id, name): # Конструктор класса
        self.id = id # Инициализация номера универа
        self.name = name # Инициализация названия университета
    def __str__(self): # Метод для строкового представления объекта
        return f'{self.id}\t{self.name}' # Возвращает id и название университета

class SvechaYoshka(Base): # Класс для хранения информации о Свечниковых в Йошке
    __tablename__ = 'svecha_yoshka' # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True) # Уникальный идентификатор
    first_name_id = Column(Integer, ForeignKey('first_name.id')) # Идентификатор имени (ссылка на FirstName)
    university_id = Column(Integer, ForeignKey('university_name.id')) # Идентификатор университета (ссылка на UniversityName)
    def __init__(self, id, first_name_id, university_id): # Конструктор класса
        self.id = id  # Инициализация номера пользователя
        self.first_name_id = first_name_id # Инициализация идентификатора имени
        self.university_id = university_id  # Инициализация идентификатора универа

Base.metadata.create_all(engine) # Вот и создаём все эти 3 таблицы

Session = sessionmaker(bind=engine) # Сперва создаём класс сессии с параметрами
session = Session() # Потом уже саму сессию

for user in result['response']['items']: # Обрабатываем результаты запроса к API VK по каждому найденному пользователю
    # Добавляем или получаем существующее имя
    first_name = session.query(FirstName).filter_by(name=user['first_name']).first() # Ищем имя в БД
    if not first_name: # Для избежания дублирования
        first_name = FirstName(name=user['first_name']) # Создаем новый объект FirstName
        session.merge(first_name) # Добавляем или обновляем объект в сессии
        session.flush()  # Чтобы получить id для нового объекта

    # Добавляем или получаем существующий университет
    university = session.query(UniversityName).filter_by(id=user['university']).first() # Ищем университет в БД
    if not university: # Для избежания дублирования
        university = UniversityName(id=user['university'], # Тут id из API.json
                                    name=user['university_name']) # Создаем новый объект UniversityName
        session.merge(university) # Добавляем или обновляем объект в сессии

    # Добавляем запись в таблицу SvechaYoshka
    svecha_yoshka = SvechaYoshka(id=user['id'], # Тут id из API.json
                                 first_name_id=first_name.id, # ID из объекта FirstName
                                 university_id=user['university'] # Тут id из API.json
    )
    session.merge(svecha_yoshka) # Добавляем или обновляем объект в сессии

session.commit() # Сохраняем все изменения в базе данных

query = ( # Итак, параметры запроса, слишком похожий на запрос на SQLite
    session.query( # Начинаем построение запроса
        SvechaYoshka.id, # Выбираем id из таблицы SvechaYoshka
        FirstName.name, # Выбираем имя из таблицы FirstName
        UniversityName.name # Выбираем название университета из таблицы UniversityName
    )
    .join(FirstName, # Присоединяем таблицу FirstName
          SvechaYoshka.first_name_id == FirstName.id) # Условие присоединения по id
    .join(UniversityName, # Присоединяем таблицу UniversityName
          SvechaYoshka.university_id == UniversityName.id) # Условие присоединения по id
)
results = query.all() # Выполняем запрос и получаем все результаты в виде списка кортежей
pprint(results) # Выводим результаты в удобочитаемом формате