# coding:utf-8

import tornado.web
import tornado.ioloop
import json
import time
from handle.getcookie import *
from handle.Interface import *


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        self.render("inde.html")

    def post(self):
        vendor = self.get_argument("vendor", "")
        vendor_name = self.get_argument("vendor_name", "")
        if vendor == "":
            self.write('<script language="javascript"> alert("请输入vendor号及name"); </script>')
            return self.write('<script language="javascript"> window.close(); </script>')
        business_dict = ["InvTypeBusiness", "AbcCodeBusiness", "PmCodeBusiness"]
        items = dict()

        VpcCodeBusiness = self.get_argument("VpcCodeBusiness", "")
        if VpcCodeBusiness:
            business_dict.append("VpcCodeBusiness")
        business_dict.append("PoExistBusiness")
        business_dict.append("SpecialMethodBusiness")
        CommentsBusiness = self.get_argument("CommentsBusiness", "")
        if CommentsBusiness:
            business_dict.append("CommentsBusiness")

        data = {"list": business_dict, "dict": items, "vendor": vendor,
                "name": vendor_name, "list_json": business_json}
        self.render("confirm.html", data=data)


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/confirm", Confirm),
        (r'/search.*', Search),
    ],
        xsrf_cookies=True,
        debug=True,
        static_path='static',
        template_path="templates"
    )
    app.listen(8008)
    tornado.ioloop.IOLoop.current().start()