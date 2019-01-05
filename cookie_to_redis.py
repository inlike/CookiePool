# -*- coding:utf-8 -*-

from db.redistools import RedisTools


def put_redis(key, data):
    RedisTools.insert_to_list_redis("cookies:{}".format(key), data)


if __name__ == '__main__':
    put_redis()