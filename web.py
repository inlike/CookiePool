# coding:utf-8

import tornado.web
import tornado.ioloop
import json
import time
import datetime
from db.peeweetools import Cookies
from handle.getcookie import *
from handle.Interface import *
from tornado.websocket import WebSocketHandler


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
        self.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        print(message)
        n = 100
        for i in range(1, n+1):
            time.sleep(0.1)
            self.write_message("{}".format(round(i/n, 4)*100))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/*", IndexHandler),
        (r'/chat', ChatHandler)
    ],
        xsrf_cookies=True,
        debug=True,
        static_path='static',
        template_path="template"
    )
    app.listen(8009)
    tornado.ioloop.IOLoop.current().start()