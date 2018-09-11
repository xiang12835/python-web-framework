#coding=utf-8

from web.view.base import BaseHandler , CachedPlusHandler
from web.document.doc_tools import *
from django.conf import settings
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
import tornado.web


@handler_define
class IndexHandler(BaseHandler):

    @api_define("Index", r'/', [
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),
    ], description="首页")
    def get(self):
        current_user = self.current_user

        print "******",current_user

        return self.render("Home/index.html", current_user=current_user)
