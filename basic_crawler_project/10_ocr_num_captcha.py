import logging

from PIL import Image
from playwright.sync_api import sync_playwright
from transformers import VisionEncoderDecoderModel, TrOCRProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    return browser


def get_page(browser):
    page = browser.new_page()
    page.goto('https://captcha7.scrape.center/')
    return page


def save_captcha_image(page):
    image_canvas = page.query_selector('.el-form .s-canvas>canvas')
    image = image_canvas.screenshot()
    with open('cache/captcha.png', 'wb') as f:
        f.write(image)
        logging.info('captcha image saved')


def recognize_captcha_image(retry=0):
    # Load model and processor
    processor = TrOCRProcessor.from_pretrained("anuashok/ocr-captcha-v3")
    model = VisionEncoderDecoderModel.from_pretrained("anuashok/ocr-captcha-v3")
    # Prepare image
    image = Image.open('./cache/captcha.png').convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # Generate text
    generated_ids = model.generate(pixel_values)
    captcha_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    logging.info('origin captcha text: %s', captcha_text)
    ## 去除特殊字符
    captcha_text = ''.join(filter(str.isalnum, captcha_text))
    if len(captcha_text) == 5:
        # 去除第一个字符
        captcha_text = captcha_text[1:]
    if not captcha_text or len(captcha_text) != 4:
        logging.info('captcha text length not equal to 4')
        raise ValueError('captcha text length not equal to 4')
    logging.info('processed captcha text: %s', captcha_text)
    return captcha_text


def user_login(page, captcha_code):
    logging.info('start to login')
    page.fill('.el-form .username>input[type="text"]', 'admin')
    page.fill('.el-form .password>input[type="password"]', 'admin')
    page.fill('.el-form .captcha>input[type="text"]', captcha_code)
    page.click('.el-form .login')
    page.wait_for_url('https://captcha7.scrape.center/success', timeout=10000)
    logging.info('login success')


def main():
    # 初始化浏览器
    browser = init_browser()
    page = get_page(browser)
    # 获取验证码图片
    save_captcha_image(page)
    # 处理并识别验证码
    captcha_code = recognize_captcha_image()
    # 执行登录操作
    user_login(page, captcha_code)
    browser.close()


if __name__ == '__main__':
    main()
