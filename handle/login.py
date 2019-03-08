# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import datetime
from base import BaseHandler
from operation import user


class LoginHandle(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/index')
        else:
            self.render("sign-in.html", message='', username='')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        ref = None
        try:
            ref = user.login(username, password)
        except Exception as e:
            err_msg = e.message
            self.render('sign-in.html', username=username, message=err_msg)
            return
        self.set_secure_cookie('user_id', ref['id'])
        self.set_secure_cookie('role', ref['role'])
        self.set_secure_cookie('username', ref['username'])
        self.redirect('/index')