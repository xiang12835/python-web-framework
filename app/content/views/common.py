# coding=utf-8

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from app.content_operation.models import *
from django.contrib import messages
from wi_model_util.imodel import get_object_or_none
from django.core.exceptions import FieldError
from django.db.models import Max
from app.bskcommon.models import *
from app.infomation.models import *
from app.bskgk.models import *
import json
from wx.wx_content.utils import upload_file


MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


def set_position(instance, model, query_dict=None):
    if query_dict:
        try:
            position = model.objects.filter(**query_dict).aggregate(Max('position'))['position__max']
        except (FieldError, TypeError):
            position = 0
    else:
        position = model.objects.all().aggregate(Max('position'))['position__max']
    if position is None:
        position = 0
    setattr(instance, 'position', position+1)


def img_upload(request):
    if request.method == 'POST':
        file_obj = request.FILES[u'files[]']
        screenshot_type = request.POST.get("type")

        if False and screenshot_type:
            screenshot_size = "480x270" if screenshot_type == "0" else "270x480"

        remote_url = upload_file(file_obj)

        if not remote_url:
            response_data = {
                "e": {
                    "code": -1
                }
            }
        else:
            response_data = {
                "files": [
                    {
                        "name": file_obj.name,
                        "type": file_obj.content_type,
                        "size": file_obj.size,
                        "url": remote_url,
                    }
                ]
            }

        response = JSONResponse(response_data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """

    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


@login_required()
def common_update_status_str(request):
    item_id = request.POST["item_id"]
    item_class = eval(request.POST['item_class'])
    item = get_object_or_none(item_class, pk=item_id)
    if item and item.status == '1':
        item.status = '0'
    else:
        item.status = '1'
    item.save()

    resp = {
        "code": 200,
        "msg": u"操作成功！",
        "result": {
            "status": item.status,
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def common_update_status_int(request):
    item_id = request.POST["item_id"]
    item_class = eval(request.POST['item_class'])
    item = get_object_or_none(item_class, pk=item_id)
    if item and item.status:
        item.status = 0
    else:
        item.status = 1
    item.save()

    resp = {
        "code": 200,
        "msg": u"操作成功！",
        "result": {
            "status": item.status,
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def api_course_list(request):
    key = request.GET.get('key')
    course_infos = CourseInfo.objects.filter(course_name__contains=key, status="1", stage=2).order_by("-create_time")[:20]
    course_info_list = []

    for course in course_infos or []:
        course_info_list.append(course.to_small_json())

    response = HttpResponse(json.dumps(course_info_list), content_type='application/json')
    response['Content-Disposition'] = 'inline; filename=files.json'
    response["Access-Control-Allow-Origin"] = "*"

    return response


@login_required()
def api_course_list_for_activity(request):
    key = request.GET.get('key')

    course_infos = CourseInfo.objects.filter(course_name__contains=key, status="1").filter(stage__in=[1, 2]).order_by("-create_time")[:20]
    course_info_list = []

    for course in course_infos or []:
        course_info_list.append(course.to_small_json())

    response = HttpResponse(json.dumps(course_info_list), content_type='application/json')
    response['Content-Disposition'] = 'inline; filename=files.json'
    response["Access-Control-Allow-Origin"] = "*"

    return response


@login_required()
def api_course_list_for_given_course(request):
    key = request.GET.get('key')
    course_infos = CourseInfo.objects.filter(course_name__contains=key).order_by("-create_time")[:20]
    course_info_list = []

    for course in course_infos or []:
        course_info_list.append(course.to_small_json_for_given_course())

    response = HttpResponse(json.dumps(course_info_list), content_type='application/json')
    response['Content-Disposition'] = 'inline; filename=files.json'
    response["Access-Control-Allow-Origin"] = "*"

    return response
