from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.baidu.com')
        page.screenshot(path='cache/baidu.png')
        print(page.title())
        browser.close()


if __name__ == '__main__':
    main()
