#coding=utf-8

from h5.views.base import BaseHandler , CachedPlusHandler
from h5.document.doc_tools import *
from django.conf import settings
from app.bskgk.models import CourseInfo , InfoCarousel , VideoInfo
from app.bskcommon.models import BskUser
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
from app.infomation.models import *
import tornado
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from app.index.util.common import get_paged_dict
from app.index.models import Page, Application, Article, Channel, BoxTag,\
    ModuleType, TitleSkipType, TemplateType, Navbar
from app.index.models.page_item import *
from app.index.lib.short_id import ShortID
import json


@handler_define
class TopicPageHtml(tornado.web.RequestHandler):

    @api_define("CourseShareHtml", r'/t/:id',
                [
                Param(':id', True, str, "1", "1", u'pageid'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
                description="课程ShareH5")
    def get(self,short_id,x):
        
        if not short_id:
            return HttpResponseBadRequest('invalid id')

        sid = ShortID()
        page_id = sid.toID(short_id)
        page = Page.query(page_id)

        if page.folder:
            return HttpResponseBadRequest('invalid id')

        content = page.data_for_view()
        content.update({"page_id": sid.toHex(page_id), 'ptype': 'p'})

        return render(request, 'page/show.html', content)



