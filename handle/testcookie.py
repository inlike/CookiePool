
import requests
from selenium import webdriver
from db.peeweetools import Cookies
from selenium.webdriver.chrome.options import Options
from setting import CHORME


class TestCookie:
    def __init__(self):
        add_argument = CHORME['add_argument']
        chrome_options = Options()
        [chrome_options.add_argument(i) for i in add_argument]
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    @staticmethod
    def requests_test(url, sign, cookies):
        session = requests.Session()
        CookieJar = requests.utils.cookiejar_from_dict(
            {c['name']: c['value'] for c in cookies})
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/71.0.3578.98 Safari/537.36'}
        session.cookies = CookieJar
        response = session.get(url, headers=headers)
        word = sign.split(';')
        for i in word:
            if i in response.text:
                return True
        return False

    def selenium_test(self, url, sign, cookies):
        self.driver.get(url)
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            self.driver.refresh()
        word = sign.split(';')
        for i in word:
            if i in self.driver.page_source:
                return True
        return False

    def close(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    pass


