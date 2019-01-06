# -*- coding:utf-8 -*-

from db.redistools import RedisTools
from db.peeweetools import Cookies
import tldextract


def put_cookie(url, data):
    """
    存放cookie调用的接口
    :param domain: 网站url
    :param data: cookie列表
    :return: None
    """
    domain = tldextract.extract(url).domain
    key = 'cookies:{}'.format(domain)
    RedisTools.insert_to_set_redis(key, data)
    try:
        obj = Cookies.get(Cookies.domain == domain)
    except BaseException:
        obj = None
    if not obj:
        obj = Cookies()
        obj.domain = domain
    obj.count = RedisTools.get_set_number(key)
    obj.save()


def get_cookie(url):
    domain = tldextract.extract(url).domain
    key = 'cookies:{}'.format(domain)
    try:
        obj = Cookies.get(Cookies.domain == domain)
    except BaseException:
        return False
    obj.use_number += 1
    obj.save()
    data = RedisTools.g


if __name__ == '__main__':
    pass