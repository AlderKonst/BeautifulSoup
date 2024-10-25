import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from bs4 import BeautifulSoup

domain = 'http://dedmorozural.ru'
url = f'{domain}/novosti'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=6d22f1d5b66fa1539e3ee2df8b15c77d; InstantCMS[geodata]=a%3A7%3A%7Bs%3A7%3A%22inetnum%22%3Bs%3A27%3A%2246.158.0.0+-+46.159.255.255%22%3Bs%3A7%3A%22country%22%3Bs%3A2%3A%22RU%22%3Bs%3A4%3A%22city%22%3Bs%3A18%3A%22%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%22%3Bs%3A6%3A%22region%22%3Bs%3A35%3A%22%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D1%80%D0%B0%D0%B9%22%3Bs%3A8%3A%22district%22%3Bs%3A44%3A%22%D0%AE%D0%B6%D0%BD%D1%8B%D0%B9+%D1%84%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%BE%D0%BA%D1%80%D1%83%D0%B3%22%3Bs%3A3%3A%22lat%22%3Bs%3A9%3A%2245.042149%22%3Bs%3A3%3A%22lng%22%3Bs%3A9%3A%2238.980640%22%3B%7D; InstantCMS[logdate]=1577386070; InstantCMS[userid]=00cb7b95006f9aa9c861d9fc32fba967',
    'dnt': '1',
    'Host': 'dedmorozural.ru',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
# response = requests.get(url, auth=HTTPDigestAuth('DanteOnline', 'dywtbofywed'))

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

span = soup.find('span', class_='register')
print(span)

span = soup.find('span', class_='my_profile')
print(span)