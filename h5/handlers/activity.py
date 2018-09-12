# coding=utf-8
from h5.views.base import BaseHandler, CachedPlusHandler
from h5.document.doc_tools import *
from django.conf import settings
import time
import datetime
from wi_model_util.imodel import attach_foreignkey, queryset_to_dict
import tornado


@handler_define
class ActivityCountDownHtml(tornado.web.RequestHandler):

    @api_define("ActivityCountDownHtml",
                r'/cdn/cache/activity/card/countdown/:id',
                [Param(':id', True, str, "1", "1", u'课程id'),
                 Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                 Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')], description="倒计时卡片")
    def get(self, xid, x):
        card = CardCountDown.objects.filter(id=xid).first()

        return self.render("countdown.html", **{"card": card})





@handler_define
class PageVoucherHtml(tornado.web.RequestHandler):

    @api_define("PageVoucherHtml",
                r'/pop/voucher/page/:id',
                [Param(':id', True, str, "1", "1", u'课程id'),
                 Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                 Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')], description="领取代金券卡片")
    def get(self, xid, x):
        item = PopVoucherPage.objects.filter(id=xid).first()
        return self.render("voucher/get_voucher.html", **{"item": item})





