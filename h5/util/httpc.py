#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import cStringIO
import pycurl
import httplib
import tempfile
import urllib2
import socket
import traceback

class HTTPError(Exception):
    def __init__(self, code, message=None, response=None):
        self.code = code
        message = message or httplib.responses.get(code, "Unknown")
        self.response = response
        Exception.__init__(self, "HTTP %d: %s" % (self.code, message))

class HTTPRequest(urllib2.Request):
    def __init__(self, url, method='GET', headers=None, body=None, timeout=None, callback=None, cookie_jar=None, timeout_ms=False):
        self.url = url
        self.method = method.upper()
        self.headers = headers and headers.copy() or {}
        self.user_agent = self.headers.get('User-Agent', None) or 'api.3g.youku.com/3.0'
        self.accept_encoding = self.headers.get('Accept-Encoding', None) or 'gzip'
        self.body = body
        self.timeout = timeout
        self.timeout_ms = timeout_ms
        self.callback = callback
        self.cookie_jar = cookie_jar

        if cookie_jar is not None:
            # cookiejar needs the methods
            urllib2.Request.__init__(self, url, headers=self.headers)

        # logging
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            trace_msg = '{} (line {})'.format(*traceback.extract_stack(limit=3)[0][:2])
            log_msg = '{} {} {}'.format(self.method, self.url, self.body or '')
            logging.debug(trace_msg)
            logging.debug(log_msg)


class HTTPResponse(object):
    def __init__(self, request, code, headers=None, buffer=None, request_time=-1):
        self.request = request
        self.code = code
        self.headers = headers and headers.copy() or {}
        self.buffer = buffer
        self.request_time = request_time
        self._body = None

        # logging
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug('Cost Time: {}s'.format(self.request_time))

    @property
    def body(self):
        if self.buffer is not None and self._body is None:
            self._body = self.buffer.getvalue()
        else:
            self._body = ''
        return self._body

    def __repr__(self):
        attrs = ', '.join(['{0}={1}'.format(x, repr(y)) for (x, y) in self.__dict__.iteritems()])
        return '{0}({1})'.format(self.__class__.__name__, attrs)

class _HeaderHander(object):
    def __init__(self):
        self._headers = []

    def info(self):
        u"""invoked by cookiejar"""
        return self

    def getheaders(self, name):
        u"""invoked by cookiejar"""
        return [x.split(':', 1)[1].strip() for x in self._headers if x.startswith(name + ':')]

    def add_header(self, header_line):
        header_line = header_line.strip()
        if header_line:
            if header_line.startswith('HTTP/'):
                self._headers = []
            else:
                self._headers.append(header_line)

def _do_request(req):
    assert isinstance(req, HTTPRequest)

    curl = pycurl.Curl()

    curl_options = {
        "GET": pycurl.HTTPGET,
        "POST": pycurl.POST,
        "PUT": pycurl.UPLOAD,
        "HEAD": pycurl.NOBODY,
    }   
    custom_methods = set(["DELETE"])
    for o in curl_options.values():
        curl.setopt(o, False)
    if req.method in curl_options:
        curl.unsetopt(pycurl.CUSTOMREQUEST)
        curl.setopt(curl_options[req.method], True)
    elif req.method in custom_methods:
        curl.setopt(pycurl.CUSTOMREQUEST, req.method)
    else:
        raise KeyError('unknown method ' + req.method)

    curl.setopt(pycurl.URL, req.url.encode('utf-8'))
    curl.setopt(pycurl.USERAGENT, req.user_agent)
    if hasattr(pycurl, 'ACCEPT_ENCODING'):
        # pycurl.version_info()[2] > 464134: # 7.21.6
        curl.setopt(pycurl.ACCEPT_ENCODING, req.accept_encoding)
    else:
        curl.setopt(pycurl.ENCODING, req.accept_encoding)
    req.headers.pop('User-Agent', None)
    req.headers.pop('Accept-Encoding', None)
    curl.setopt(pycurl.HTTPHEADER, ['{0}:{1}'.format(x, y) for (x, y) in req.headers.iteritems()])

    req_timeout = req.timeout or int(socket.getdefaulttimeout() or 0)
    if req.timeout_ms:
        if req_timeout:
            curl.setopt(pycurl.NOSIGNAL, 1)
            curl.setopt(pycurl.TIMEOUT_MS, req_timeout)
    else:
        if req_timeout:
            curl.setopt(pycurl.TIMEOUT, req_timeout)

    if req.method in ("POST", "PUT"):
        curl.setopt(pycurl.POSTFIELDS, req.body.encode('utf-8'))

    resp_buffer = cStringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, resp_buffer.write)
    header_handler = _HeaderHander()

    curl.setopt(pycurl.HEADERFUNCTION, header_handler.add_header)

    try:
        curl.perform()

        http_code = curl.getinfo(pycurl.HTTP_CODE)
        total_time = curl.getinfo(pycurl.TOTAL_TIME)
        resp = HTTPResponse(req, http_code, buffer=resp_buffer, request_time=total_time)

        if req.cookie_jar is not None:
            req.cookie_jar.extract_cookies(header_handler, req)

        if http_code >= 400:
            he = HTTPError(http_code, response=resp)
            raise he

        if req.callback:
            req.callback(resp)
        return resp
    except pycurl.error as e:
        e_code, e_msg = e.args
        if e_code == 28:
            resp = HTTPResponse(req, 408)
            he = HTTPError(408, response=resp, message=e_msg)
            raise he
        else:
            raise e

def _do_aysn_request(req):
    # TODO: 异步请求
    return None

def get(url, **kwargs):
    kwargs['method'] = 'GET'
    req = HTTPRequest(url, **kwargs)
    return _do_request(req)

def post(url, data, **kwargs):
    kwargs['method'] = 'POST'
    kwargs['body'] = data
    req = HTTPRequest(url, **kwargs)
    return _do_request(req)

def put(url, data, **kwargs):
    kwargs['method'] = 'PUT'
    kwargs['body'] = data
    req = HTTPRequest(url, **kwargs)
    return _do_request(req)

def delete(url, **kwargs):
    kwargs['method'] = 'DELETE'
    req = HTTPRequest(url, **kwargs)
    return _do_request(req)

