# -*- coding:utf-8 -*-

from db.redistools import RedisTools
from db.peeweetools import Cookies
import json
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
    data = json.dumps(data)
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
    return True


def get_cookie(url):
    """
    获取cookie返回cookie列表
    :param url:
    :return:
    """
    domain = tldextract.extract(url).domain
    key = 'cookies:{}'.format(domain)
    try:
        obj = Cookies.get(Cookies.domain == domain)
    except BaseException:
        return False
    obj.use_number += 1
    obj.save()
    data = RedisTools.get_set_all(key)
    return data


def cookie_setting(url, test_type=None, test_url=None, test_sign=None):
    """设置cookie的检验字段"""
    domain = tldextract.extract(url).domain
    try:
        obj = Cookies.get(Cookies.domain == domain)
    except BaseException:
        return False
    obj.test_type = test_type
    obj.test_url = test_url
    obj.test_sign = test_sign
    obj.save()


if __name__ == '__main__':
    pass

