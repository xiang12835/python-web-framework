# coding=utf-8

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from app.bskgk.models import OrderInfo
from app.index.models.application import Application
from base.core.dateutils import *
from django.contrib import messages
import json
from django.db import connections
import datetime
from app.index.lib.download_csv import UnicodeWriter,Echo, output_csv
from django.views.generic import View
from django.http.response import StreamingHttpResponse
from app.user.libs.check_role import check_role_required
from app.user.models import User
from app.bskcommon.models import VoucherEntity
from app.bskgk.models import SellPush
import logging


def my_custom_stat_sql(sql):
    cursor = connections["statstic"].cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def my_custom_sql(sql,db="bskgk_slave"):
    cursor = connections[db].cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def my_custom_one_sql(sql,db="bskgk_slave"):
    cursor = connections[db].cursor()
    cursor.execute(sql)
    rows = cursor.fetchone()
    cursor.close()
    return rows


class SqlExecute(object):

    @classmethod
    def fetch_all(cls, sql, db="bskgk"):
        cursor = connections[db].cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    @classmethod
    def fetch_one(cls, sql, db="bskgk"):
        cursor = connections[db].cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        return row

    @classmethod
    def execute_many(cls, sql, params, db="bskgk"):
        cursor = connections[db].cursor()
        cursor.executemany(sql, params)
        cursor.close()
