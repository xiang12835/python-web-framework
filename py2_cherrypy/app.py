# coding=utf-8

import cherrypy


class HelloWorld(object):
    def index(self):
        return "Hello World!"

    index.exposed = True


conf = {'global': {'server.socket_port': 8000, 'server.socket_host': 'localhost'}}

cherrypy.config.update(conf)
cherrypy.quickstart(HelloWorld())
