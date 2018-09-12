#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import time
import logging
import json
from python_memcache import memcache

class McJsonPickleWrapper(object):
    def __init__(self, file, protocol=None):
        self.file = file
        self.protocol = protocol

    def dump(self, value):
        import cjson

        data = cjson.encode(value)
        self.file.write(data)

    def load(self):
        import cjson

        data = self.file.read()
        return cjson.decode(data)


class MemcacheProxy(object):
    """Memcache Proxy"""

    def __init__(self, server, backup):
        #searilaize
        pickler = McJsonPickleWrapper
        unpickler = McJsonPickleWrapper

        #master
        self.mc = memcache.Client(server, pickler=pickler, unpickler=unpickler)

        #slave
        self.mc_backup = memcache.Client(backup, pickler=pickler, unpickler=unpickler)


    def add(self, *args, **kwargs):
        try:
            return self.mc.add(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.add(*args, **kwargs)


    def add_multi(self, *args, **kwargs): # real signature unknown
        """ Add multiple keys at once. """
        try:
            return self.mc.add_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.add_multi(*args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            return self.mc.get(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.get(*args, **kwargs)

    def get_multi(self, *args, **kwargs): # real signature unknown
        """ Get multiple keys at once. """
        try:
            return self.mc.get_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.get_multi(*args, **kwargs)

    def set(self, *args, **kwargs):
        try:
            return self.mc.set(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.set(*args, **kwargs)

    def set_multi(self, *args, **kwargs): # real signature unknown
        """ Set multiple keys at once. """
        try:
            return self.mc.set_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.set_multi(*args, **kwargs)


    def delete(self, *args, **kwargs):
        try:
            return self.mc.delete(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.delete(*args, **kwargs)


    def delete_multi(self, *args, **kwargs): # real signature unknown
        """ Delete multiple keys at once. """
        try:
            return self.mc.delete_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup.delete_multi(*args, **kwargs)


try:
    mc = MemcacheProxy(settings.cache_nutcracker, settings.cache_nutcracker_backup)
except Exception, e:
    logging.error(e)
    mc = None


def get_plus_json(key, func, expire_m=None, expire_s=None, is_update=False, set_retry=True, not_valid_check={}):
    key_body_name = "api.body"
    key_expire_name = "api.expired_at"

    content = None
    raw_content = None
    if not is_update:
        #get from cache pool0
        content = mc.get(key)
        if content:
            if isinstance(content, dict) and  content.has_key(key_expire_name):
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
                    return [content, ]
                else:
                    #expired to get new one
                    #if get new key exception use old one
                    logging.debug("expired %s" % key)
                    raw_content = content
                

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
                    if isinstance(result, list):
                        for r in result:
                            for k, v in not_valid_check.iteritems():
                                if r.get(k) == v:
                                    valid = False
                                    break

                if valid:
                    logging.debug("set new version data")

                    data = {key_expire_name: int(time.time() + expire_m)}
                    for r in result:
                        data.update(r)

                    logging.debug("get data add set key:%s" % key)
                    mc.set(key, data, expire_s)
                    return [data, ]
        except Exception, e:
            logging.error(e)

            if raw_content:
                logging.debug("exception use old key:%s" % key)
                if set_retry:
                    #set 10 minute retry
                    data = raw_content
                    data.update({key_expire_name: int(time.time() + settings.cache_expire_Ten_Minute)})

                    mc.set(key, data, expire_s)
                return [raw_content, ]
            else:
                #must be evctions or old key
                logging.error(e)
                raise e


    if mc.add(key_mutex, 1, settings.cache_expire_M):
        logging.debug("*mutex: %s" % key_mutex)

        try:
            raw_content = get_and_set()
        finally:
            logging.debug("delete mutex key:%s" % key_mutex)
            #delate mutex key
            mc.delete(key_mutex)
    else:
        #on key expire be mutex go here use old key to return
        logging.debug("*mutex locked: %s" % key)

        if not raw_content:
            #retry to get from func() ,normally not go here ,must be evictions
            logging.debug("* evictions: %s" % key)
            raw_content = get_and_set()

    return raw_content

