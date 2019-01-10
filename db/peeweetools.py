from peewee import *
from playhouse.pool import PooledSqliteDatabase
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime

"""peewee提供了一个数据库的封装模型，playhouse.db_url为其连接的一种方式通过数据库的指定格式url连接
连接后创建完以后需要模型生成表使用db.connect()，db.create_tables([Person, Pet])"""

blog = PooledSqliteDatabase('static/cookies.db')


class BaseModel(Model):
    """基类"""
    class Meta:
        database = blog


class Cookies(BaseModel):

    domain = CharField(verbose_name='域名', max_length=20, null=False, unique=True)
    count = IntegerField(verbose_name='记录条数', null=False)
    use_number = IntegerField(verbose_name='使用次数', default=0)
    test_type = CharField(verbose_name='检测方式', max_length=10, null=True, unique=False)
    test_url = CharField(verbose_name='检测地址', max_length=100, null=True, unique=True)
    test_sign = CharField(verbose_name='有效标示', max_length=100, null=True, unique=False)
    testing_date = DateTimeField(verbose_name='写入时间', default=datetime.datetime.now)
    insert_date = DateTimeField(verbose_name='写入时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
    is_delete = BooleanField(verbose_name='删除', default=False, null=False)

    def to_dict(self):
        objs = Cookies().select()
        data = [model_to_dict(i) for i in objs]
        return data


def create_tables():
    """生成数据表"""
    blog.connect()
    blog.create_tables([Cookies])
    blog.close()


if __name__ == '__main__':
    create_tables()
# if __name__ == '__main__':
#
#     class Test(BaseModel):
#         """参数解释
#         CharField：字符串类型
#         IntegerField：整型
#         DateTimeField：时间类型
#         ForeignKeyField：外键关联
#         unique：是否唯一
#         max_lenth:最大长度
#         verbose_name:表头名
#         null：是都为空
#         default：默认值"""
#
#         name = CharField(unique=True, max_length=50, verbose_name='用户名', null=False, default='你哈')
#         number = IntegerField(default=0, verbose_name='数字')
#         update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
#
#
#     class Tests(BaseModel):
#         title = CharField(verbose_name='标题', max_length=64)
#         site = CharField(verbose_name='前缀', max_length=32, unique=True)
#         article_type = ForeignKeyField(Test)
#
#
    # def create_tables():
    #     """生成数据表"""
    #     blog.connect()
    #     blog.create_tables([Tests, Test])
    #     blog.close()

#
#     def drop_tables():
#         """删除数据表"""
#         blog.connect()
#         blog.drop_tables([Tests, Test])
#         blog.close()
#
#
#     def insert(value):
#         """插入数据,或者将属性作为参数传入Test（name='name',number=2222）"""
#         obj = Test()
#         obj.name = value
#         obj.number = 99
#         obj.save()
#
#
#     def updata():
#         """"更新数据"""
#         obj = Test.get(Test.name == '更新')
#         obj.name = '更新完毕'
#         obj.number = 100
#         obj.save()
#
#
#     def select_all():
#         """查询所有数据"""
#         ret = Test.select()
#         for obj in ret:
#             print(obj.name)
#
#
#     def select_test():
#         """查询条件数据"""
#         Test.select().where((Test.name.contains('测试'))) .count()    # 包含指定内容返回集合
#         Test.select().where((Test.name == '测试') | (Test.number == 9999)).first()    # 条件或
#         Test.select().where((Test.name == '测试'), (Test.number == 9999)).first()    # 条件并
#         Test.select().join(Tests).where(Tests.title == 'title').execute()   # 关联查询
#
#         obj = Test.get(Test.name == 'yang')
#         if obj:
#             print(obj.name)
#         else:
#             print('none have')
#
#
#     def delete_a(i):
#         """删除数据"""
#         obj = Test.get(Test.id == i)
#         obj.delete_instance()
#
#
#     def sort():
#         """对返回结果列排序"""
#         set = Test.select().order_by(Test.name)
#
#
#     def to_dict():
#         """把模型数据转为字典对象"""
#         user = Test.create(username='jack')
#         u = model_to_dict(user)
#         return u
#
#
#     def to_model():
#         """生成model对象"""
#         user_data = {'id': 2, 'username': 'charlie'}
#         user = dict_to_model(Test, user_data)
#
#
