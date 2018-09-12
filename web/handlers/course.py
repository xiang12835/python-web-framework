#coding=utf-8

from web.views.base import BaseHandler , CachedPlusHandler
from web.document.doc_tools import *
from django.conf import settings
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
import tornado


@handler_define
class IndexHandler(tornado.web.RequestHandler):

    @api_define("Index", r'/course',
                [
                Param('course_id', False, str, "", "", u'课程id'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
                description="首页")
    def get(self,x=''):
        course_id = self.get_argument('course_id','')
        return self.render("Course/course.html", **{})









