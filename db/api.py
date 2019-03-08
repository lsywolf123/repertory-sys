# -*- coding: utf-8 -*-
"""
Created on 2017-7-12
@author: lsy
Implementation of SQLAlchemy backend.
"""
import logging
import datetime
from datetime import timedelta
from db.session import get_session
from db import models

LOG = logging.getLogger(__name__)


def model_query(*args, **kwargs):
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or 'no'

    query = session.query(*args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
            "Unrecognized read_deleted value '%s'" % read_deleted)
    return query

PERFECT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def parse_time(time, fmt=PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(time, fmt)


def convert_datetime(values, *datetime_keys):
    for key in values:
        if key in datetime_keys and isinstance(values[key], basestring):
            values[key] = parse_time(values[key])
    return values


def utc_now():
    """Overridable version of utils.utc_now."""
    if utc_now.override_time:
        try:
            return utc_now.override_time.pop(0)
        except AttributeError:
            return utc_now.override_time
    return datetime.datetime.now()

utc_now.override_time = None


# user表操作
def user_create(values, session=None):
    if not values['created_at']:
        values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        user_ref = models.User()
        session.add(user_ref)
        user_ref.update(values)
    return user_ref


def user_create_customer(values, session=None):
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        user_ref = models.User()
        session.add(user_ref)
        user_ref.update(values)
    return user_ref


def user_username_if_exist_in_db(username, session=None):
    if model_query(models.User, session=session).\
            filter_by(username=username).\
            first():
        return True
    return False


def user_get_by_username(username, session=None):
    return model_query(models.User, session=session).\
            filter_by(username=username).\
            first()


def user_get_by_id(user_id, session=None):
    return model_query(models.User, session=session).\
            filter_by(id=user_id).\
            first()


def user_update_by_id(user_id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        user_ref = user_get_by_id(user_id, session=session)
        for (key, value) in values.iteritems():
            user_ref[key] = value
        user_ref.save(session=session)
        return user_ref


# Repertory表
def goods_create(values, session=None):
    if not values['created_at']:
        values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        repertory_ref = models.Repertory()
        session.add(repertory_ref)
        repertory_ref.update(values)
    return repertory_ref


def goods_name_if_exist_in_db(name, session=None):
    if model_query(models.Repertory, session=session).\
            filter_by(name=name).\
            first():
        return True
    return False


def goods_get_all(session=None):
    return model_query(models.Repertory, session=session).\
            all()


def goods_get_by_id(id, session=None):
    return model_query(models.Repertory, session=session).\
            filter_by(id=id).\
            first()


def goods_get_by_name(name, session=None):
    return model_query(models.Repertory, session=session).\
            filter_by(name=name).\
            first()


def goods_update_by_id(id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        goods_ref = goods_get_by_id(id, session=session)
        for (key, value) in values.iteritems():
            goods_ref[key] = value
        goods_ref.save(session=session)
        return goods_ref


# application表
def application_create(values, session=None):
    if not values['created_at']:
        values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        application_ref = models.Application()
        session.add(application_ref)
        application_ref.update(values)
    return application_ref


def application_get_all(session=None):
    return model_query(models.Application, session=session). \
        order_by(models.Application.created_at.asc()). \
        all()


def application_get_by_id(id, session=None):
    return model_query(models.Application, session=session).\
            filter_by(id=id).\
            first()


def application_get_by_user_id(user_id, session=None):
    return model_query(models.Application, session=session).\
        filter_by(apply_user=user_id). \
        order_by(models.Application.created_at.asc()). \
        all()


def application_update_by_id(id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        application_ref = application_get_by_id(id, session=session)
        for (key, value) in values.iteritems():
            application_ref[key] = value
        application_ref.save(session=session)
        return application_ref


# merchant表操作
def merchant_create(values, session=None):
    values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        merchant_ref = models.Merchant()
        session.add(merchant_ref)
        merchant_ref.update(values)
    return merchant_ref


def merchant_get_by_id(merchant_id, session=None):
    return model_query(models.Merchant, session=session).\
            filter_by(id=merchant_id).\
            first()


def merchant_get_by_name(name, session=None):
    return model_query(models.Merchant, session=session).\
            filter_by(name=name).\
            first()


def merchant_get_by_user_id(user_id, session=None):
    return model_query(models.Merchant, session=session).\
            filter_by(user_id=user_id).\
            first()



def merchant_delete_by_id(merchant_id):
    session = get_session()
    with session.begin(subtransactions=True):
        values = {
            'deleted': 1,
            'deleted_at': utc_now()
        }
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        merchant_ref = merchant_get_by_id(merchant_id, session=session)
        for (key, value) in values.iteritems():
            merchant_ref[key] = value
        merchant_ref.save(session=session)
        return merchant_ref


def merchant_update_by_id(merchant_id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        merchant_ref = merchant_get_by_id(merchant_id, session=session)
        for (key, value) in values.iteritems():
            merchant_ref[key] = value
        merchant_ref.save(session=session)
        return merchant_ref


def merchant_phone_if_exist_in_db(phone, session=None):
    if model_query(models.Merchant, session=session).\
            filter_by(phone=phone).\
            first():
        return True
    return False


def merchant_list(session=None):
    return model_query(models.Merchant, session=session).\
        order_by(models.Merchant.created_at.desc()).\
        all()


def merchant_recent_list(session=None):
    return model_query(models.Merchant, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Merchant.created_at). \
        order_by(models.Merchant.created_at.desc()).\
        all()


def merchant_list_asc(session=None):
    return model_query(models.Merchant, session=session).\
        order_by(models.Merchant.deadline.asc()).\
        all()


def merchant_list_by_name_asc(name, session=None):
    return model_query(models.Merchant, session=session). \
        filter_by(name=name). \
        order_by(models.Merchant.deadline.asc()).\
        all()


def merchant_list_by_hostname_asc(host_name, session=None):
    return model_query(models.Merchant, session=session). \
        filter_by(host_name=host_name). \
        order_by(models.Merchant.deadline.asc()).\
        all()


def merchant_list_by_phone_asc(phone, session=None):
    return model_query(models.Merchant, session=session). \
        filter_by(phone=phone). \
        order_by(models.Merchant.deadline.asc()).\
        all()


def merchant_count(session=None):
    query = model_query(models.Merchant, session=session).\
            count()
    return query


def search_merchant_count_by_name(name, session=None):
    query = model_query(models.Merchant, session=session). \
        filter_by(name=name). \
        count()
    return query


def search_merchant_count_by_hostname(hostname, session=None):
    query = model_query(models.Merchant, session=session). \
        filter_by(host_name=hostname). \
        count()
    return query


def search_merchant_count_by_phone(phone, session=None):
    query = model_query(models.Merchant, session=session). \
        filter_by(phone=phone). \
        count()
    return query


def merchant_recent_count(session=None):
    query = model_query(models.Merchant, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Merchant.created_at). \
        count()
    return query


def merchant_expire_count(session=None):
    query = model_query(models.Merchant, session=session). \
        filter(utc_now() > models.Merchant.deadline). \
        count()
    return query


# 客户表操作
def customer_create(values, session=None):
    if not values.has_key('created_at'):
        values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        customer_ref = models.Customer()
        session.add(customer_ref)
        customer_ref.update(values)
    return customer_ref


def customer_bind_by_serial_num(serial_num, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['created_at'] = utc_now()
        customer_ref = customer_get_by_serial_num(serial_num, session=session)
        for (key, value) in values.iteritems():
            customer_ref[key] = value
        customer_ref.save(session=session)
        return customer_ref


def customer_get_by_serial_num(serial_num, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(serial_num=serial_num). \
        first()


def customer_get_by_merchant_id_order_by_exchange(merchant_id, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Customer.gain_money.desc()). \
        all()


def customer_get_by_merchant_id_order_by_goldbean(merchant_id, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Customer.total_gb.desc()). \
        all()


def customer_get_by_id(customer_id, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(id=customer_id). \
        first()


def customer_get_by_user_id(user_id, session=None):
    return model_query(models.Customer, session=session).\
            filter_by(user_id=user_id).\
            first()


def customer_update_by_id(customer_id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        customer_ref = customer_get_by_id(customer_id, session=session)
        for (key, value) in values.iteritems():
            customer_ref[key] = value
        customer_ref.save(session=session)
        return customer_ref


def customer_list(session=None):
    return model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        order_by(models.Customer.created_at.desc()).\
        all()


def customer_list_by_merchant_id(merchant_id, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Customer.created_at.desc()).\
        all()


def customer_recent_list(session=None):
    return model_query(models.Customer, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Customer.created_at). \
        filter(models.Customer.merchant_id != None). \
        order_by(models.Customer.created_at.desc()).\
        all()


def customer_recent_list_by_merchant_id(merchant_id, session=None):
    return model_query(models.Customer, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Customer.created_at). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Customer.created_at.desc()).\
        all()


def customer_added_list(session=None):
    return model_query(models.User, session=session). \
        filter_by(role=3). \
        order_by(models.User.created_at.desc()).\
        all()


def customer_added_list_by_created_time(created_time, session=None):
    return model_query(models.User, session=session). \
        filter_by(created_at=created_time). \
        order_by(models.User.created_at.desc()).\
        all()


def customer_added_count_by_created_time(created_time, session=None):
    return model_query(models.User, session=session). \
        filter_by(created_at=created_time). \
        order_by(models.User.created_at.desc()).\
        count()


def customer_last(session=None):
    return model_query(models.Customer, session=session). \
        order_by(models.Customer.serial_num.desc()).\
        first()


def customer_count(session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        count()
    return query


def customer_count_by_merchant_id(merchant_id,session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        count()
    return query


def customer_recent_count(session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter(datetime.datetime.now()-timedelta(days=7) <= models.Customer.created_at). \
        count()
    return query


def customer_recent_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(datetime.datetime.now()-timedelta(days=7) <= models.Customer.created_at). \
        count()
    return query


def customer_active_count(session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter(datetime.datetime.now()-timedelta(days=7) <= models.Customer.updated_at). \
        count()
    return query


def customer_active_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(datetime.datetime.now()-timedelta(days=7) <= models.Customer.updated_at). \
        count()
    return query


def search_customer_count_by_serial_num(merchant_id, serial_num, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(serial_num=serial_num). \
        count()
    return query


def search_customer_count_by_name(merchant_id, name, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(name=name). \
        count()
    return query


def search_customer_count_by_phone(merchant_id, phone, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(phone=phone). \
        count()
    return query


def search_customer_count_by_gb_range(merchant_id, min_gb, max_gb, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Customer.total_gb >= min_gb). \
        filter(models.Customer.total_gb < max_gb). \
        count()
    return query


def customer_list_by_serial_num(merchant_id, serial_num, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(serial_num=serial_num). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_list_by_name(merchant_id, name, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(name=name). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_list_by_phone(merchant_id, phone, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(phone=phone). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_list_by_gb_range(merchant_id, min_gb, max_gb, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Customer.total_gb >= min_gb). \
        filter(models.Customer.total_gb < max_gb). \
        order_by(models.Customer.total_gb.desc()).\
        all()


def search_all_customer_count_by_serial_num(serial_num, session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(serial_num=serial_num). \
        count()
    return query


def search_all_customer_count_by_name(name, session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(name=name). \
        count()
    return query


def search_all_customer_count_by_phone(phone, session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(phone=phone). \
        count()
    return query


def search_all_customer_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        count()
    return query


def search_all_customer_count_by_gb_range(min_gb, max_gb, session=None):
    query = model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter(models.Customer.gb >= min_gb). \
        filter(models.Customer.gb < max_gb). \
        count()
    return query


def customer_all_list_by_serial_num(serial_num, session=None):
    return model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(serial_num=serial_num). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_all_list_by_name(name, session=None):
    return model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(name=name). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_all_list_by_phone(phone, session=None):
    return model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter_by(phone=phone). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_all_list_by_merchant_id(merchant_id, session=None):
    return model_query(models.Customer, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Customer.gb.desc()).\
        all()


def customer_all_list_by_gb_range(min_gb, max_gb, session=None):
    return model_query(models.Customer, session=session). \
        filter(models.Customer.merchant_id != None). \
        filter(models.Customer.gb >= min_gb). \
        filter(models.Customer.gb < max_gb). \
        order_by(models.Customer.gb.desc()).\
        all()


# 消费表操作
def consume_create(values, session=None):
    values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        consume_ref = models.Consume()
        session.add(consume_ref)
        consume_ref.update(values)
    return consume_ref


def consume_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        count()
    return query


def consume_count_by_customer_id(customer_id, session=None):
    query = model_query(models.Consume, session=session). \
        filter_by(customer_id=customer_id). \
        count()
    return query


def search_consume_count_by_consumer_name(merchant_id, consumer_name, session=None):
    query = model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(consumer_name=consumer_name). \
        count()
    return query


def search_consume_count_by_customer_id(merchant_id, customer_id, session=None):
    query = model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(customer_id=customer_id). \
        count()
    return query


def search_consume_count_by_created_at(merchant_id, min_time, max_time, session=None):
    query = model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Consume.created_at <= max_time). \
        filter(models.Consume.created_at >= min_time). \
        count()
    return query


def consume_list_by_merchant_id(merchant_id, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Consume.created_at.desc()).\
        all()


def consume_list_by_consumer_name(merchant_id, consumer_name, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(consumer_name=consumer_name). \
        order_by(models.Consume.created_at.desc()). \
        all()


def consume_list_by_customer_id(merchant_id, customer_id, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(customer_id=customer_id). \
        order_by(models.Consume.created_at.desc()). \
        all()


def consume_get_by_customer_id(customer_id, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(customer_id=customer_id). \
        order_by(models.Consume.created_at.desc()). \
        all()


def consume_recent_list_by_customer_id(customer_id, session=None):
    return model_query(models.Consume, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Consume.created_at). \
        filter_by(customer_id=customer_id). \
        order_by(models.Consume.created_at.desc()). \
        all()


def consume_all_list_by_customer_id(customer_id, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(customer_id=customer_id). \
        order_by(models.Consume.created_at.desc()). \
        all()


def consume_list_by_created_at(merchant_id, min_time, max_time, session=None):
    return model_query(models.Consume, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Consume.created_at <= max_time). \
        filter(models.Consume.created_at >= min_time). \
        all()


# 规则表操作
def rule_create(values, session=None):
    values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        rule_ref = models.Rule()
        session.add(rule_ref)
        rule_ref.update(values)
    return rule_ref


def rule_get_by_merchant_id(merchant_id, session=None):
    return model_query(models.Rule, session=session). \
        filter_by(merchant_id=merchant_id). \
        first()


def rule_update_by_merchant_id(merchant_id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        rule_ref = rule_get_by_merchant_id(merchant_id, session=session)

        for (key, value) in values.iteritems():
            rule_ref[key] = value
        rule_ref.save(session=session)
        return rule_ref


# 活动表操作
def activity_create(values, session=None):
    values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        activity_ref = models.Activity()
        session.add(activity_ref)
        activity_ref.update(values)
    return activity_ref


def activity_get_by_merchant_id(merchant_id, session=None):
    return model_query(models.Activity, session=session). \
        filter_by(merchant_id=merchant_id). \
        first()


def activity_update_by_merchant_id(merchant_id, values):
    session = get_session()
    with session.begin(subtransactions=True):
        values['updated_at'] = utc_now()
        convert_datetime(values, 'created_at', 'deleted_at', 'updated_at')
        activity_ref = activity_get_by_merchant_id(merchant_id, session=session)
        for (key, value) in values.iteritems():
            activity_ref[key] = value
        activity_ref.save(session=session)
        return activity_ref


# 兑换表操作
def exchange_create(values, session=None):
    values['created_at'] = utc_now()
    if not session:
        session = get_session()
    with session.begin(subtransactions=True):
        exchange_ref = models.Exchange()
        session.add(exchange_ref)
        exchange_ref.update(values)
    return exchange_ref


def exchange_get_all_by_customer_id(customer_id, session=None):
    return model_query(models.Exchange, session=session). \
        filter_by(customer_id=customer_id). \
        order_by(models.Exchange.created_at.desc()). \
        all()


def exchange_get_by_customer_id(customer_id, session=None):
    return model_query(models.Exchange, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Exchange.created_at). \
        filter_by(customer_id=customer_id). \
        order_by(models.Exchange.created_at.desc()). \
        all()


def exchange_get_by_merchant_id(merchant_id, session=None):
    return model_query(models.Exchange, session=session). \
        filter(datetime.datetime.now() - timedelta(days=7) <= models.Exchange.created_at). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Exchange.created_at.desc()). \
        all()


def exchange_recent_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(datetime.datetime.now()-timedelta(days=7) <= models.Exchange.created_at). \
        count()
    return query


def exchange_count_by_merchant_id(merchant_id, session=None):
    query = model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        count()
    return query


def exchange_count_by_customer_id(customer_id, session=None):
    query = model_query(models.Exchange, session=session). \
        filter_by(customer_id=customer_id). \
        count()
    return query


def search_exchange_count_by_customer_name(merchant_id, customer_name, session=None):
    query = model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(customer_name=customer_name). \
        count()
    return query


def search_exchange_count_by_created_at(merchant_id, min_time, max_time, session=None):
    query = model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Exchange.created_at <= max_time). \
        filter(models.Exchange.created_at >= min_time). \
        count()
    return query


def exchange_list_by_merchant_id(merchant_id, session=None):
    return model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        order_by(models.Exchange.created_at.desc()).\
        all()


def exchange_list_by_customer_name(merchant_id, customer_name, session=None):
    return model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter_by(customer_name=customer_name). \
        order_by(models.Exchange.created_at.desc()). \
        all()


def exchange_list_by_created_at(merchant_id, min_time, max_time, session=None):
    return model_query(models.Exchange, session=session). \
        filter_by(merchant_id=merchant_id). \
        filter(models.Exchange.created_at <= max_time). \
        filter(models.Exchange.created_at >= min_time). \
        all()


if __name__ == '__main__':
    values = {}
    values['role'] = 2
    values['username'] = 'test1'
    values['password'] = '123456'
    values['created_at'] = utc_now()
    user_create(values)
    # print goods_get_by_name('李锤子')['count']
