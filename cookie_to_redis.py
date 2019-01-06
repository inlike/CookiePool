# -*- coding:utf-8 -*-

from db.redistools import RedisTools
from db.peeweetools import Cookies
import tldextract


def put_cookie(domain, data):
    domain = tldextract.extract(domain).domain
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


if __name__ == '__main__':
    pass