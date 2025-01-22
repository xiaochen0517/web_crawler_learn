import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

proxy = config['PROXY_SERVER']['server_url']

proxys = {
    'http': proxy,
    'https': proxy
}

try:
    response = requests.get('http://httpbin.org/get', proxies=proxys)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(e)
