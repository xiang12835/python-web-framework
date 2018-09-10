# coding=utf-8

import json
import re

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from app.bskgk.utils import redefine_item_pos
from app.index.lib.short_id import ShortID
from app.index.util.common import get_paged_dict
from wx.wx_content.libs.template_msg import WeixinTemplateMessage
from django.conf import settings


appid = settings.WX_TEMPLATE_SETTINGS["appid"]
secret = settings.WX_TEMPLATE_SETTINGS["secret"]


@login_required
def my_template_list(request):
    qd = request.GET
    t = WeixinTemplateMessage(appid, secret)
    datas = t.post_my_template_list()
    datas = datas.get("list", [])
    for data_dict in datas:
        content_str = data_dict.get("content", "")
        kw_count = content_str.count("keyword")
        # print kw_count
        data_dict["kw_count"] = kw_count

        kw_desc_list = []
        for item in content_str.split('\n'):
            if not item:
                continue
            kw_desc_list.append(item.split('{{')[0])
        # print kw_desc_list
        data_dict["kw_desc_list"] = kw_desc_list

    context = {
        "datas": datas
    }
    return render(request, 'my_template/my_template_list.html', context)


@login_required
def template_keywords(request):
    if request.method == 'POST':
        qd = request.POST

        # 发送模版消息
        t = WeixinTemplateMessage(appid, secret)
        template_id = qd.get("itemid", "")
        kw_count = qd.get("kw_count", "0")
        kw_count = int(kw_count) if kw_count else 0
        touser = "oakPr0KZeIEM8YD2TkZsLxKsQUQQ"

        # data = {
        #     "keyword1": {
        #         "value": "【2018省考】线上冲刺押题班",
        #     },
        #     "keyword2": {
        #         "value": "2018年03月17日 12:30",
        #     },
        #     "keyword3": {
        #         "value": "大斌哥",
        #     }
        # }

        data = {}
        keys = []
        for i in xrange(1, int(kw_count)+1):
            keys.append("keyword"+str(i))
        for k in keys:
            d = {}
            d["value"] = qd.get(k, "")
            data[k] = d
        # print data

        form_id = "form_id"
        r = t.send_template_msg(touser, template_id, data, form_id, page='', color='', emphasis_keyword='')
        print r

        # 正常时的返回JSON数据包示例：
        #
        # {
        #   "errcode": 0,
        #   "errmsg": "ok"
        # }

        msg = ""
        if r.get("errcode") != 0:
            msg = "发送失败"

        if msg:
            datas = []
            for i in xrange(1, kw_count + 1):
                tup = ("keyword" + str(i), "关键词" + str(i))
                datas.append(tup)

            context = {
                "template_id": template_id,
                "kw_count": kw_count,
                "datas": datas,
                "msg": msg
            }

            return render(request, 'my_template/template_keywords.html', context)

        else:
            return HttpResponseRedirect(reverse("my_template_list"))
    else:
        qd = request.GET
        template_id = qd.get("template_id", "")
        kw_count = qd.get("kw_count", "0")
        kw_count = int(kw_count) if kw_count else 0

        datas = []
        for i in xrange(1, kw_count+1):
            tup = ("keyword"+str(i), "关键词"+str(i))
            datas.append(tup)

        context = {
            "template_id": template_id,
            "kw_count": kw_count,
            "datas": datas,
            "msg": ""
        }

        return render(request, 'my_template/template_keywords.html', context)
