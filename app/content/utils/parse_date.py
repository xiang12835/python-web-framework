# coding=utf-8

import datetime
from base.core.dateutils import *
import time


def parse_datetime(request):
    qd = request.GET

    start_time = qd.get("start_time", days_ago(30).strftime("%Y-%m-%d %H:%M"))
    end_time = qd.get("end_time", nature_after_days(1).strftime("%Y-%m-%d %H:%M"))

    if type(start_time) == str or type(start_time) == unicode:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')

    if type(end_time) == str or type(end_time) == unicode:
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M')

    dd = end_time - start_time
    if dd.days > 120:
        end_time = zero_date().strftime("%Y-%m-%d %H:%M")
        start_time = days_ago(120).strftime("%Y-%m-%d %H:%M")

    return start_time, end_time


def parse_int_datetime(request):
    qd = request.GET

    start_time = qd.get("start_time", days_ago(30).strftime("%Y-%m-%d %H:%M"))
    end_time = qd.get("end_time", zero_date().strftime("%Y-%m-%d %H:%M"))

    if type(start_time) == str or type(start_time) == unicode:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')

    if type(end_time) == str or type(end_time) == unicode:
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M')

    
    t = start_time.timetuple()
    start_time = int(time.mktime(t))  

    t = end_time.timetuple()
    end_time = int(time.mktime(t)) 

    return  start_time,end_time

def parse_one_day_datetime(request):
    qd = request.GET

    start_time = qd.get("start_time")

    if not start_time:
        start_time = zero_date()
    else:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d')
    
    end_time = start_time + datetime.timedelta(1)
    return start_time ,end_time



def parse_one_day(request):
    qd = request.GET

    start_time = qd.get("start_time")

    if not start_time:
        start_time = zero_date()
    else:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')
    
    end_time = start_time + datetime.timedelta(1)
    return start_time ,end_time




def parse_week_day(request):
    qd = request.GET

    start_time = qd.get("start_time")

    if not start_time:
        start_time = zero_date()
    else:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')
    
    end_time = start_time + datetime.timedelta(1)
    start_time = end_time - datetime.timedelta(7)
    return start_time ,end_time



def last_one_day(lastdate):
    start_time = lastdate - datetime.timedelta(1)
    return start_time ,lastdate



def parse_dates(request):
    qd = request.GET

    start_time = qd.get("start_time", days_ago(30).strftime("%Y-%m-%d %H:%M"))
    end_time = qd.get("end_time", zero_date().strftime("%Y-%m-%d %H:%M"))

    if type(start_time) == str or type(start_time) == unicode:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')

    if type(end_time) == str or type(end_time) == unicode:
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M')

    dates = []
    while start_time<=end_time:
        d = start_time.strftime("%Y-%m-%d")
        dates.append(d)
        start_time += datetime.timedelta(1)


    return reversed(dates)
