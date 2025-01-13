import logging

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    driver = uc.Chrome(headless=True, use_subprocess=False)
    try:
        driver.get('https://weibo.com/hot/mine')
        # 等待页面加载完成
        driver.implicitly_wait(2)
        # 获取有一个 class 开头为 HotTopic_item_ 的 div 元素
        elements = driver.find_elements(by=By.CSS_SELECTOR, value='[class^="HotTopic_item_"]')
        logging.info('elements size %s', len(elements))
        for element in elements:
            # 如果在 element 中获取到了 HotTopic_doticon_ 开头的 class 则直接跳过
            if element.find_elements(by=By.CSS_SELECTOR, value='[class^="HotTopic_doticon_"]'):
                continue
            # 获取 element 中的文本内容
            a_element = element.find_element(by=By.CSS_SELECTOR, value='a[class^="ALink_default_"]')
            logging.info('a_element %s', a_element.text)
    finally:
        driver.close()


if __name__ == '__main__':
    main()
