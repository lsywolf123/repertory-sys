# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
import exception
from db import api as db


# 创建新用户
def add_goods(name, count, created_at=None):
    if db.goods_name_if_exist_in_db(name):
        raise exception.GoodsIsExistException()
    values = {
        'name': name,
        'count': count,
        'created_at': created_at if created_at else None
    }
    return db.goods_create(values)


# 根据username查找用户
def get_all_goods():
    result_list = []
    goods_list = db.goods_get_all()
    num = 1
    for goods in goods_list:
        goods = dict(goods)
        goods['num'] = num
        result_list.append(goods)
        num += 1
    return result_list


# 根据username查找用户
def get_goods_by_id(id):
    goods = db.goods_get_by_id(id)
    return dict(goods)


def update_goods(name, count, id):
    values = {
        'name': name,
        'count': count
    }
    return db.goods_update_by_id(id, values)


def apply_goods(id, count, user_id, created_at=None):
    goods = db.goods_get_by_id(id)
    if int(count) > int(goods['count']):
        raise exception.GoodsIsNotEnoughException()
    values = {
        'apply_user': user_id,
        'apply_goods': id,
        'apply_count': count,
        'is_approval': 0,
        'created_at': created_at if created_at else None
    }
    return db.application_create(values)


def get_application_by_user_id(role, user_id):
    application_list = []
    if role == '1':
        result = db.application_get_all()
    else:
        result = db.application_get_by_user_id(user_id)
    count = 1
    for application in result:
        application = dict(application)
        application['num'] = count
        application['name'] = db.goods_get_by_id(application['apply_goods'])['name']
        if application['approval'] == 0 and application['decline'] == 0:
            application['status'] = '未处理'
        elif application['approval'] == 1 and application['decline'] == 0:
            application['status'] = '已通过'
        elif application['approval'] == 0 and application['decline'] == 1:
            application['status'] = '已拒绝'
        application_list.append(application)
        count += 1
    return application_list


def update_application(role, application_id, approval):
    application = db.application_get_by_id(application_id)
    goods = db.goods_get_by_id(application['apply_goods'])
    if goods['count'] - application['apply_count'] < 0 and approval == 'True':
        raise exception.GoodsIsNotEnoughException()
    if application['approval'] == 0 and application['decline'] == 0 and role == '1':
        if approval == 'True':
            values = {
                'approval': 1
            }
        if approval == 'False':
            values = {
                'decline': 1
            }
        res = db.application_update_by_id(application_id, values)
        if res:
            if approval == 'True':
                values = {
                    'count': goods['count'] - application['apply_count']
                }
                db.goods_update_by_id(application['apply_goods'], values)

if __name__ == '__main__':
    pass