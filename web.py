# coding:utf-8

import tornado.web
import tornado.ioloop
import json
import time
import datetime
from handle.getcookie import *
from handle.Interface import *
from db.peeweetools import Cookies
from handle.getcookie import *
from handle.Interface import *


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        item = Cookies()
        items = item.to_dict()
        self.render("index.html", data=items)

    def post(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        operation = post_data.get("button", None)[0]
        if operation == 'save':
            obj = Cookies().get(domain=post_data['domain'][0])
            obj.test_type = ''.join(post_data['test_type'])
            obj.test_url = ''.join(post_data['test_url'])
            obj.test_sign = ''.join(post_data['test_sign'])
            obj.save()
            self.write(
                '<script language="javascript"> alert("更新成功"); </script>')
            return self.write("<script>location.href='/';</script>")
        elif operation == 'del':
            obj = Cookies().get(domain=post_data['domain'][0])
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
            feedback = put_cookie(url, data)
            if feedback:
                self.write(
                    '<script language="javascript"> alert("获取cookie成功");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/*", IndexHandler),
    ],
        xsrf_cookies=True,
        debug=True,
        static_path='static',
        template_path="template"
    )
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()