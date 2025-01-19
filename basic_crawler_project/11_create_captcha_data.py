from captcha.image import ImageCaptcha
from PIL import Image
import random

MAX_CAPTCHA_LENGTH = 4

NUMBERS = [str(i) for i in range(10)]
UPPER_CASE_LETTERS = [chr(i) for i in range(65, 91)]
LOWER_CASE_LETTERS = [chr(i) for i in range(97, 123)]
ALL_CHARACTERS = NUMBERS + UPPER_CASE_LETTERS + LOWER_CASE_LETTERS
print(len(ALL_CHARACTERS))

def generate_captcha_text():
    captcha_text = []
    for i in range(MAX_CAPTCHA_LENGTH):
        captcha_text.append(random.choice(ALL_CHARACTERS))
    return ''.join(captcha_text)


def generate_captcha_text_and_image():
    image = ImageCaptcha()
    captcha_text = generate_captcha_text()
    captcha = image.generate(captcha_text)
    captcha_image = Image.open(captcha)
    return captcha_text, captcha_image


def save_captcha_text_and_image(train_set=True, captcha_text="", captcha_image=None):
    if train_set:
        captcha_image.save(f'./captcha_images/train/{captcha_text}.png')
    else:
        captcha_image.save(f'./captcha_images/validation/{captcha_text}.png')


def main():
    for i in range(3000):
        [captcha_text, captcha_image] = generate_captcha_text_and_image()
        save_captcha_text_and_image(False, captcha_text, captcha_image)


if __name__ == '__main__':
    # main()
    pass
