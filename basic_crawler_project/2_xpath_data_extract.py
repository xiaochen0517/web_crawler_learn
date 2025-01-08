from lxml import etree
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

base_url = 'https://ssr1.scrape.center/detail/1'


def get_page():
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text
    logging.error('get invalid status code %s while scraping %s', response.status_code, base_url)


if __name__ == '__main__':
    html_str = get_page()
    html = etree.HTML(html_str)
    movie_name = html.xpath('//div[@id="app"]/div[@id="detail"]//div[contains(@class, "el-card")][1]//a/h2')[0].text
    print(movie_name)
