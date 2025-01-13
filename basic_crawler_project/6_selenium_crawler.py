import undetected_chromedriver as uc

if __name__ == '__main__':
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.get('https://antispider1.scrape.center/')
    input("Press Enter to continue...")
