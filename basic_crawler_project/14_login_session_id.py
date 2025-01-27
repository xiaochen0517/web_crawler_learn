import requests
from urllib.parse import urljoin

from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书验证警告（可选）
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = "https://login2.scrape.center/"
LOGIN_URL = urljoin(BASE_URL, "/login")

session = requests.Session()
login_response = session.post(LOGIN_URL, data={
    'username': 'admin',
    'password': 'admin'
}, verify=False)

print(f'login status: {login_response.status_code}')
print(f'cookies: {login_response.cookies}')

PAGE_URL = urljoin(BASE_URL, "/page/1")

page_response = session.get(PAGE_URL, verify=False)

print(f'page status: {page_response.status_code}')
print(f'page url is: {page_response.url}')
