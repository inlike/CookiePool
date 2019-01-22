# coding:utf-8

import tornado.web
import tornado.ioloop
import json
import time
import datetime
import random
from db.peeweetools import Cookies
from handle.getcookie import *
from handle.Interface import get_cookie, put_cookie, cookie_setting
from handle.testcookie import TestCookie
from tornado.websocket import WebSocketHandler


class Random(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url', None)
        if not url:
            self.render('None')
        lists = get_cookie(url)
        self.set_header('Content-Type', 'text/json')
        self.write(json.dumps(random.choice(lists)))


class All(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url', None)
        if not url:
            self.render('None')
        lists = get_cookie(url)
        self.set_header('Content-Type', 'text/json')
        self.write(json.dumps(lists))


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        item = Cookies()
        items = item.to_dict()
        self.render("index.html", data=items)

    def post(self):
        post_data = dict()
        for key in self.request.arguments:
            post_data[key] = self.get_argument(key)
        print(post_data)
        operation = post_data.get("button", None)
        if operation == 'save':
            if post_data['test_type'] == 'None' or post_data['test_url'] \
                    == 'None' or post_data['test_sign'] == 'None':
                self.write(
                    '<script language="javascript"> alert("有未填项不能更新");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            obj = Cookies().get(domain=post_data['domain'])
            obj.test_type = post_data['test_type']
            obj.test_url = post_data['test_url']
            obj.test_sign = post_data['test_sign']
            obj.save()
            self.write(
                '<script language="javascript"> alert("更新成功"); </script>')
            return self.write("<script>location.href='/';</script>")
        elif operation == 'del':
            obj = Cookies().get(domain=post_data['domain'])
            obj.delete_instance()
            RedisTools.del_key('cookies:{}'.format(post_data['domain']))
            self.write(
                '<script language="javascript"> alert("{}删除成功"); </script>'.format(obj.domain))
            return self.write("<script>location.href='/';</script>")
        elif operation == 'analysis_cookie':
            text = self.get_argument('cookie_text', None)
            url = self.get_argument('cookie_url', None)
            if not text or not url:
                self.write(
                    '<script language="javascript"> alert("提交内容为空不能解析");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            data = get_text_cookie(url, text)
            feedback = put_cookie(url, data)
            if feedback:
                self.write(
                    '<script language="javascript"> alert("解析域名成功"); </script>')
                return self.write("<script>location.href='/';</script>")
        elif operation == 'chrome_cookie':
            url = self.get_argument('cookie_text', None)
            if not url:
                self.write(
                    '<script language="javascript"> alert("提交内容为空不能获取");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            data = get_chrome_cookie(url)
            if not data:
                self.write(
                    '<script language="javascript"> alert("未发现相关cookie");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            feedback = put_cookie(url, data)
            if feedback:
                self.write(
                    '<script language="javascript"> alert("获取cookie成功");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")


class ChatHandler(WebSocketHandler):

    def open(self):
        print("连接")
        # self.write_message("正在检测")

    def on_message(self, message):
        print(message)
        domain = message
        key = "cookies:{}".format(domain)
        data = {'proportion': '', 'update': '', 'count': '', 'error': ''}
        obj = Cookies.get(domain=domain)
        cookie_count = obj.count
        test_type = obj.test_type
        test_url = obj.test_url
        test_sgin = obj.test_sign
        if test_type or test_url or test_sgin:
            pass
        else:
            data['error'] = 1
            return self.write_message(data)
        test_date = obj.testing_date
        cookies = RedisTools.get_set_all(key)

        if test_type.upper() == "REQUESTS":
            for index, cookie in enumerate(cookies):

                if TestCookie.requests_test(test_url, test_sgin, cookie):
                    pass
                else:
                    RedisTools.delete_set(key, json.dumps(cookie))
                data['proportion'] = round(index + 1 / cookie_count, 4) * 100
                if data['proportion'] < 100:
                    self.write_message(data)
        else:
            test = TestCookie()
            for index, cookie in enumerate(cookies):
                if test.selenium_test(test_url, test_sgin, cookie):
                    pass
                else:
                    RedisTools.delete_set(key, json.dumps(cookie))
                data['proportion'] = round(index+1/cookie_count, 4)*100
                if data['proportion'] < 100:
                    self.write_message(data)
            test.close()
        count = RedisTools.get_set_number(key)
        obj.update_date = datetime.datetime.now()
        data['update'] = str(obj.update_date)
        data['count'] = count
        if count:
            obj.count = data['count'] = count
            obj.save()
        else:
            obj.delete_instance()
        print(data)
        self.write_message(data)

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/*", IndexHandler),
        (r'/chat', ChatHandler),
        (r'/random', Random),
        (r'/all', All)
    ],
        xsrf_cookies=True,
        debug=True,
        static_path='static',
        template_path="template"
    )
    app.listen(8016)
    tornado.ioloop.IOLoop.current().start()