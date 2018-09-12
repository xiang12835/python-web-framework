#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import StringIO
import pycurl
import httpc

# import json
# import urllib
# import urllib2
# import socket

def get(path, timeout=0, default=''):
    """Deprecated: see util.httpc"""
    try:
        resp = httpc.get(path, timeout=timeout)
        content = resp.body
    except Exception as e:
        logging.error(path)
        logging.exception(e)
        content = default
    return content


# class HttpClient(object):
#
#     """
#     http 公共请求lib，主要是统一日志打印格式
#     """
#
#     @classmethod
#     def get_request(cls, url, params=None, timeout=None):
#
#         path = url
#         if params:
#             path = url + "?" + urllib.urlencode(params)
#         try:
#             if timeout:
#                 content = urllib2.urlopen(path, timeout=timeout).read()
#             else:
#                 content = urllib2.urlopen(path).read()
#             return json.loads(content)
#         except Exception, e:
#             error_info = "%s:%s" % (url, e)  # 记录日志格式
#             logging.error(error_info)
#             raise e
