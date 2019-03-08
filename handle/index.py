# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from base import BaseHandler
from tornado.web import authenticated
from operation import operation


class IndexHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        role = self.get_secure_cookie('role')
        username = self.get_secure_cookie('username')
        if user_id:
            goods_list = operation.get_all_goods()
            self.render('index.html', goods_list=goods_list, role=role)
        else:
            self.redirect('/login')


class AddGoodsHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        role = self.get_secure_cookie('role')
        username = self.get_secure_cookie('username')
        if user_id:
            info = {
                'name': '',
                'count': '',
                'message': '',
            }
            self.render('add_goods.html', **info)
        else:
            self.redirect('/login')

    def post(self):
        name = self.get_argument('name')
        count = self.get_argument('count')
        ref = None
        try:
            ref = operation.add_goods(name, count)
        except Exception as e:
            err_msg = e.message
            self.render('add_goods.html', name=name, count='',message=err_msg)
            return
        if ref:
            self.redirect('/index')


class UpdateGoodsHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        id = self.get_argument('id')
        role = self.get_secure_cookie('role')
        username = self.get_secure_cookie('username')
        goods = operation.get_goods_by_id(id)
        if user_id:
            info = {
                'id': goods['id'],
                'name': goods['name'],
                'count': goods['count'],
                'message': '',
            }
            self.render('update_goods.html', **info)
        else:
            self.redirect('/login')

    def post(self):
        name = self.get_argument('name')
        count = self.get_argument('count')
        id = self.get_argument('id')
        ref = None
        try:
            ref = operation.update_goods(name, count, id)
        except Exception as e:
            err_msg = e.message
            self.render('add_goods.html', id=id, name=name, count='', message=err_msg)
            return
        if ref:
            self.redirect('/index')


class ApplyGoodsHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        id = self.get_argument('id')
        role = self.get_secure_cookie('role')
        username = self.get_secure_cookie('username')
        goods = operation.get_goods_by_id(id)
        if user_id:
            info = {
                'id': goods['id'],
                'name': goods['name'],
                'count': goods['count'],
                'user_id': user_id,
                'message': '',
            }
            self.render('apply_goods.html', **info)
        else:
            self.redirect('/login')

    def post(self):
        user_id = self.get_argument('user_id')
        name = self.get_argument('name')
        count = self.get_argument('count')
        id = self.get_argument('id')
        ref = None
        try:
            ref = operation.apply_goods(id, count, user_id)
        except Exception as e:
            err_msg = e.message
            self.render('apply_goods.html', id=id, name=name, count='', message=err_msg, user_id=user_id)
            return
        if ref:
            self.redirect('/index')


class ApplicationHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        role = self.get_secure_cookie('role')
        application_list = operation.get_application_by_user_id(role, user_id)
        if user_id:
            info = {
                'message': '',
                'role': role,
                'application_list': application_list,
            }
            self.render('application.html', **info)
        else:
            self.redirect('/login')


class UpdateApplicationHandle(BaseHandler):
    @authenticated
    def get(self):
        user_id = self.get_current_user()
        role = self.get_secure_cookie('role')
        if user_id:
            application_id = self.get_argument('id')
            approval = self.get_argument('approval')
            message = ''
            try:
                operation.update_application(role, application_id, approval)
            except Exception as e:
                message = e.message
            application_list = operation.get_application_by_user_id(role, user_id)
            info = {
                'message': message,
                'role': role,
                'application_list': application_list,
            }
            self.render('application.html', **info)
        else:
            self.redirect('/login')