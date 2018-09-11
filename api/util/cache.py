#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylibmc, _pylibmc
import settings
import hashlib
import inspect
import time
import functools
from functools import wraps
import re
import logging
from sets import Set as do_set
import traceback
import random

class ExpireTime(object):
    u"""缓存超时时间, 单位秒"""
    HALF_MIN = 30
    MIN = 60
    FIVE_MINS = 60 * 5
    TEN_MINS = 60 * 10
    TWENTY_MINS = 60 * 20
    HALF_HOUR = 60 * 30
    HOUR = 60 * 60
    HALF_DAY = 60 * 60 * 12
    DAY = 60 * 60 * 24
    TWO_DAY = 60 * 60 * 48
    MONTH_DAY = 60 * 60 * 24 * 30

# default expire time
expire_time = ExpireTime.HOUR

def mc_cmd(func):
    def f(*args, **kwargs):
        self = args[0]
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            if (self.old_libmc_version) and (
                time.time() - self.conn_time > self.retry_timeout):
                try:
                    self.conn()
                    result = func(*args, **kwargs)
                except Exception as e2:
                    logging.error(e2)
        return result
    return f

class Client(object):
    def __init__(self, servers):
        self._servers = servers

        try:
            self.old_libmc_version = _pylibmc.libmemcached_version_hex < 0x01000003
        except:
            self.old_libmc_version = True

        self.conn()

    def conn(self):
        self._mc = self._conn(self._servers)

    def _conn(self, servers):
        behaviors = {
            'ketama': True,
            'no_block': True,
            'tcp_nodelay': True,
            'remove_failed': 100,
            '_retry_timeout': 3,
            'dead_timeout': 3,
        }

        # 1.0.3之前的版本不支持dead_timeout，只能自己实现重连

        if self.old_libmc_version:
            del behaviors['dead_timeout']
            self.conn_time = time.time()
            self.retry_timeout = behaviors['_retry_timeout']

        mc = pylibmc.Client(servers, binary=True, behaviors=behaviors)
        return mc

    @staticmethod
    def _fix_key(key):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        return key

    def clone(self):
        u"""TODO: 还考虑处理线程安全"""
        return self

    @mc_cmd
    def add(self, key, value, time=expire_time):
        key = Client._fix_key(key)
        return self._mc.add(key, value, time)

    @mc_cmd
    def delete(self, key):
        key = Client._fix_key(key)
        return self._mc.delete(key)

    @mc_cmd
    def set(self, key, value, time=expire_time):
        key = Client._fix_key(key)
        return self._mc.set(key, value, time)

    @mc_cmd
    def set_multi(self, mapping, time=expire_time):
        new_mapping = {}
        for k, v in mapping.items():
            new_mapping[Client._fix_key(k)] = v
        return self._mc.set_multi(mapping, time)

    @mc_cmd
    def get(self, key):
        key = Client._fix_key(key)
        return self._mc.get(key)

    @mc_cmd
    def get_multi(self, keys):
        keys = [Client._fix_key(i) for i in keys]
        return self._mc.get_multi(keys)

    @mc_cmd
    def decr(self, key):
        key = Client._fix_key(key)
        return self._mc.decr(key)

    @mc_cmd
    def incr(self, key):
        key = Client._fix_key(key)
        return self._mc.incr(key)

    #live
    def get_random(self, key):
        key = Client._fix_key(key)
        return self._mc.get(key)

    def set_random(self, key, value, time=expire_time):
        key = Client._fix_key(key)
        return self._mc.set(key, value, time)


# FIXME: deprecated 以下为兼容代码

def client(servers):
    return Client(servers)

###################################################
#                   cache define                  #
###################################################
# master
_mc0 = client(settings.cache_servers0)
pool0 = pylibmc.ThreadMappedPool(_mc0)

# slave
_mc1 = _mc0 #client(settings.cache_servers1)
pool1 = pool0 #pylibmc.ThreadMappedPool(_mc1)


# master
_search_mc0 = client(settings.search_cache_servers0)
search_pool0 = pylibmc.ThreadMappedPool(_search_mc0)
#
#########################################################
# qrcode_test
# qrcode_test_mc = client(settings.qrcode_online_mc)
# qrcode_test = pylibmc.ThreadMappedPool(qrcode_test_mc)
#
# #########################################################
#
# # slave
# _search_mc1 = _search_mc0 #client(settings.search_cache_servers1)
# search_pool1 = search_pool0 # pylibmc.ThreadMappedPool(_search_mc1)
#
# # master
# _statis_mc0 = client(settings.statis_cache_server0)
# statis_pool0 = pylibmc.ThreadMappedPool(_statis_mc0)
# #
# # slave
# _statis_mc1 = _statis_mc0 #client(settings.search_cache_servers1)
# statis_pool1 = statis_pool0 # pylibmc.ThreadMappedPool(_search_mc1)
#
# #das cache
# _das_mc0 = client(settings.das_cache_server0)
# das_pool0 = pylibmc.ThreadMappedPool(_das_mc0)
#
# # master
# _play_secret_mc0 = client(settings.play_secret_cache_servers0)
# play_secrect_pool0 = pylibmc.ThreadMappedPool(_play_secret_mc0)

###################################################
#                  end cache define               #
###################################################


def incr(key,pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.incr(key)
    return result

def decr(key,pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.decr(key)
    return result

def add(key, value, time=expire_time, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.add(key, value, time)
    return result

def delete(key, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.delete(key)
    return result

def set(key, value, time=expire_time, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.set(key, value, time)
    return result

def set_multi(mapping, time=expire_time, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.set_multi(mapping, time)
    return result

def get(key, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.get(key)
    return result

def get_multi(keys, pool=pool0):
    with pool.reserve() as _mc:
        result = _mc.get_multi(keys)
    return result


#### search multi start#####
def get_multi_search(keys, pool=search_pool0):
    with pool.reserve() as _mc:
        result = _mc.get_multi(keys)
    return result


def set_multi_search(mapping, time=expire_time, pool=search_pool0):
    with pool.reserve() as _mc:
        result = _mc.set_multi(mapping, time)
    return result
#### search multi end#####

# #####################statis get/set####################
# def get_statis(key):
#     with statis_pool0.reserve() as _mc:
#         result = _mc.get(key)
#     return result
#
#
# def set_statis(key, value, time=expire_time):
#     with statis_pool0.reserve() as _mc:
#         result = _mc.set(key, value, time)
#     return result
#
# def incr_statis(key):
#     with statis_pool0.reserve() as _mc:
#         result = _mc.incr(key)
#     return result


#####################search get/set####################
def get_search(key):
    with search_pool0.reserve() as _mc:
        result = _mc.get(key)
    return result


def set_search(key, value, time=expire_time):
    with search_pool0.reserve() as _mc:
        result = _mc.set(key, value, time)
    return result

# #####################play_secret get/set####################
# def get_play_secret(key):
#     with play_secrect_pool0.reserve() as _mc:
#         result = _mc.get(key)
#     return result
#
#
# def set_play_secret(key, value, time=expire_time):
#     with play_secrect_pool0.reserve() as _mc:
#         result = _mc.set(key, value, time)
#     return result


# --------- 以上为兼容代码

#def get_plus(key, func, expire_m=None, expire_s=None, is_update=False):
#    u"""
#    分别尝试从pool0和pool1中取key的值
#    如果pool0取值失败，则调用func来生成值，并写入pool0和pool1
#    func调用期间，会优先尝试从pool1中取值，避免同时重复执行func多次
#    """
#    content = None if is_update else get(key)
#    if content is None:
#        key_mutex = key + '_mutex'
#        expire_m = expire_m or settings.cache_expire_XL
#        expire_s = expire_s or settings.cache_expire_MAX
#
#        def _get_and_set():
#            result = func()
#            if result is not None:
#                set(key, result, expire_m)
#                set(key, result, expire_s, pool1)
#                delete(key_mutex)
#            return result
#
#        if add(key_mutex, 1, settings.cache_expire_M):
#            try:
#                content = _get_and_set()
#            except Exception as e:
#                content = get(key, pool1)
#                if content is None:
#                    raise e
#        else:
#            content = get(key, pool1)
#            if content is None:
#                content = _get_and_set()
#
#    return content

#
#* ************new cache strategy 1********************/
#
def get_from_cache(key, func, expire_m=None, expire_s=None, is_update=False):

    content = None
    if not is_update:
        #get from cache pool0
        content = get(key)
        if content:
            return content

    #mutex key for set new key
    key_mutex = '%s_mutex' % key
    #default pool0 one hour after be expired.
    expire_m = expire_m or settings.cache_expire_One_Hour
    #week 7 days not expire
    expire_s = settings.cache_expire_Two_Day

    def get_and_set():
        #get result from origin function
        try:
            result = func()
            if result is not None:
                #write to pool0
                set(key, result, expire_m)
                #write to pool1
                set(key, result, expire_s, pool1)
            return result
        except Exception,e:
            #throw exception to up layer
            logging.error(e)
            raise e

    if add(key_mutex, 1, settings.cache_expire_M):
        logging.debug("*mutex: %s" % key_mutex)

        try:
            content = get_and_set()
        except Exception as e:
            logging.error(e)

            content = get(key, pool1)
            #set to pool0 10m
            if content:
                logging.debug("*get from pool1 and set 10m:%s" % key)
                #set to pool0 for hit in cache pool0,ten minute after retry!
                set(key, content, settings.cache_expire_Ten_Minute)
                #reset expire time for not expire
                set(key, content, expire_s, pool1)
            else:
                #pool0 and pool1 no cache hit here
                raise e
        finally:
            #delate mutex key
            delete(key_mutex)
    else:
        #on key expire be mutex go here
        #get from pool1
        logging.debug("*mutex pool1: %s" % key)
        content = get(key, pool1)

        #retry to get from func() ,normally not go here ,must be evictions
        if not content:
            logging.debug("*pool1 evictions: %s" % key)
            content = get_and_set()

    return content


#
#* ************new cache strategy 2********************/
#
import datetime
def get_plus(key, func, expire_m=None, expire_s=None, is_update=False, set_retry = True, not_valid_check={}):

    #key = "new:%s" % key
    key_body_name = "api.body"
    key_expire_name = "api.expired_at"
    
    content = None
    raw_content = None
    if not is_update:
        #get from cache pool0
        content = get(key)
        if content:
            if isinstance(content,dict) and  content.has_key(key_expire_name) and content.has_key(key_body_name):
#                logging.debug("expired_at %s:now %s" % (datetime.datetime.fromtimestamp(\
#                    content.get(key_expire_name)).strftime("%H:%M:%S") , int(time.time())))
                
                #new version key result
                #{
                #   "api.body" : xxxxx
                #   "api.expire" :  1363672663
                #}
                if content.get(key_expire_name) > int(time.time()):
                    #not expired
                    logging.debug("get key from cache:%s" % key)
                    return content.get(key_body_name)
                else:
                    #expired to get new one
                    #if get new key exception use old one
                    logging.debug("expired %s" % key)
                    raw_content = content.get(key_body_name)
            else:
                #compatibe for old content
                logging.debug("get old key from cache:%s" % key)
                return content

    #default pool0 one hour after be expired.
    expire_m = expire_m or settings.cache_expire_One_Hour
    #expire_m = 3 for test
    #2h not expire
    expire_s = expire_s or settings.cache_expire_Two_Hour
    #key for mutex
    key_mutex = '%s_mutex' % key
    
    def get_and_set():
        
        try:
            #get result from origin function
            result = func()
            if result:

                #new version key result
                #{
                #   "api.body" : xxxxx
                #   "api.expire" :  1363672663
                #}
                valid = True
                if not_valid_check:
                    if isinstance(result,list):
                        for r in result:
                            for k,v in not_valid_check.iteritems():
                                if r.get(k) == v:
                                    valid = False
                                    break

                if valid:
                    logging.debug("set new version data")
                    data = {key_body_name:result, \
                            key_expire_name: int(time.time() + expire_m)}

                    logging.debug("get data add set key:%s" % key)
                    set(key, data, expire_s)
            return result
        except Exception,e:
            logging.error(e)
            logging.error(traceback.format_exc())

            if raw_content:
                logging.debug("exception use old key:%s" % key)
                if set_retry:
                    #set 10 minute retry
                    data = {key_body_name:raw_content, \
                            key_expire_name: int(time.time() + settings.cache_expire_Ten_Minute)}
                    set(key, data, expire_s)
                return raw_content
            else:
                #must be evctions or old key
                logging.error(e)
                raise e

                
    if add(key_mutex, 1, settings.cache_expire_M):
        logging.debug("*mutex: %s" % key_mutex)

        try:
            raw_content = get_and_set()
        finally:
            logging.debug("delete mutex key:%s" % key_mutex)
            #delate mutex key
            delete(key_mutex)
    else:
        #on key expire be mutex go here use old key to return
        logging.debug("*mutex locked: %s" % key)

        if not raw_content:
            #retry to get from func() ,normally not go here ,must be evictions
            logging.debug("* evictions: %s" % key)
            raw_content = get_and_set()

    return raw_content


#get_plus = get_from_cache_in_body


#
#* ************new cache strategy 2********************/
#
import json
def get_plus_json(key, func, expire_m=None, expire_s=None, is_update=False, set_retry = True, not_valid_check={}):

    #key = "new:%s" % key
    key_body_name = "api.body"
    key_expire_name = "api.expired_at"

    content = None
    raw_content = None
    if not is_update:
        #get from cache pool0
        content = get(key)
        if content:
            content = json.loads(content)
            if isinstance(content,dict) and  content.has_key(key_expire_name) and content.has_key(key_body_name):
#                logging.debug("expired_at %s:now %s" % (datetime.datetime.fromtimestamp(\
#                    content.get(key_expire_name)).strftime("%H:%M:%S") , int(time.time())))

                #new version key result
                #{
                #   "api.body" : xxxxx
                #   "api.expire" :  1363672663
                #}
                if content.get(key_expire_name) > int(time.time()):
                    #not expired
                    logging.debug("get key from cache:%s" % key)
                    return content.get(key_body_name)
                else:
                    #expired to get new one
                    #if get new key exception use old one
                    logging.debug("expired %s" % key)
                    raw_content = content.get(key_body_name)
            else:
                #compatibe for old content
                logging.debug("get old key from cache:%s" % key)
                return content

    #default pool0 one hour after be expired.
    expire_m = expire_m or settings.cache_expire_One_Hour
    #expire_m = 3 for test
    #2h not expire
    expire_s = expire_s or settings.cache_expire_Two_Hour
    #key for mutex
    key_mutex = '%s_mutex' % key

    def get_and_set():

        try:
            #get result from origin function
            result = func()
            if result:

                #new version key result
                #{
                #   "api.body" : xxxxx
                #   "api.expire" :  1363672663
                #}
                valid = True
                if not_valid_check:
                    if isinstance(result,list):
                        for r in result:
                            for k,v in not_valid_check.iteritems():
                                if r.get(k) == v:
                                    valid = False
                                    break

                if valid:
                    logging.debug("set new version data")
                    data = {key_body_name:result, \
                            key_expire_name: int(time.time() + expire_m)}

                    logging.debug("get data add set key:%s" % key)
                    data = json.dumps(data)
                    set(key, data, expire_s)
            return result
        except Exception,e:
            logging.error(e)

            if raw_content:
                logging.debug("exception use old key:%s" % key)
                if set_retry:
                    #set 10 minute retry
                    data = {key_body_name:raw_content, \
                            key_expire_name: int(time.time() + settings.cache_expire_Ten_Minute)}
                    data = json.dumps(data)
                    set(key, data, expire_s)
                return raw_content
            else:
                #must be evctions or old key
                logging.error(e)
                raise e


    if add(key_mutex, 1, settings.cache_expire_M):
        logging.debug("*mutex: %s" % key_mutex)

        try:
            raw_content = get_and_set()
        finally:
            logging.debug("delete mutex key:%s" % key_mutex)
            #delate mutex key
            delete(key_mutex)
    else:
        #on key expire be mutex go here use old key to return
        logging.debug("*mutex locked: %s" % key)

        if not raw_content:
            #retry to get from func() ,normally not go here ,must be evictions
            logging.debug("* evictions: %s" % key)
            raw_content = get_and_set()

    return raw_content



old_pattern = re.compile(r'%\w')
new_pattern = re.compile(r'\{(\w+(\.\w+|\[\w+\])?)\}')

__formaters = {}

def _format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = _formater(text)
        __formaters[text] = f
    return f(*a, **kw)

def _formater(text):
    def translator(k):
        if '.' in k:
            name, attr = k.split('.')
            if name.isdigit():
                k = int(name)
                return lambda *a, **kw: getattr(a[k], attr)
            return lambda *a, **kw: getattr(kw[name], attr)
        else:
            if k.isdigit():
                return lambda *a, **kw: a[int(k)]
            return lambda *a, **kw: kw[k]
    args = [translator(k) for k, _1 in new_pattern.findall(text)]
    if args:
        if old_pattern.findall(text):
            raise Exception('mixed format is not allowed')
        f = new_pattern.sub('%s', text)
        def _(*a, **kw):
            return f % tuple([k(*a, **kw) for k in args])
        return _
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        n = len(old_pattern.findall(text))
        return lambda *a, **kw: text % tuple(a[:n])

def _encode_cache_key(k):
    if isinstance(k, (bool, int, long, float, str)):
        return str(k)
    elif isinstance(k, unicode):
        return k.encode('utf-8')
    elif isinstance(k, dict):
        import urllib
        for x in k.keys():
            k[x] = _encode_cache_key(k[x])
        return urllib.urlencode(sorted(k.items()), True)
    else:
        return repr(k)

def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]
    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = _format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ', '_'), aa
    return gen_key

def cache(key_pattern, expire=expire_time):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            if settings.is_debug:
                return f(*a, **kw)
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            r = get(key)
            if r is None:
                r = f(*a, **kw)
                if r:
                    set(key, r, expire)
            return r
        _.original_function = f
        return _
    return deco

def search_cache(key_pattern, expire=expire_time):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            if settings.is_debug:
                return f(*a, **kw)
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            # key = hashlib.md5(key).hexdigest()
            r = get_search(key)
            if r is None:
                r = f(*a, **kw)
                if r:
                    set_search(key, r, expire)
            return r
        _.original_function = f
        return _
    return deco


# def statis_cache(key_pattern, expire=expire_time):
#     def deco(f):
#         arg_names, varargs, varkw, defaults = inspect.getargspec(f)
#         if varargs or varkw:
#             raise Exception("do not support varargs")
#         gen_key = gen_key_factory(key_pattern, arg_names, defaults)
#
#         @wraps(f)
#         def _(*a, **kw):
#             if settings.is_debug:
#                 return f(*a, **kw)
#             key, args = gen_key(*a, **kw)
#             if not key:
#                 return f(*a, **kw)
#             r = get_statis(key)
#             if r is None:
#                 r = f(*a, **kw)
#                 if r:
#                     set_statis(key, r, expire)
#             return r
#         _.original_function = f
#         return _
#     return deco

# 批量取内容的缓存装饰器，需以函数方式传入key唯一标示的获取方法，如
# _q = lambda x: x.get('videoid', '')
# @cache_list('test_cache_list', _q)
# def test_cache_list():
#     pass

def cache_list(key_pattern, key_func):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            # a为tuple，需将其转为list进行操作
            a = list(a)
            ids = a.pop(0) if isinstance(a[0], list) else list(a[0])
            # 用缓存key和id生成dict
            KEY_ID_DICT = dict([('{0}{1}'.format(key_pattern, i), i) for i in ids])
            _keys = KEY_ID_DICT.keys()
            # 根据缓存key，批量获取结果
            cached_rs = get_multi(_keys)
            if cached_rs:
                # 获取没有缓存的key
                no_cached_keys = do_set(_keys) ^ do_set(cached_rs.keys())
            else:
                no_cached_keys = _keys
                cached_rs = {}
            if no_cached_keys:
                # 获取没有缓存中的ids, 正常取批量获取内容函数里取结果
                no_cached_ids = [KEY_ID_DICT.get(i) for i in no_cached_keys]
                a.insert(0, no_cached_ids)
                a = tuple(a)
                no_cached_list = f(*a, **kw)
                # 根据返回结果生成‘key和结果’对应的dict
                no_cached_rs = dict([('{0}{1}'.format(key_pattern, key_func(i)), i) for i in no_cached_list])
                if no_cached_rs:
                    # 批量set到缓存
                    set_multi(no_cached_rs)
                # 更新返回结果并返回
                cached_rs.update(no_cached_rs)
            return cached_rs.values()
        return _
    return deco

def cache_list_search(key_pattern, key_func):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            # a为tuple，需将其转为list进行操作
            a = list(a)
            ids = a.pop(0) if isinstance(a[0], list) else list(a[0])
            # 用缓存key和id生成dict
            KEY_ID_DICT = dict([('{0}{1}'.format(key_pattern, i), i) for i in ids])
            _keys = KEY_ID_DICT.keys()
            # 根据缓存key，批量获取结果
            cached_rs = get_multi_search(_keys)
            if cached_rs:
                # 获取没有缓存的key
                no_cached_keys = do_set(_keys) ^ do_set(cached_rs.keys())
            else:
                no_cached_keys = _keys
                cached_rs = {}
            if no_cached_keys:
                # 获取没有缓存中的ids, 正常取批量获取内容函数里取结果
                no_cached_ids = [KEY_ID_DICT.get(i) for i in no_cached_keys]
                a.insert(0, no_cached_ids)
                a = tuple(a)
                no_cached_list = f(*a, **kw)
                # 根据返回结果生成‘key和结果’对应的dict
                no_cached_rs = dict([('{0}{1}'.format(key_pattern, key_func(i)), i) for i in no_cached_list])
                if no_cached_rs:
                    # 批量set到缓存
                    set_multi_search(no_cached_rs)
                # 更新返回结果并返回
                cached_rs.update(no_cached_rs)
            return cached_rs.values()
        return _
    return deco

def cachedfunction(cache_keys="", prefix='api#phone', suffix='fun', expire_time=settings.cache_expire_L, is_update_cache='', extkws={}):
        u"""
           cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
           prefix:前缀，suffix：后缀
           expire_time：缓存时间，defaut time 30'm
           is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
           extkws={},追加缓存参数,同名覆盖缓存参数
           is_obd:"YES" or '' ,缓存运营管理
            生成ckey的长度len不超过200
         """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_keys_list = []
                if cache_keys:
                    cache_keys_list = cache_keys.split(',')
                arg_names, varargs, varkw, defaults = inspect.getargspec(func)
                #defaults
                _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
                _args1 = dict(zip(arg_names, args))
                _kwds = dict(_defargs, **_args1)
                _kwds.update(kwargs)
                _kwds.update(extkws)
                otheragrs = []
                if varargs:
                    tmp = _args1.values()
                    otheragrs = [v for v in args if v not in tmp]
                    if otheragrs:
                        for i in xrange(0, len(otheragrs)):
                            _k = "_arg{}".format(i)
                            _kwds[_k] = otheragrs[i]

                if cache_keys_list:
                    for k, v in _kwds.items():
                        if k not in cache_keys_list:
                            _kwds.pop(k, None)
                ckey = ""
                if _kwds:
                    ckey = _encode_cache_key(_kwds)
                ckey = hashlib.md5(ckey).hexdigest()
                ckey = "{}#{}#{}".format(prefix, ckey, suffix)
                if len(ckey) > 200:
                    ckey = ckey[:200]

                try:
                    if settings.is_debug or not ckey:
                        return func(*args, **kwargs)
                    else:
                        value = None if is_update_cache.upper() == 'YES' else get(ckey)
                        if value is None:
                            value = func(*args, **kwargs)
                            if value:
                                set(ckey, value, expire_time)
                        return value
                except Exception, e:
                    #print e
                    return func(*args, **kwargs)
            wrapper.original_function = func
            wrapper.func_name = func.func_name
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator

#####################
def cachedfunction2(cache_keys, prefix='api#phone', suffix='fun', expire_time=settings.cache_expire_L,
                    is_update_cache='', extkws={},check_keys=[],condition={}, check_func=None, pool=pool0):
    u"""
       cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
       prefix:前缀，suffix：后缀
       expire_time：缓存时间，defaut time 30'm
       is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
       extkws={},追加缓存参数,同名覆盖缓存参数
       is_obd:"YES" or '' ,缓存运营管理
        生成ckey的长度len不超过200
     """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_keys_list = []
            if cache_keys:
                cache_keys_list = cache_keys.split(',')
                # 去除cache key里面的空格
                cache_keys_list = [ele.strip() for ele in cache_keys_list]
            arg_names, varargs, varkw, defaults = inspect.getargspec(func)
            #defaults
            _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
            _args1 = dict(zip(arg_names, args))
            _kwds = dict(_defargs, **_args1)
            _kwds.update(kwargs)
            _kwds.update(extkws)
            otheragrs = []
            if varargs:
                tmp = _args1.values()
                otheragrs = [v for v in args if v not in tmp]
                if otheragrs:
                    for i in xrange(0, len(otheragrs)):
                        _k = "_arg{}".format(i)
                        _kwds[_k] = otheragrs[i]

            if cache_keys_list:
                for k, v in _kwds.items():
                    if k not in cache_keys_list:
                        _kwds.pop(k, None)
            ckey = ""
            if _kwds:
                #删除不满足条件的key
                if condition:
                    for k,v in condition.iteritems():
                        if not _kwds.get(k):
                            del _kwds[v]

                ckey = _encode_cache_key(_kwds)
            ckey = hashlib.md5(ckey).hexdigest()
            ckey = "{}#{}#{}".format(prefix, ckey, suffix)
            if len(ckey) > 200:
                ckey = ckey[:200]

            try:
                if settings.is_debug or not ckey:
                    return func(*args, **kwargs)
                else:
                    value = None if kwargs.get('is_update_cache', '').upper() == 'YES' else get(ckey, pool=pool)

                    if value is None:
                        result_valid = True
                        value = func(*args, **kwargs)
                        if value:
                            if check_keys:
                                for k in check_keys:
                                    if not value.get(k,None):
                                        result_valid = False
                                        break
                            if check_func:  # 检查结果函数，根据传递的函数查看结果是否可缓存，如果函数出异常，则忽略
                                try:
                                    if not check_func(value):
                                        result_valid = False
                                except Exception as e:
                                    logging.error(e)
                                    pass
                            if result_valid:
                                set(ckey, value, expire_time, pool=pool)
                    return value
            except Exception, e:
                return func(*args, **kwargs)
        wrapper.original_function = func
        wrapper.func_name = func.func_name
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


def cachedfunction_use_memkey(mem_key, expire_time=settings.cache_expire_L,
                              is_update_cache='', check_keys=[], check_func=None, pool=pool0):
    u"""
       cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
       prefix:前缀，suffix：后缀
       expire_time：缓存时间，defaut time 30'm
       is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
       extkws={},追加缓存参数,同名覆盖缓存参数
       is_obd:"YES" or '' ,缓存运营管理
        生成ckey的长度len不超过200
     """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            ckey = mem_key

            try:
                if settings.is_debug or not ckey:
                    return func(*args, **kwargs)
                else:
                    value = None if kwargs.get('is_update_cache', '').upper() == 'YES' else get(ckey, pool=pool)

                    if value is None:
                        result_valid = True
                        value = func(*args, **kwargs)
                        if value:
                            if check_keys:
                                for k in check_keys:
                                    if not value.get(k,None):
                                        result_valid = False
                                        break
                            if check_func:  # 检查结果函数，根据传递的函数查看结果是否可缓存，如果函数出异常，则忽略
                                try:
                                    if not check_func(value):
                                        result_valid = False
                                except Exception as e:
                                    logging.error(e)
                                    pass
                            if result_valid:
                                set(ckey, value, expire_time, pool=pool)
                    return value
            except Exception, e:
                return func(*args, **kwargs)
        wrapper.original_function = func
        wrapper.func_name = func.func_name
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator

#####################
# def cachedfunction_play_secret(cache_keys, prefix='api#phone', suffix='fun', expire_time=settings.cache_expire_L,
#                     is_update_cache='', extkws={},check_keys=[],condition={}, check_func=None):
#     u"""
#        cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
#        prefix:前缀，suffix：后缀
#        expire_time：缓存时间，defaut time 30'm
#        is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
#        extkws={},追加缓存参数,同名覆盖缓存参数
#        is_obd:"YES" or '' ,缓存运营管理
#         生成ckey的长度len不超过200
#      """
#
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             cache_keys_list = []
#             if cache_keys:
#                 cache_keys_list = cache_keys.split(',')
#                 # 去除cache key里面的空格
#                 cache_keys_list = [ele.strip() for ele in cache_keys_list]
#             arg_names, varargs, varkw, defaults = inspect.getargspec(func)
#             #defaults
#             _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
#             _args1 = dict(zip(arg_names, args))
#             _kwds = dict(_defargs, **_args1)
#             _kwds.update(kwargs)
#             _kwds.update(extkws)
#             otheragrs = []
#             if varargs:
#                 tmp = _args1.values()
#                 otheragrs = [v for v in args if v not in tmp]
#                 if otheragrs:
#                     for i in xrange(0, len(otheragrs)):
#                         _k = "_arg{}".format(i)
#                         _kwds[_k] = otheragrs[i]
#
#             if cache_keys_list:
#                 for k, v in _kwds.items():
#                     if k not in cache_keys_list:
#                         _kwds.pop(k, None)
#             ckey = ""
#             if _kwds:
#                 #删除不满足条件的key
#                 if condition:
#                     for k,v in condition.iteritems():
#                         if not _kwds.get(k):
#                             del _kwds[v]
#
#                 ckey = _encode_cache_key(_kwds)
#             ckey = hashlib.md5(ckey).hexdigest()
#             ckey = "{}#{}#{}".format(prefix, ckey, suffix)
#             if len(ckey) > 200:
#                 ckey = ckey[:200]
#
#             try:
#                 if settings.is_debug or not ckey:
#                     return func(*args, **kwargs)
#                 else:
#                     value = None if kwargs.get('is_update_cache', '').upper() == 'YES' else get_play_secret(ckey)
#
#                     if value is None:
#                         result_valid = True
#                         value = func(*args, **kwargs)
#                         if value:
#                             if check_keys:
#                                 for k in check_keys:
#                                     if not value.get(k,None):
#                                         result_valid = False
#                                         break
#                             if check_func:  # 检查结果函数，根据传递的函数查看结果是否可缓存，如果函数出异常，则忽略
#                                 try:
#                                     if not check_func(value):
#                                         result_valid = False
#                                 except Exception as e:
#                                     logging.error(e)
#                                     pass
#                             if result_valid:
#                                 set_play_secret(ckey, value, expire_time)
#                     return value
#             except Exception, e:
#                 return func(*args, **kwargs)
#         wrapper.original_function = func
#         wrapper.func_name = func.func_name
#         wrapper.__doc__ = func.__doc__
#         return wrapper
#     return decorator


# def play_cachedfunction2(cache_keys, prefix='api#phone', suffix='fun', expire_time=settings.cache_expire_L, is_update_cache='', extkws={},check_keys=[]):
#     u"""
#        cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
#        prefix:前缀，suffix：后缀
#        expire_time：缓存时间，defaut time 30'm
#        is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
#        extkws={},追加缓存参数,同名覆盖缓存参数
#        is_obd:"YES" or '' ,缓存运营管理
#         生成ckey的长度len不超过200
#      """
#
#     key_body_name = "play.api.body"
#     key_expire_name = "play.api.expired_at"
#
#     def generate_cache_key(func, *args, **kwargs):
#         cache_keys_list = []
#         if cache_keys:
#             cache_keys_list = cache_keys.split(',')
#         arg_names, varargs, varkw, defaults = inspect.getargspec(func)
#         #defaults
#         _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
#         _args1 = dict(zip(arg_names, args))
#         _kwds = dict(_defargs, **_args1)
#         _kwds.update(kwargs)
#         _kwds.update(extkws)
#         otheragrs = []
#         if varargs:
#             tmp = _args1.values()
#             otheragrs = [v for v in args if v not in tmp]
#             if otheragrs:
#                 for i in xrange(0, len(otheragrs)):
#                     _k = "_arg{}".format(i)
#                     _kwds[_k] = otheragrs[i]
#
#         if cache_keys_list:
#             for k, v in _kwds.items():
#                 if k not in cache_keys_list:
#                     _kwds.pop(k, None)
#         ckey = ""
#         if _kwds:
#             ckey = _encode_cache_key(_kwds)
#         ckey = hashlib.md5(ckey).hexdigest()
#         ckey = "{}#{}#{}".format(prefix, ckey, suffix)
#         if len(ckey) > 200:
#             ckey = ckey[:200]
#         return ckey
#
#     def get_set(func, ckey, *args, **kwargs):
#         result_valid = True
#         value = func(*args, **kwargs)
#         if value:
#             if check_keys:
#                 for k in check_keys:
#                     if not value.get(k,None):
#                         result_valid = False
#                         break
#             if result_valid:
#                 short_expire_time = expire_time - settings.cache_expire_M
#                 data = {key_body_name: value,
#                         key_expire_name: int(time.time() + short_expire_time)}
#
#                 set(ckey, data, expire_time)
#         return value
#
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#
#             # 生成key
#             ckey = generate_cache_key(func, *args, **kwargs)
#
#             try:
#                 if settings.is_debug or not ckey:
#                     return func(*args, **kwargs)
#                 else:
#                     value = None if kwargs.get('is_update_cache', '').upper() == 'YES' else get(ckey)
#
#                     raw_value = {}
#                     if value:
#                         # 调试方便，使用变量
#                         is_new_cache = isinstance(value, dict) and value.has_key(key_expire_name) and value.has_key(key_body_name)
#                         if is_new_cache:
#                             raw_value = value.get(key_body_name)
#                             short_expire_time = value.get(key_expire_name)
#                             if short_expire_time > int(time.time()):  # 没有到短的过期时间点
#                                 logging.debug("*raw_value return: %s" % ckey)
#                                 return raw_value
#                         else:  # 老的兼容
#                             return value
#
#                     key_mutex = '%s_mutex' % ckey
#                     # 方便调试，使用变量
#                     lock_mutex = add(key_mutex, 1, settings.cache_expire_M)
#                     if lock_mutex:
#                         logging.debug("*mutex lock success: %s" % key_mutex)
#                         try:
#                             value = get_set(func, ckey, *args, **kwargs)
#                         except Exception,e:
#                             #如果有old value return old value
#                             if raw_value:
#                                 value = raw_value
#                             else:
#                                 raise e
#                         finally:
#                             logging.debug("delete mutex key:%s" % key_mutex)
#                             # 必须删除锁
#                             delete(key_mutex)
#                     else:
#                         logging.debug("*mutex is locked: %s" % key_mutex)
#                         if raw_value:  # 处于10分钟过期时间段之内的，并且没有锁定成功的，返回原值
#                             logging.debug("*unlocked, raw_value return: %s" % ckey)
#                             value = raw_value
#                         else:  # 旧的值过期，又没有锁定成功，只能再查询一次，很少发生
#                             logging.debug("*set cache: %s" % ckey)
#                             value = get_set(func, ckey, *args, **kwargs)
#
#                     return value
#             except Exception, e:
#                 return func(*args, **kwargs)
#         wrapper.original_function = func
#         wrapper.func_name = func.func_name
#         wrapper.__doc__ = func.__doc__
#         return wrapper
#     return decorator


def cachedfunction_plus(cache_keys, prefix='api#phone#plus', suffix='fun', expire_time=settings.cache_expire_One_Hour,
                        is_update_cache='', extkws={}):
    u"""

        函数缓存装饰器，主要目的是当真正的函数错误时，能够返回缓存的旧的值

       cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
       prefix:前缀，suffix：后缀
       expire_time：缓存时间，默认一小时
       is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
        生成ckey的长度len不超过200
     """

    def generate_cache_key(func, *args, **kwargs):
        cache_keys_list = []
        if cache_keys:
            cache_keys_list = cache_keys.split(',')
        arg_names, varargs, varkw, defaults = inspect.getargspec(func)
        #defaults
        _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
        _args1 = dict(zip(arg_names, args))
        _kwds = dict(_defargs, **_args1)
        _kwds.update(kwargs)
        _kwds.update(extkws)
        if varargs:
            tmp = _args1.values()
            otheragrs = [v for v in args if v not in tmp]
            if otheragrs:
                for i in xrange(0, len(otheragrs)):
                    _k = "_arg{}".format(i)
                    _kwds[_k] = otheragrs[i]

        if cache_keys_list:
            for k, v in _kwds.items():
                if k not in cache_keys_list:
                    _kwds.pop(k, None)
        ckey = ""
        if _kwds:
            ckey = _encode_cache_key(_kwds)
        ckey = hashlib.md5(ckey).hexdigest()
        ckey = "{}#{}#{}".format(prefix, ckey, suffix)
        if len(ckey) > 200:
            ckey = ckey[:200]
        return ckey

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # 生成key
            ckey = generate_cache_key(func, *args, **kwargs)
            expire_m = expire_time
            expire_s = None
            # 如果指定的过期时间长于两小时，则增加一小时
            if expire_m >= settings.cache_expire_Two_Hour:
                expire_s = expire_m + settings.cache_expire_One_Hour

            is_update = False
            if kwargs.get('is_update_cache', '').upper() == 'YES':
                is_update = True

            # 由于get_plus函数里面执行原始函数是没有参数的，因此这里需要包一层，然后传入一个无参函数
            def wraper_func():
                return func(*args, **kwargs)

            cached_result = get_plus(ckey, wraper_func, expire_m, expire_s, is_update)
            return cached_result
        wrapper.original_function = func
        wrapper.func_name = func.func_name
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


##########3
class CacheFragment(object):

    def __init__(self,key,model_name,expire_time=settings.cache_expire_L,is_update_cache='No',obj=None):
        self.is_update_cache = is_update_cache
        self.expire_time = expire_time
        self.model_name = model_name
        self.obj = obj
        self.key = self.gen_key(key,model_name)

    def gen_key(self,key,model_name):
        return '{0}:{1}'.format(model_name,key)

    def __enter__(self):
        if settings.is_debug or not self.key or self.is_update_cache.upper() == "YES":
            self.cache_content = None
        else:
            self.cache_content = get(self.key)
            if self.cache_content:
                print 'cache content'
            else:
                print 'no cache'

        return self.cache_content

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cache_content is None:
            set(self.key, self.obj.cache_data, self.expire_time)
