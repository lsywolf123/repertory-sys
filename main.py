# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import os
import tornado.ioloop
import tornado.web
from handle import login
from handle import index
from handle import logout



ROOT = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT, "templates")
TMP_PATH = os.path.join(ROOT, "templates")

settings = {
    'template_path': TMP_PATH,
    "static_path": STATIC_PATH,
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o",
    "login_url": "/login",
}

application = tornado.web.Application(
    [
        (r"/index", index.IndexHandle),
        (r'/login', login.LoginHandle),
        (r'/logout', logout.LogoutHandle),
        (r"/add-goods", index.AddGoodsHandle),
        (r"/update-goods", index.UpdateGoodsHandle),
        (r"/apply-goods", index.ApplyGoodsHandle),
        (r"/application", index.ApplicationHandle),
        (r"/update-application", index.UpdateApplicationHandle),
    ], **settings)


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    print 'server 0.0.0.0:8000 started'