# -*- coding:utf-8 -*-

from db.redistools import RedisTools


def put_redis(cookies):
    items = cookies.items()
    for item in items:
        domain, cookie_list = item
        RedisTools.insert_to_list_redis("cookies:{}".format(domain), cookie_list)


if __name__ == '__main__':
    put_redis()