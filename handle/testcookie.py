
import requests
from selenium import webdriver
from db.peeweetools import Cookies
from selenium.webdriver.chrome.options import Options
from setting import CHORME


def requests_test(url, sign, cookies):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36',
               'cookie': 1}
    response = requests.get(url, headers=headers)
    word = sign.split(';')
    for i in word:
        if i in response.text:
            return True
    return False


def selenium_test(url, sign, cookies):
    add_argument = CHORME['add_argument']
    chrome_options = Options()
    [chrome_options.add_argument(i) for i in add_argument]
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    word = sign.split(';')
    for i in word:
        if i in driver.page_source:
            return True
    return False


if __name__ == '__main__':
    selenium_test(1, 1, 1)


