
import requests
from selenium import webdriver
from db.peeweetools import Cookies


def requests_test(url, sign):
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


