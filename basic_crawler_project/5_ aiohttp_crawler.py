import asyncio
import aiohttp
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

"""
async http client
"""
CONCURRENCY_LIMIT = 5

INDEX_URL = 'https://spa5.scrape.center/api/book/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{book_id}/'

PAGE_SIZE = 10
PAGE_NUMBER = 20

semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
session = None


async def scrape_api(url: str):
    async with semaphore:
        try:
            logging.info('scraping %s...', url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)


"""
MongoDB Config
"""
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_CONNECTION_STRING = 'mongodb://admin:123456@localhost:27017'
MONGO_DB_NAME = 'aiohttp_books'
MONGO_COLLECTION_NAME = 'aiohttp_books'

mongo_client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


async def save_data(data: dict):
    if data:
        logging.info('saving data %s', data)
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


async def scrape_index(page: int):
    """
    get books index
    """
    url = INDEX_URL.format(limit=PAGE_SIZE, offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


async def scrape_detail(book_id: int):
    """
    get book detail
    """
    url = DETAIL_URL.format(book_id=book_id)
    detail_data = await scrape_api(url)
    await save_data(detail_data)
    return detail_data


async def run():
    global session
    try:
        session = aiohttp.ClientSession()
        """
        获取图书列表
        """
        tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
        results = await asyncio.gather(*tasks)
        """
        提取图书的id
        """
        book_ids = []
        for index_data in results:
            if not index_data:
                continue
            logging.info('index data %s', json.dumps(index_data, ensure_ascii=False))
            for item in index_data.get('results', []):
                book_id = item.get('id')
                if not book_id: continue
                book_ids.append(book_id)
        logging.info('book ids count %s', len(book_ids))
        """
        获取图书详情
        """
        tasks = [asyncio.ensure_future(scrape_detail(book_id)) for book_id in book_ids]
        detail_results = await asyncio.gather(*tasks)
        logging.info('detail results %s', detail_results)
    finally:
        if session:
            await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
