import requests
from pprint import pprint
import json
token = 'vk1.a.yxxhoAU0X_NN86KDgr58ONhwvxX0TY4KPBM2Ut07EUKbsRlrW_db4PjxJNK2PcEMe0V2QvXgXLk0SD36rBFcBzvg0R-FQhxCnv-xn_wC93frumLrJy8_LEoZngLo0G_Bo4L_yr22z7rfQMmXm9f3X7_bvG914Ho25oHv-R3jkrq2vVHTM02I9ohTVK4lU1QbldY0LdFkgJ1MiZfY9Gnqww'
method = 'users.search'
url = f'https://api.vk.com/method/{method}'
params = {
    'access_token': token,
    'q': 'Свечников',
    'v': '5.199',
    'hometown': ['Йошкар-Ола'],
    'fields': 'education, home_town'
}
result = requests.get(url, params=params)
result.encoding = 'UTF-8'
pprint(result.json())