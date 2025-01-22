from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

proxy = config['PROXY_SERVER']['server_url']

proxy_handler = ProxyHandler({
    'http': proxy,
    'https': proxy
})

opener = build_opener(proxy_handler)

try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
