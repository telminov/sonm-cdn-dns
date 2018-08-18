import os
import requests
import settings

# Чтобы получить ключ, нужно зарегаться на https://ipstack.com/
DATABASE_URL = 'http://api.ipstack.com'


def get_continent_code_from_ip(ip):
    url = os.path.join(DATABASE_URL, ip)
    response = requests.get(url, params={'access_key': settings.IP_STACK_ACCESS_KEY})
    response = response.json()
    continent_code = response['continent_code']

    return continent_code
