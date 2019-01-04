# -*- coding:utf-8 -*-
import browsercookie


def get_chrome_cookie():
    """
    需要将直接获取浏览器的cookie
    :return:dict
    """
    cookies = browsercookie.chrome()
    items = dict()
    for cookie in cookies:
        item = items.get(cookie.domain, [])
        item.append({'domain': cookie.domain, 'expiry': cookie.expires,
                     'path': cookie.path, 'name': cookie.name,
                     'secure': cookie.secure, 'value': cookie.value})
        items[cookie.domain] = item
    return items


def get_reque_session_cookie(response):
    """
    获取response/Session的cookie并转化
    :param response:
    :return: dict
    """
    cookies = response.cookies
    items = dict()
    for cookie in cookies:
        item = items.get(cookie.domain, [])
        item.append({'domain': cookie.domain, 'expiry': cookie.expires,
                     'path': cookie.path, 'name': cookie.name,
                     'secure': cookie.secure, 'value': cookie.value})
        items[cookie.domain] = item
    return items


def get_scrapy_cookie(response):
    """
    传入scrapy的response对象，其中的cookie
    :param test:
    :return:
    """
    cookies = response.headers.getlist('Set-Cookie')
    items = dict()
    for cookie in cookies:
        item = [(i.split('=')[0].lower().replace(' ', ''), i.split('=')[1]) for i
                in cookie.decode().split(';') if '=' in i]
        name, value = item.pop(0)
        item.append(("name", name))
        item.append(("value", value))
        item = dict(item)
        cookie_list = items.get(item['domain'], [])
        cookie_list.append(item)
        items[item['domain']] = cookie_list
    return items


if __name__ == '__main__':
    get_chrome_cookie()