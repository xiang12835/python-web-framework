#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
import thread
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import types
import re
import string
import logging
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
import settings

SERVICE_SELECTION = 0

class ThreadMappedPool(dict):

    def __new__(cls, master):
        return super(ThreadMappedPool, cls).__new__(cls)

    def __init__(self, master):
        self.master = master

    @property
    def current_key(self):
        return thread.get_ident()

    @contextmanager
    def reserve(self):
        """Reserve a client.

        Creates a new client based on the master client if none exists for the
        current thread.
        """
        key = self.current_key
        mc = self.pop(key, None)
        if mc is None:
            mc = self.master.clone()
        try:
            yield mc
        finally:
            self[key] = mc

    def relinquish(self):
        """Relinquish any reserved client for the current context.

        Call this method before exiting a thread if it might potentially use
        this pool.
        """
        return self.pop(self.current_key, None)

# transport
_trans = None

def transport(reconn=False):
    global _trans
    if reconn or not (_trans and _trans.isOpen()):
        _trans = TSocket.TSocket(**settings.thrift_server)
        logging.debug("http://%s:%s" % (settings.thrift_server['host'], str(settings.thrift_server['port'])))
        _trans = TTransport.TBufferedTransport(_trans)
        _trans.open()
    return _trans

def protocol(trans):
    return TBinaryProtocol.TBinaryProtocolAccelerated(trans)

def service(sname, protocol):
    def deco(fn):
        def f(*args, **kwargs):
            protocol.writeMessageBegin(sname, SERVICE_SELECTION, 0)
            result = fn(*args, **kwargs)
            protocol.writeMessageEnd()
            return result
        return f
    return deco

def register_service_client():
    u"""service目录下XXXService.py文件中的 Client，Iface 类"""
    p_map = {}
    i_method = {}
    service_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../service')
    #只取service dir name
    valid_service = [x.split('.')[0] for x in os.listdir(service_dir) if re.match(r'^[a-zA-Z0-9_-]+$', x)]
    for s in valid_service:
        i_list = []
        _prename = string.capwords(s)
        #service下klass包名
        h_module_name = 'service.{0}.{1}Service'.format(s, _prename)
        h_module = __import__(h_module_name, fromlist=['Client'])
        service_client_class = h_module.Client
        _module_name = service_client_class.__base__.__module__
        p_map[s] = service_client_class
        i_module = __import__(_module_name, fromlist=['Iface'])
        service_iface_class = i_module.Iface
        for k, v in service_iface_class.__dict__.iteritems():
            if type(v) is types.FunctionType:
                i_list.append(k)
        i_method[s] = i_list
    return p_map, i_method

#test
#service_client_map, service_iface_map = register_service_client()

