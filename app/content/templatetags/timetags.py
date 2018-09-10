#coding=utf-8

from django import template
import datetime
register = template.Library()

def print_timestamp(timestamp):
    if not timestamp:
      return ""

    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        ts = float(timestamp)/1000
        return datetime.datetime.fromtimestamp(ts)


def platform_str(platform):
   platform_dict = {2:"ios",1:"android"}
   return platform_dict.get(platform,"其他")

def order_stats_str(platform):
   platform_dict = {'2':"成交",'1':"下单",'0': "创建"}
   return platform_dict.get(platform,"其他")


def page_type_str(platform):
   platform_dict = {'0':"快速出题",'1':"真题",'2': "模考", "10": "无尽刷题"}
   return platform_dict.get(str(platform),"其他")

def senconds_format(seconds):
    if not seconds:
      return ''

    seconds = float(seconds)
    if seconds<=60:
        return "1分钟"
    else:
         return "%.2f分钟"  % (seconds / 60 )


register.filter(print_timestamp)
register.filter(platform_str)
register.filter(order_stats_str)
register.filter(page_type_str)
register.filter(senconds_format)




