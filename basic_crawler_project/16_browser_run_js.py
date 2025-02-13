import os

import requests
import json
from playwright.sync_api import sync_playwright

BASE_URL = 'https://spa2.scrape.center'
INDEX_URL = BASE_URL + '/api/movie?limit=10&offset={offset}&token={token}'
MAX_PAGE = 5

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # 获取本地JS文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    replace_js_path = os.path.join(current_dir, 'data/16_browser_run_js/replace_chunk.js')

    if not os.path.exists(replace_js_path):
        raise FileNotFoundError(f"替换文件不存在: {replace_js_path}")

    page.route(
        'https://spa2.scrape.center/js/chunk-10192a00.243cb8b7.js',
        lambda route: (
            print('replace_chunk.js'),
            route.fulfill(path=replace_js_path)
        )
    )

    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")  # 等待页面完全加载


    def get_token(page, ofs):
        run_js = '''() => {
            return window.gen_token_func("%s", "%s")
        }''' % ('/api/movie', ofs)
        result = page.evaluate(run_js)
        return result


    for i in range(MAX_PAGE):
        offset = i * 10
        token = get_token(page, offset)
        index_url = INDEX_URL.format(offset=offset, token=token)
        response = requests.get(index_url)
        # 格式化展示 response.json() 的内容，将 json 缩进 2 个空格
        print(f'第 {i + 1} 页数据: \n{json.dumps(response.json(), indent=2, ensure_ascii=False)}')

    browser.close()
