import requests
import logging
import re
import json
import multiprocessing
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

base_url = 'https://ssr1.scrape.center/'
TOTAL_PAGE = 10
RESULT_DIR = '1_requests_basic'


def scrape_page(url: str) -> str:
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page: int) -> str:
    index_url = f'{base_url}/page/{page}'
    return scrape_page(index_url)


def parse_index(html: str) -> list[str]:
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        logging.warning('no item found in page')
        return []
    return [urljoin(base_url, item) for item in items]


def scrape_detail(url: str) -> str:
    return scrape_page(url)


def parse_detail(html: str):
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    category_pattern = re.compile('<button.*?type="button".*?category.*?>.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('<span.*?>(\d{4}-\d{2}-\d{2})\s?上映</span>', re.S)
    drama_pattern = re.compile('<div.*?class="drama">.*?<h3.*?>剧情简介</h3>.*?<p.*?>(.*?)</p>.*?</div>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else ""
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else ""
    categories = re.findall(category_pattern, html) if re.search(category_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1).strip() if re.search(published_at_pattern,
                                                                                       html) else ""
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else ""
    score = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern, html) else None

    return {
        'name': name,
        'cover': cover,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def sanitize_filename(filename: str) -> str:
    """
    过滤文件名中的不支持字符。

    :param filename: 原始文件名
    :return: 过滤后的文件名
    """
    # 定义Windows和其他系统不支持的字符
    invalid_chars = r'[<>:"/\\|?*]'
    # 使用正则表达式替换无效字符为空字符串
    sanitized_filename = re.sub(invalid_chars, '', filename)
    return sanitized_filename


def save_data(data: dict):
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{sanitize_filename(name)}.json'
    logging.info('saving data to %s', data_path)
    with open(data_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def run(page: int):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    logging.info('detail urls %s', detail_urls)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('start saving data => %s', data.get('name'))
        save_data(data)
        logging.info('data saved')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(run, pages)
    pool.close()
    pool.join()
