
import json
import redis
from scrapy_redis import get_redis
from setting import REDIS_URL

redis_cli = get_redis(url=REDIS_URL)
# redis_cli = redis.StrictRedis(
#         host='127.0.0.1', port=6379)


class RedisTools:
    """实现了获取数据编码格式的自动转换"""

    @staticmethod
    def duplicate(key, data):
        """数据是否存在集合中"""
        v = redis_cli.sismember(key, data)
        if v:
            return True
        return False

    @staticmethod
    def insert_to_set_redis(key, *data):
        """存入集合"""
        redis_cli.sadd(key, *data)

    @staticmethod
    def get_set_pop(key):
        """随机弹出一条数据"""
        if not RedisTools.get_set_number(key):
            return None
        data = redis_cli.spop(key)
        try:
            return json.loads(data)
        except:
            return data.decode()

    @staticmethod
    def get_set_randome(key, n=1):
        """
        随机返回集合指定数目元素
        :param key:
        :param n:
        :return: list
        """
        if not RedisTools.get_set_number(key):
            return None
        data = redis_cli.srandmember(key, n)
        try:
            return json.loads(data)
        except:
            return data.decode()

    @staticmethod
    def get_set_number(key):
        num = redis_cli.scard(key)
        return num

    @staticmethod
    def get_set_all(key):
        """
        返回指定集合中所有元素
        :param key:
        :return:list
        """
        if not RedisTools.get_set_number(key):
            return None
        data = redis_cli.smembers(key)
        data = list(data)
        data = [json.loads(item.decode()) for item in data]
        return data

    @staticmethod
    def delete_set(key, *data):
        """
        删除集合中数据
        :param key:
        :param data:
        :return:
        """
        n = redis_cli.srem(key, *data)
        return n

    @staticmethod
    def del_key(key):
        redis_cli.delete(key)

    @staticmethod
    def insert_to_list_redis(key, data):
        """存入列表"""
        redis_cli.lpush(key, data)

    @staticmethod
    def get_list_pop(key):
        """获取一条并删除列表中元素"""
        if not RedisTools.get_list_number(key):
            return None

        data = redis_cli.lpop(key)
        try:
            return json.loads(data)
        except:
            return data.decode()

    @staticmethod
    def get_list_number(key):
        """获取列表中元素总数"""
        num = redis_cli.llen(key)
        return num

    @staticmethod
    def message_queue(type_mode, key, vaule=None):
        """实现消息队列"""
        if type_mode == 'put':
            redis_cli.lpush(key, vaule)
        else:
            message = redis_cli.rpop(key)
            try:
                return json.loads(message)
            except:
                return message.decode()


if __name__ == '__main__':

    RedisTools.insert_to_set_redis('test', '测试集合')
    RedisTools.get_set_pop('test')