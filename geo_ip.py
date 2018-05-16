import os
import requests

# Чтобы получить ключ, нужно зарегаться на https://ipstack.com/
ACCESS_KEY = 'd6b7f0fbe5b6e72d5b534b4989206cda'
DATABASE_URL = 'http://api.ipstack.com'


def get_continent_code_from_ip(ip):
    url = os.path.join(DATABASE_URL, ip)
    response = requests.get(url, params={'access_key': ACCESS_KEY})
    response = response.json()
    continent_code = response['code_continent']

    return continent_code
