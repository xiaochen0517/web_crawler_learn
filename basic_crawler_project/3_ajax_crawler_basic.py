import requests
import json
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

base_url = 'https://spa1.scrape.center/'


def scrape_movie_list(page: int) -> dict:
    logging.info('scraping %s...', page)
    try:
        list_url = urljoin(base_url, f'/api/movie/?limit=10&offset={10 * (page - 1)}')
        response = requests.get(list_url)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, page)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', page, exc_info=True)


def scrape_movie_count() -> int:
    try:
        count_url = urljoin(base_url, '/api/movie/?limit=1&offset=0')
        response = requests.get(count_url)
        if response.status_code == 200:
            return response.json()['count']
        logging.error('get invalid status code %s while scraping count', response.status_code)
    except requests.RequestException:
        logging.error('error occurred while scraping count', exc_info=True)


def scrape_movie_detail(movie_id: int) -> dict:
    logging.info('scraping %s...', movie_id)
    try:
        detail_url = urljoin(base_url, f'/api/movie/{movie_id}/')
        response = requests.get(detail_url)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, movie_id)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', movie_id, exc_info=True)


if __name__ == '__main__':
    total_page = scrape_movie_count() // 10
    for page in range(1, total_page + 1):
        movie_list_result = scrape_movie_list(page)
        for movie in movie_list_result.get("results"):
            movie_id = movie['id']
            movie_detail = scrape_movie_detail(movie_id)
            logging.info('movie detail %s', movie_detail)
