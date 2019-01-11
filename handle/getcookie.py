# -*- coding:utf-8 -*-
import browsercookie
import tldextract

"""
统一cookie数据格式:[{},{}]
"""


def get_chrome_cookie(websize):
    """
    需要将直接获取浏览器的cookie
    :return:dict
    """
    domain = '.{}.{}'.format(tldextract.extract(websize).domain, tldextract.extract(websize).suffix)
    cookies = browsercookie.chrome()
    items = dict()
    for cookie in cookies:
        item = items.get(cookie.domain, [])
        item.append({'domain': cookie.domain, 'expiry': cookie.expires,
                     'path': cookie.path, 'name': cookie.name,
                     'secure': cookie.secure, 'value': cookie.value})
        items[cookie.domain] = item
    data = items.get(domain, [])
    if not data:
        return False
    return data


def get_reque_session_cookie(response):
    """
    获取response/Session的cookie并转化
    :param response:
    :return: dict
    """
    cookies = response.cookies
    items = []
    for cookie in cookies:
        items.append({'domain': cookie.domain, 'expiry': cookie.expires,
                     'path': cookie.path, 'name': cookie.name,
                     'secure': cookie.secure, 'value': cookie.value})
    if not items:
        return False
    return items


def get_scrapy_cookie(response):
    """
    传入scrapy的response对象，其中的cookie
    :param test:
    :return:
    """
    cookies = response.headers.getlist('Set-Cookie')
    items = []
    for cookie in cookies:
        item = [(i.split('=')[0].lower().replace(' ', ''), i.split('=')[1]) for i
                in cookie.decode().split(';') if '=' in i]
        name, value = item.pop(0)
        item.append(("name", name))
        item.append(("value", value))
        item = dict(item)
        items.append(item)
    if not items:
        return False
    return items


def get_text_cookie(websize, text):
    """
    传入抓包获得的cookie字符串，解析成webdriver.cookie格式
    :param websize:
    :param text:
    :return:
    """
    domain = '.{}.{}'.format(tldextract.extract(websize).domain, tldextract.extract(websize).suffix)
    items = [(i.split('=')[0].replace(' ', ''), i.split('=')[1]) for i in text.split(';') if '=' in i]
    items = [{'domain': domain,
              'name': i[0],
              'value': i[1],
              'path': '/',
              'expiry':'',
              'secure': '',
              } for i in items]
    if not items:
        return False
    return items


if __name__ == '__main__':
    get_chrome_cookie()