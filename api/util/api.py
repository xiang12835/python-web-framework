#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
#import cache
import hashlib
import math
import random
import re
import settings
import time
import urllib
import urllib2
import logging
import json
import string
from collections import OrderedDict

import datetime



import HTMLParser
from Crypto.Cipher import AES

#encode 专辑id
def encodeplid(plid):
    try:
        return 'P{0}'.format(base64.b64encode(str(long(plid) << 2)))
    except ValueError:
        return plid

#decode 专辑id
def decodeplid(plid):
    if isinstance(plid, (int, long)) or str(plid).isdigit():
        return long(plid)
    else:
        try:
            return long(base64.b64decode(plid[1:])) >> 2
        except TypeError:
            return 0L
#是否是专辑
def isplid(plid):
    if not isinstance(plid, (int, long, basestring)):
        return False

    if isinstance(plid, basestring):
        if not (plid.isdigit() or plid.startswith('P')):
            return False

    longid = 0L
    try:
        longid = decodeplid(plid)
    except:
        longid = 0L

    return longid > 0


def encodevid(vid):
    try:
        return 'X{0}'.format(base64.b64encode(str(long(vid) << 2)))
    except ValueError:
        return vid


def decodevid(vid):
    if isinstance(vid, (int, long)) or str(vid).isdigit():
        return long(vid)
    else:
        try:
            return long(base64.b64decode(vid[1:])) >> 2
        except TypeError:
            return 0L

def encodeuid(uid):
    try:
        return 'U{0}'.format(base64.b64encode(str(long(uid) << 2)))
    except ValueError:
        return uid

def decodeuid(uid):
    if isinstance(uid, unicode):
        uid = uid.encode('utf-8')

    if isinstance(uid, (int, long)) or str(uid).isdigit():
        return long(uid)
    else:
        try:
            return long(base64.b64decode(uid[1:])) >> 2
        except (TypeError, ValueError):
            return 0L

def isvid(vid):
    if not isinstance(vid, (int, long, basestring)):
        return False

    if isinstance(vid, basestring):
        if not (vid.isdigit() or vid.startswith('X')):
            return False

    # longid = 0L
    # try:
    #     longid = decodevid(vid)
    # except:
    #     longid = 0L
    #
    # return longid > 0
    return True


def isshowid(showid):

    # if showid.startswith("z"):
    #     showid=showid[1:]
    return bool(_p_showid.match(showid))


def reputation(up, down, fav, comm):
    u"""
        好评(0~9.99)
        算法：LOG((1-踩/(踩+收藏+评论))*10*LOG10(顶+踩+收藏+评论) ,1.5)
        如果得分>9.99，则得分＝9.99
        踩+收藏+评论<10,则为0
    """

    result = 0

    try:
        if not down + fav + comm < 10:
            result = math.log((1 - float(down) / (down + fav + comm)) * 10 * math.log10(up + down + fav + comm), 1.5)
            result = 9.99 if result > 9.99 else result
    except ValueError:
        # 如果fav,comm==0，那么直接为0
        result = 0

    return max(result, 0)

def fmt_vv_pv(vv):
    try:
        vv = float(vv)
    except Exception as e:
        pass
        vv = 0
    if vv < 10 ** 4:
        vv = int(vv)
    if vv >= 10 ** 4 and vv < 10 ** 8:
        return u'{0}万'.format(round(vv / 10000, 1))
    if vv >= 10 ** 8:
        return u'{0}亿'.format(round(vv / 100000000,1))
    return '{0}'.format(vv)

def fmt_comment(vv):
    try:
        vv = int(vv)
    except Exception as e:
        pass
        vv = 0
    if vv >= 10 ** 4 and vv < 10 ** 8:
        return u'{0}万'.format(round(vv / 10000, 1))
    if vv >= 10 ** 8:
        return u'{0}亿'.format(round(vv / 100000000), 1)
    return '{0}'.format(vv)

def fmt_duration(seconds):
    u""" 将视频时长转换成mm:ss的形式 """

    # 容错，防止传空字符串
    if not seconds:
        seconds = 0

    if isinstance(seconds, basestring) and ':' in seconds:
        return seconds
    try:
        seconds = float('{0}'.format(seconds))
    except Exception as e:
        logging.error(e)
        seconds = 0
        pass
    return '{0:0>2}:{1:0>2}'.format(*divmod(int(seconds), 60))


def fmt_duration2(seconds):
    u""" 将视频时长转换成hh:mm:ss的形式 """
    try:
        seconds = float('{0}'.format(seconds))
    except Exception as e:
        logging.error(e)
        seconds = 0
        pass

    h, seconds = divmod(int(seconds), 3600)
    m, s = divmod(int(seconds), 60)
    return '{0:0>2}:{1:0>2}:{2:0>2}'.format(h, m, s)

def parse_duration(duration):
    m, s = duration.split(':') if duration else (0, 0)
    return float(int(m) * 60 + int(s))

def cid_name(cid):
    """ ddeprecated """
    cid = int(cid) if isinstance(cid, basestring) else cid
    return cid2name(cid)

def cid2name(cid):
    assert isinstance(cid, int)
    return settings.category_map.get(cid, '')

def name2cid(name):
    assert isinstance(name, unicode)
    return settings.category_map_rev.get(name, 0)

def cid_list():
    cidlist = [int(k) for k, v in settings.category_map.items()]
    return cidlist

def ftype_name(fmt):
    _sep = ',' if ',' in fmt else ' '
    mapping = {1: 'hd', 2: '3gp', 3: 'flv', 4: '3gphd', 5: 'flvhd', 6: 'm3u8'}
    if fmt:
        fmt = _sep.join([mapping.get(int(x)) for x in re.split(r'[,\s]', fmt)])
        return urllib.quote(fmt)
    else:
        return ''

def api_server():
    """api.youku.com"""
    return settings.openapi_server

def api2_server():
    return settings.openapi_server2

def api3_server():
    """api.youku.com"""
    return settings.openapi_server3

#    server_list = settings.openapi_server2
#    return server_list[random.randint(0, len(server_list) - 1)]

def random2dserver():
    """ random translate shorturl server"""
    server_list = settings.qr_server
    return server_list[random.randint(0,len(server_list)-1)]

def comment_server():
    u"""评论接口服务器地址"""
    servers = [
        #新评论系 统 VIP
        '10.111.188.23',
        # '10.111.88.105',
        # '10.111.88.106',
        # '10.111.88.107',
        # '10.111.88.108',
        # '10.103.55.121',
        # '10.103.55.122',
        # '10.103.55.123',
        # '10.103.55.124',
        # '10.103.15.1',
        # '10.103.15.2',
        # '10.103.15.3',
        # '10.103.15.4',
        # '10.103.15.5',
        # '10.103.15.6',
        # '10.103.15.7',
        # '10.103.15.8',
        # '10.103.15.9',
        # '10.103.15.10',
    ]
    return servers[random.randint(0, len(servers) - 1)]

def vv_counter_server():
    return random.choice(settings.vvcounter_server)

def hudong_dashang_server():
    return random.choice(settings.pay_houdong_dashang)

def vv_counter_server_read():
    return random.choice(settings.vvcounter_server_read)

def vv_counter_server_read_new():
    return random.choice(settings.vvcounter_server_read_new)

def passport_vip_server():
    return settings.passport_vip

def tweet_server():
    u"""用户中心服务器地址"""
    # servers = [
    #     #'10.103.17.51', 数据有问题
    #     '10.103.17.52',
    #     '10.103.17.53',
    #     '10.103.17.54',
    #     '10.103.17.55',
    #     '10.103.17.56',
    #     '10.103.17.57',
    #     '10.103.17.58',
    # ]
    servers = settings.user_center_server
    return servers[random.randint(0, len(servers) - 1)]

def anonym_subscribe_server():
    u"""匿名用户订阅"""
    servers = settings.user_subscribe_server
    return servers[random.randint(0, len(servers) - 1)]

def subscribe_server():
    u"""用户订阅vip"""
    servers = settings.user_subscribe_server
    return servers[random.randint(0, len(servers) - 1)]


def cinema_ticket_server():
    return random.choice(settings.cinema_ticket_server)

def weiying_ticket_server():
    return random.choice(settings.weiying_server)

def user_im_server():
    servers = settings.user_im_server
    return servers[random.randint(0, len(servers) - 1)]


def user_like_server():
    servers = settings.user_like_server
    return servers[random.randint(0, len(servers) - 1)]


def user_custom_server():
    servers = settings.user_custom_server
    return servers[random.randint(0, len(servers) - 1)]

def user_center_batch_server():
    u"""用户中心服务器地址，主要是批量功能服务的服务器"""
    servers = [
        '10.103.55.136',
        '10.103.55.137',
        '10.103.55.138',
        '10.103.55.139',
    ]
    return servers[random.randint(0, len(servers) - 1)]

def samsung_vip_server():
    return settings.samsung_vip_server

def soku_server():
    return '10.103.88.151'

def soku_server2():
    # return '10.103.88.154'
    # return '10.103.88.154'
    # servers = (
    #     '10.103.8.26',
    #     '10.103.8.27',
    #     '10.103.8.111',
    #     '10.103.8.112',
    #     '10.103.8.63',
    # )
    # return random.choice(servers)
    return '10.103.88.142'

def soku_server2_direct():
    """
    新的搜库直达区搜索服务器vip
    """
    return settings.soku_server

def soku_keyword_rcommand():
    """
    搜库关键词推荐
    """
    return '10.103.88.154'

def tip_soku_server():
    u"""搜索关键词提示接口"""
    servers = [
        # tip.so.youku.com
        '10.103.8.219',
        '10.103.8.220',
        # tip.soku.com # 以后切换到这个服务器
        #'10.103.8.226',
        #'10.103.8.227',
    ]
    return servers[random.randint(0, len(servers) - 1)]


def tip_soku_server_new():
    """
    http://wiki.1verge.net/das:soku:api:kubox-v2
    """
    return '10.103.88.189'

def passport_server():
    u"""passport接口"""
    servers = settings.passport_server
    return random.choice(servers)

def passport_auth_user_server():
    u"""passport 验证用户cookie接口"""
    servers = settings.passport_auth_user_server
    return random.choice(servers)

def passport_server2():
    u"""passport手机注册接口"""
    # return '10.103.88.136'
    return '10.105.88.67'  # 替换为新的

def passport_server_qrcode():
    """
        二维码扫描
    """
    servers = settings.passport_server_qrcode

    return random.choice(servers)

def passport_thrid_part_server():
    """
        第三方登录服务器
    """
    servers = settings.passport_thrid_part_server

    return random.choice(servers)

def data_rec_server():
    # servers = [
    #
    #     '10.103.55.125',
    #     '10.103.55.126',
    #     '10.103.55.127',
    #     '10.103.55.128',

        # '10.103.22.71',
        # '10.103.22.73',
        # '10.103.22.74',
        # '10.103.22.75',
        # '10.103.22.76',
        # '10.103.22.77',
        # '10.103.22.79',
        # '10.103.22.80',
        # '10.103.22.81',
        # '10.103.22.82',
        # '10.103.22.90',
#        '10.103.22.41',
#        #'10.103.22.42',
#        '10.103.22.43',
#        '10.103.22.44',
#        '10.103.22.45',
#        '10.103.22.46',
#        '10.103.22.47',
#        '10.103.22.48',
#        '10.103.22.49',
#        '10.103.22.50',
    #]
    servers = settings.das_server
    return servers[random.randint(0, len(servers) - 1)]

def sid_server():
    sid_servers = [
        '10.103.188.39',
        '10.103.188.40',
        '10.103.188.41',
        '10.103.188.42',
    ]
    return random.choice(sid_servers)

def notify_server():
    servers = [
        '10.103.188.58',
    ]
    # return servers[random.randint(0, len(servers) - 1)]
    return servers[0]

def search_game_server():
    """搜索接口，搜索游戏服务器"""
    return random.choice(settings.search_game_server)

def internal_server():
    return settings.internal_server

def cms_server(is_new=False):
    u"""cms接口服务器"""
    if is_new:
        return random.choice(settings.new_cms_server)
    else:
        return settings.cms_server['server']

def cms_switch_server():
    u"""cms接口服务器"""
    return random.choice(settings.cms_switch_server)

# def cms_server_wp_index():
#     u'''cms服务器wp接口测试'''
#     return settings.cms_wp_index_test['server']


def umc_server():
    return settings.umc_server['server']


def box_cms_server():
    """
    box cms 接口服务器
    """
    return settings.box_cms_server["server"]

def cms_django_server():
    u""" cms_django 服务器接口"""
    return settings.cms_django_server["server"]

def yus_server():
    u"""yus接口服务器"""
    return playlog_yus()


def session_server():
    return settings.ykss_server["server"]

def lbs_server():
    u"""lbs服务器"""
    #return '10.103.13.121:6003'
    #return 'lbs.m.youku.com'
    return '10.103.13.122'

def shorurl_server():
    u"""短域名服务器"""
    #servers = [
        #'10.103.17.87:8004',
        #'10.103.17.88:8004',
    #    "10.105.88.12",
    #]
    servers = settings.qr_server
    return servers[random.randint(0, len(servers) - 1)]

def v_server():
    u"""v.youku.com"""
    servers = settings.v_server
    return random.choice(servers)

def play_yks_server():
    u"""v.youku.com"""
    servers = settings.play_yks_server
    # servers = settings.play_yks_server_test
    return random.choice(servers)

def passport2_server():
    u"""批量取第三方好友绑定关系的server地址"""
    #return '10.103.88.179:8070'
    return settings.passport_server_v1


def playlog_yus():
    u"""云存储服务器地址"""
#    _servers = [
#        '211.151.146.157',
#        '211.151.146.158',
#        '211.151.146.159',
#        '211.151.146.160',
#        '211.151.146.161',
#        '211.151.146.162',
#    ]

    return random.choice(settings.play_log_server)

def view_duration_server():
    """
        用户观看时长
    """

    return random.choice(settings.viewdura_server)


def middle_server_0():
    u"""中间层服务地址"""
    return settings.middle_server_0


def exchange_server():
    """
        换量新系统API
    """
    return random.choice(settings.exchange_server)

def mainsite_server():
    u"""youku指数接口服务器"""
    return settings.mainsite_server['server']

def http2rtsp(playurl):
    _items = playurl.split('?K=')[0].split('/')
    if 'f.youku.com' in _items:
        _fn = '{0}.{1}'.format(_items[-1], _items[8])
    else:
        _fn = '/'.join(_items[3:])

    _index = hash_djb(_items[-1]) % 2 + 1

    # 调用prefetcher接口
    # FIXME: 取消rtsp的调用
    #try:
    #    _prefetcher_path = 'http://go.youku.com/stream/Prefetcher?f={0}&s={1}'
    #    _prefetcher_path = _prefetcher_path.format(_fn, _index)
    #    urllib2.urlopen(_prefetcher_path, timeout=1)
    #except:
    #    pass

    return 'rtsp://vod{0}.3g.youku.com/{1}'.format(_index, _fn)

def hash_djb(s):
    _hash = 5381
    for x in s:
        _hash = ((_hash << 5) + _hash) + ord(x)
    _hash &= 0x7FFFFFFF
    return _hash

def code2field(code, codetype):
    """code: short code list of fields
    codetype: [video|show]"""
    assert isinstance(code, list)

    code_mapping = {
        'show': settings.show_fields_code,
        'video': settings.videos_fields_code,
    }.get(codetype, {})

    _result = []
    for c in code:
        _result.append(code_mapping.get(c, ''))
    _result = filter(lambda x: bool(x), _result)
    return _result

def code2field_extension(code, codetype):
    """code: short code list of fields
    codetype: [video|show]"""
    assert isinstance(code, list)

    show_dict = settings.show_fields_code.copy()
    #add new field
    show_dict.update({"showsubtitle": "showsubtitle", "day_vv": "showday_vv", "week_vv": "showweek_vv",
                      "ryar": "releaseyear", 'showsum_vv': 'showsum_vv'})
    code_mapping = {
        'show': show_dict,
        'video': settings.videos_fields_code,
    }.get(codetype, {})

    _result = []
    for c in code:
        _result.append(code_mapping.get(c, ''))
    _result = filter(lambda x: bool(x), _result)
    return _result


def fix_show_fields(shows, fields):
    if not fields:
        return

    fields = fields.split('|')
    fields = code2field(fields, 'show')

    shows = shows if isinstance(shows, list) else [shows]

    for r in shows:
        for k in r.keys():
            if k not in fields:
                del r[k]


def video_limit(limits):
    u"""
        0 : 不作限制 (对应2进制数0)
        1 : 禁下载 (对应2进制数1)
        2 : 禁评论 (对应2进制数10)
        3 : 禁下载和评论 (对应2进制数11)
        4 : 版权限制，不允许在当前设备上播放 (对应2进制数100)
    """
    result = 0
    mapping = {'DOWNLOAD_DISABLED': 1, 'COMMENT_DISABLED': 2}
    for l in limits:
        result |= mapping.get(l, 0)
    return result


#def show_comment_add_time(millsSeconds):
#    ms = int(time.time()) - millsSeconds
#    if ms > 2592000:
#        tmpStr = str(ms / 2592000) + u'个月前'
#    elif ms > 604800:
#        tmpStr = str(ms / 604800) + u'周前'
#    elif ms > 86400:
#        tmpStr = str(ms / 86400) + u'天前'
#    elif ms > 3600:
#        tmpStr = str(ms / 3600) + u'小时前'
#    elif ms > 60:
#        tmpStr = str(ms / 60) + u'分钟前'
#    else:
#        tmpStr = u'1分钟前'
#    return u'发表于' + tmpStr


def format_timeline_day(seconds):

    import time,datetime

    today=datetime.date.today()
    dd = time.localtime(seconds)
    date = datetime.date(dd.tm_year,dd.tm_mon,dd.tm_mday)

    sub_days=(today-date).days

    time_bottom=""
    if sub_days==0:
        time_bottom=u"今天(周{})".format(date.isoweekday())
    elif sub_days==1:
        time_bottom=u"昨天(周{})".format(date.isoweekday())
    else:
        time_bottom=date.isoformat()

    return time_bottom


def format_timeline_day_str(datestr):
    import datetime

    today=datetime.date.today()
    date_arr = datestr.split("-")
    date = datetime.date(int(date_arr[0]),int(date_arr[1]),int(date_arr[2]))

    sub_days=(today-date).days

    time_bottom=""
    if sub_days==0:
        time_bottom=u"今天(周{})".format(date.isoweekday())
    elif sub_days==1:
        time_bottom=u"昨天(周{})".format(date.isoweekday())
    else:
        time_bottom=date.isoformat()

    return time_bottom

def format_nextviewsdruation(mins):

    p,m = divmod(mins,60)
    next_viewdura_str="距升级还需"
    if p>0:
        next_viewdura_str=next_viewdura_str+"{}小时".format(p)
    if m>0:
        next_viewdura_str +="{}分钟".format(m)

    return next_viewdura_str

def format_nowviewsduration(mins,percent):

    # p,m = divmod(mins,60)
    # now_viewdura_str=""
    # if p>0:
    #     now_viewdura_str="{}小时".format(p)
    # if m>0:
    #     now_viewdura_str +="{}分钟".format(m)

    # return "已经观看{}{}的小伙伴给你跪了".format(now_viewdura_str,percent)

    if mins:
        return u"已看{}分钟，领先{}的用户".format(mins,percent)
    else:
        return "今天尚未观看视频哦"

def format_pay_expire_time(endtime):
    endtime_obj = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endtime, "%Y-%m-%d %H:%M:%S")))
    now = datetime.datetime.now()
    total_espire_seconds = int((endtime_obj - now).total_seconds())

    if total_espire_seconds < 60*60:
        expire_time = u'观看有效期1小时以内'

    elif total_espire_seconds > 60*60 and total_espire_seconds< 48*60*60:
        expire_time_ = math.ceil(float(total_espire_seconds)/3600)
        expire_time = u'观看有效期{}小时'.format(int(expire_time_))

    else:
        expire_time_ = math.ceil(float(total_espire_seconds)/3600)
        expire_time = u'观看有效期{}小时'.format(int(expire_time_))

    return expire_time



def show_comment_add_time(millsSeconds,isTimeLine=False):
    year = 31104000
    month = 2592000
    week = 604800
    day = 86400
    hour = 3600
    minute = 60
    ms = int(time.time()) - millsSeconds

    if isTimeLine:

        ms_date = time.localtime(int(millsSeconds))
        if ms>7*day:
            tmpStr =time.strftime("%Y-%m-%d %H:%M:%S",ms_date)
        elif ms > day:
            tmpStr = str(ms / day) + u'天前'
        elif ms > hour:
            tmpStr = str(ms / hour) + u'小时前'
        elif ms > minute:
            tmpStr = str(ms / minute) + u'分钟前'
        else:
            tmpStr = u'1分钟前'
        return tmpStr
    else:

        if ms > year:
            tmpStr = str(ms / year) + u'年前'
        elif ms > month:
            tmpStr = str(ms / month) + u'个月前'
        elif ms > week:
            tmpStr = str(ms / week) + u'周前'
        elif ms > day:
            tmpStr = str(ms / day) + u'天前'
        elif ms > hour:
            tmpStr = str(ms / hour) + u'小时前'
        elif ms > minute:
            tmpStr = str(ms / minute) + u'分钟前'
        else:
            tmpStr = u'1分钟前'
        return u'发表于' + tmpStr


def format_timeline_video_published(publised):
    #publised like "2013-09-02 15:56:16"

    if not publised:
        return u"1分钟前"

    published = datetime.datetime.strptime(publised,"%Y-%m-%d %H:%M:%S")

    now  = datetime.datetime.now()

    sub_date = now - published

    days = sub_date.days

    seconds = sub_date.seconds

    if days<1 and seconds:
        if seconds>60*60:
            h,m = divmod(seconds,60*60)

            if h>0:
                return u"{}小时前".format(h)
            else:
                return u"{}分钟前".format(m)
        else:
            m,s=divmod(seconds,60)
            if m>0:
                return u"{}分钟前".format(m)
            else:
                return u"1分钟前"

    elif days>=1 and days<7:
        return u"{}天前".format(days)

    else:
        return publised

def formatSokuPersonBirthday(birthday):
    """
        birthday "1984-01-12"
        如果 “0000-12-11” 返回“12-11”
    """
    ret = u''
    if birthday:
        birthday_arr = birthday.split("-")
        if birthday_arr[0]=="0000":
            ret = "-".join(birthday_arr[1:])
        else:
            ret = birthday
    if ret == u'00-00':
        ret = ''
    return ret


def fix_comment_content(content):
    if content:
        if _p_comment_quote.search(content):
            content = _p_comment_quote.sub(r'//\1', content)
        if _p_comment_reply.search(content):
            content = _p_comment_reply.sub(r'@\1', content)

    return content

def fix_user_name(username):
    if username and _p_user_name_type.search(username):
        username = _p_user_name_type.sub('', username)
    return username

def ua2client(user_agent):
    #默认值
    clientInfoCode = 999
    if user_agent:
        uaDict = {
            r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad': 1,
            r'Youku;[^;]+;Android': 2,
            r'Youku;[^;]+;iPhone OS;[^;]+;iPod': 3,
            r'Youku;[^;]+;iPhone OS;[^;]+;iPhone': 4,
            r'SymbianOs': 5,
            r'BlackBerry': 6,
            r'Youku HD;[^;]+;Android': 7,
            r'Paike{1}.*Android{1}.*': 1002,
            r'Paike{1}.*iPhone{1}.*': 1004,
        }
        for k in uaDict.keys():
            if re.search(k, user_agent):
                clientInfoCode = uaDict[k]
                break

    return clientInfoCode

def ua2Ad_type(user_agent):
    u"""广告type{ 0:'unknown', 1:'iPhone', 2:'Android'} """
    #目前只分iPhone，Android
    clientInfoCode = 0
    if user_agent:
        #从上到下精确匹配
        uaDict = {
            r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad': 1,
            r'Youku;[^;]+;iPhone OS;[^;]+;iPhone': 1,
            r'Youku;[^;]+;iPhone OS;[^;]+;iPod': 1,
            r'Youku;[^;]+;iPhone OS;[^;]+;': 1,
            r'Youku HD;[^;]+;iPhone OS': 1,
            r'Youku HD;[^;]+;Android;': 2,
            r'Youku;[^;]+;Android': 2,
            r'Paike{1}.*iPhone{1}.*': 1,
            r'Paike{1}.*Android{1}.*': 2,
            r'iPhone.*': 1,
            r'Android.*': 2,

        }
        for k in uaDict.keys():
            if re.search(k, user_agent):
                clientInfoCode = uaDict[k]
                break
    return clientInfoCode

def ua2device_type(user_agent):
    u"""
    hwclass    int    硬件类型：
            0:保留
            1:pc
            2:tv(电视)
            3:pad(平板)
            4:phone(手机)
            9:unknown
    """
    clientInfoCode = 9
    if user_agent:
        odlist = [
            #####################################
            ### 添加 tv
            #####################################
            (r'Android_SmartTV',2),
            (r'Youku;[^;]+;Android_SmartTV',2),
            (r"Youku SmartTV;[^;]+",2),

            (r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad',3),
            (r'Youku HD;[^;]+;Android', 3),
            (r'Youku;[^;]+;Android', 4),
            (r'Youku;[^;]+;iPhone OS;[^;]+;iPod', 4),
            (r'Youku;[^;]+;iPhone OS;[^;]+;iPhone', 4),
            (r'Youku;[^;]+;iPhone OS;[^;]+;iPhone', 4,),
            (r'Youku;[^;]+;WindowsPhone;[^;]+', 4,), # 增加wp平台ua
            (r'SymbianOs', 4,),
            (r'BlackBerry', 4,),
            (r'Paike{1}.*Android{1}.*', 4,),
            (r'Paike{1}.*iPhone{1}.*', 4,),
            (r'iPhone.*',4,),
            (r'Android.*',4,),
        ]
#        uaDict = {
#            r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad':3,
#            r'Youku HD;[^;]+;Android': 3,
#            r'Youku;[^;]+;Android': 4,
#            r'Youku;[^;]+;iPhone OS;[^;]+;iPod': 4,
#            r'Youku;[^;]+;iPhone OS;[^;]+;iPhone': 4,
#            r'SymbianOs': 4,
#            r'BlackBerry': 4,
#            r'Paike{1}.*Android{1}.*': 4,
#            r'Paike{1}.*iPhone{1}.*': 4,
#            r'iPhone.*':4,
#            r'Android.*':4,
#        }
        uaDict = OrderedDict(odlist)
        for k in uaDict.keys():
            if re.search(k, user_agent):
                clientInfoCode = uaDict[k]
                break

    return clientInfoCode

def ua2device_all_type(user_agent):
    u"""
        1: iPad
        2: iPhone
        3: Android Pad
        4: Android Phone
        5: Windows Phone
        9: unknown
    """
    clientInfoCode = 9
    if user_agent:
        uaDict = {
            r'Youku HD;[^;]+;iPhone OS': 1,
            r'Youku;[^;]+;iPhone OS': 2,
            r'Youku HD;[^;]+;Android': 3,
            r'Youku;[^;]+;Android': 4,
        }
        for k in uaDict.keys():
            if re.search(k, user_agent):
                clientInfoCode = uaDict[k]
                break

    return clientInfoCode

def ua2device_name(user_agent):
    #默认值   
    devicename = 'UNKNOWN'
    if user_agent:
        uaDict = {
            #####################################
            ### 添加 tv
            #####################################
            r'Android_SmartTV':"SmartTV",
            r'Youku;[^;]+;Android_SmartTV':"SmartTV",
            r"Youku SmartTV;[^;]+":"SmartTV",

            r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad': 'iPad',
            r'Youku HD;[^;]+;Android': 'Android Pad',
            r'Youku;[^;]+;iPhone OS;[^;]+;iPod': 'iPod',
            r'Youku;[^;]+;iPhone OS;[^;]+;iPhone': 'iPhone',
            r'SymbianOs': 'SymbianOs',
            r'BlackBerry': 'BlackBerry',
            r'Youku;[^;]+;Android': 'Android Phone',
            r'Paike{1}.*Android{1}.*': 'Android',
            r'Paike{1}.*iPhone{1}.*': 'iPhone',
            r'iPhone.*':'iPhone',
            r'Android.*':'Android',
        }
        for k in uaDict.keys():
            if re.search(k, user_agent):
                devicename = uaDict[k]
                break
    return devicename

def get_os_id(os):
    if os=='iPhone OS':
        return '1'
    elif os=='Android':
        return '2'
    else:
        return '3'

def ua2device_id(user_agent):
    device_id = 'NA'
    if user_agent:
        uaDict = {
            r'Youku HD;[^;]+;iPhone OS;[^;]+;iPad': '5',
            r'Youku HD;[^;]+;Android': '7',
            r'Youku HD;[^;]+;WindowsPhone': '10',
            r'Youku;[^;]+;iPhone OS;[^;]+;iPod': '4',
            r'Youku;[^;]+;iPhone OS;[^;]+;iPhone': '4',
            r'Youku;[^;]+;Android': '6',
            r'Youku;[^;]+;WindowsPhone': '10',
            r'iPhone.*':'4',
            r'Android.*':'6',
        }
        for k in uaDict.keys():
            if re.search(k, user_agent):
                device_id = uaDict[k]
                break
    return device_id

def content_len(content):
    u"""计算给定内容的长度"""
    assert isinstance(content, basestring)
    if not isinstance(content, unicode):
        content = content.decode('utf-8')
    return len(content)

def fmt_need_filter(fmt):
    u""" 验证给定的格式是否需要过滤（支持全站视频的格式不需要过滤）"""
    flag = False
    if isinstance(fmt, list):
        for x in fmt:
            flag = flag or fmt_need_filter(x)
    elif isinstance(fmt, int):
        flag = fmt not in (5, 6) # flvhd, m3u8
    elif isinstance(fmt, basestring):
        flag = fmt not in ('', '5', '6') # flvhd, m3u8
    else:
        assert isinstance(fmt, (list, basestring, int))

    return flag

# def is_m3u8_64k(client, version):
#     global _wireless_m3u8_64k_cache_key
#     _data = cache.get(_wireless_m3u8_64k_cache_key)
#     if isinstance(_data, dict) and client in _data:
#         return _data[client] == version
#     else:
#         return False
#
# def need_m3u8_64k(user_agent):
#     info = user_agent.split(';')
#     if len(info) == 5 and info[2] == 'iPhone OS':
#         if info[0] == 'Youku':
#             client = 'iphone'
#         elif info[0] == 'Youku HD':
#             client = 'ipad'
#         else:
#             client = ''
#
#         version = info[1]
#         return is_m3u8_64k(client, version) if client else False
#     else:
#         return False

# def get_m3u8_64k():
#     global _wireless_m3u8_64k_cache_key
#     return cache.get(_wireless_m3u8_64k_cache_key)
#
# def add_m3u8_64k(client, version):
#     global _wireless_m3u8_64k_cache_key
#     _data = cache.get(_wireless_m3u8_64k_cache_key)
#     if not isinstance(_data, dict):
#         _data = {}
#     _data[client] = version
#     return cache.set(_wireless_m3u8_64k_cache_key, _data, settings.cache_expire_MAX)
#
# def del_m3u8_64k(client):
#     global _wireless_m3u8_64k_cache_key
#     _data = cache.get(_wireless_m3u8_64k_cache_key)
#     if isinstance(_data, dict) and client in _data:
#         del _data[client]
#
#     if _data:
#         return cache.set(_wireless_m3u8_64k_cache_key, _data, settings.cache_expire_MAX)
#     else:
#         return cache.delete(_wireless_m3u8_64k_cache_key)

def build_weburl(vid):
    return 'http://v.youku.com/v_show/id_{0}.html'.format(vid)

def build_webplayer_url(vid,platform,backurl):
    """generate webplayer url with the given vid"""
    return 'http://v.youku.com/v_show/id_{vid}.html?x&adapter={adapter}&backurl={backurl}'.format(vid=vid,
        adapter=platform,
        backurl = backurl,
    )
def build_web_uplayer_url(vid,platform='android',format='3gphd'):
    """generate web uplayer url with the given vid"""
    #backurl=youku://&name=zchongv&pwd=fadceec322e548d95b62e8798065d8f6 for ios
    return 'http://v.youku.com/v_show/id_{vid}.html?x&adapter={adapter}&backurl=youku://'.format(vid=vid,
        adapter=platform,
    )
    #return 'http://v.youku.com/youkuplayer/YoukuPlayer.html?vid={0}&adapter={1}&format={2}'.format(vid,platform,format)

def build_status_url(statusid):
    return 'http://i.youku.com/m/{0}'.format(statusid)

_xcaller_map = {
    'Youku;Android': 'gphone',
    'Youku;iPhone OS': 'iphone',
    'Youku HD;Android': 'apad',
    'Youku HD;iPhone OS': 'ipad',
    'Paike;Android': 'paike_gphone',
    'Paike;iPhone OS': 'paike_iphone',
}
_p_ua_xcaller = re.compile(r'(Youku|Youku HD|Paike);([\d.]+);([^;]+);')

def ua2xcaller(user_agent):
    u"""通过User-Agent生成X-Caller"""
    xcaller = '3in1.mobile.others'
    if user_agent:
        m = _p_ua_xcaller.match(user_agent)
        if m:
            project_name, project_version, os_name = m.groups()
            key = ';'.join([project_name, os_name])
            if key in _xcaller_map:
                project_version = '_'.join(project_version.split('.'))
                xcaller = '3in1.mobile.{}.{}'.format(_xcaller_map[key], project_version)

    return xcaller

FORMAT_ID_TO_FORMAT_MAP = {
        1: 'hd',
        2: '3gp',
        3: 'flv',
        4: '3gphd',
        5: 'flvhd',
        6: 'm3u8',
}

def convert_img_url(img):
    u"""
        由视频截图由小图转大图
        http://wiki.1verge.net/v2:thumb
    """
    old_img_pattern = r'(http://g[1-4]\.ykimg\.com/)0(1)'
    mo = re.match(old_img_pattern, img)
    if mo:
        img = mo.re.sub(r'\g<1>1\g<2>', img)
    else:
        new_img_pattern = 'http://res.mfs.ykimg.com/050'
        if img.startswith(new_img_pattern):
            trans = string.maketrans('159BD', '26ACE')
            char_28 = img[28].translate(trans)
            img = ''.join([new_img_pattern, char_28, img[29:]])
        
    return img

def total_vvformat(vv):
    u"""播放量显示方式"""

    # 容错，防止传空字符串
    if not vv:
        vv = 0
    try:
        vv = float(vv)
    except Exception as e:
        logging.error(e)
        vv = 0
    if vv >= 10 ** 4 and vv < 10 ** 8:
        return u'{0}万'.format(round(vv / 10000, 1))
    if vv >= 10 ** 8:
        return u'{0}亿'.format(round(vv / 100000000, 1))
    return u'{0}'.format(int(vv))

def validate_email(email):
    email_re = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", re.IGNORECASE)
    rs = email_re.findall(email)
    if len(rs) == 1:
        return True
    return False

# 传入show_name，show_info必须是unicode编码的
def get_trunc_words(show_name, show_info, show_max_len=5):
    if not show_name:
        return show_info
    if len(show_name) > show_max_len:
        return show_info
    return u"{0} {1}".format(show_name, show_info)

def show_bottom_info(is_variety, comp, total, last):
    u'''
    根据是否完成comp，总多少集total，最新集last返回两种类型剧集情况
    show_type为1的时候是少数情况，在综艺娱乐的节目里
    '''
    if last == 0:
        return ''
    # 综艺
    if is_variety:
        if comp == 1:
            return u'全{0}期'.format(total)
        else:
            last = str(last)
            if re.match(r'20\d{6}', last):
                return  u'更新至{0}{1}'.format(last[4:6], last[6:])
            elif len(last) >= 6:
                return  u'{0}'.format(last)   
            else:
                return  u'更新至{0}'.format(last)   
    # 电视剧, 动漫
    else:
        if comp == 1 and total == last:
            return u'全{0}集'.format(total)
        else:
            return u'更新至{0}'.format(last)

def stripe_bottom_ios(cid, completed, total, last):

    if cid == 96 and total == 1:
        return ''

    if cid == 85:#综艺的情况
        if completed == 1:
            return u'%s集全' % total
        else:
            last = str(last)
            if re.match(r'20\d{6}', last):
                return u'更新至{0}-{1}'.format(last[4:6], last[6:])
            else:
                return u'更新至{0}期'.format(last)
    else:
        if completed == 1:
            return u'%s集全' % total
        else:
            return u'更新至{0}集'.format(last)

# 根据时长估算标清、高清、超清的视频大小
def file_size(duration):
    u''' 
    文件大小（字节） = 时长（秒） X 码率（比特） / 8 
    码率：
    flvhd（标清）: 250
    mp4          : 500
    hd           : 1000
    注意码率单位KB/S，返回大小为B
    '''
    size = (float(duration) * 250 / 8) * 1024
    size = 1 if size < 1 else size
    vdsize = int(size * 1.2)
    hdsize = int(size *  1.05) * 2
    hd2size = int(size) * 4
    return (vdsize, hdsize, hd2size)

def valid_guid(guid):
    if not guid:
        return False

    return bool(re.match(r'^[a-f0-9]{32}$', guid))

def valid_ua(ua):
    if not ua:
        return False

    try:
        items = ua.split(';')
        if not len(items) == 5:
            return False

        if items[0] not in ['Youku', 'Youku HD', 'Paike', 'WAP']:
            return False
    except:
        return False

    return True

def cmp_product_ver(v1, v2):

    try:
        # 安卓电信定制机中得版本号，必须带这个字符串为后缀，所以去掉。
        v1 = v1.replace('ctch1', '')
        v2 = v2.replace('ctch1', '')

        arr1 = v1.split('.')
        arr2 = v2.split('.')
        if len(arr1) > len(arr2):
            for i in range(len(arr1) - len(arr2)):
                arr2.append(0)
        elif len(arr1) < len(arr2):
            for i in range(len(arr2) - len(arr1)):
                arr1.append(0)
            
        for a, b in zip(arr1, arr2):
            result = cmp(int(a), int(b))
            if result != 0:
                return result
        return 0
    except Exception as e:
        # logging.exception(e)
        return 0


def recommend_without_login_server(guid):
    servers_83 = [
        '10.103.22.83:81',
        '10.103.22.83:82',
    ]
    servers_84 = [
        '10.103.22.84:81',
        '10.103.22.84:82',
    ]
    last_bit = guid[-1]
    if last_bit.isdigit():
        if int(last_bit)%2 == 0:
            server = random.choice(servers_84)
        else:
            server = random.choice(servers_83)

    else:
        if int(ord(last_bit))%2 == 0:
            server = random.choice(servers_84)
        else:
            server = random.choice(servers_83)

    return server


def dealHtmlValue(name):

    result=""
    try:
        if "&lt" in name:
            html_parser = HTMLParser.HTMLParser()
            result = html_parser.unescape(name)
        else:
            result = name
    except:
        result=name

    return result


_wireless_m3u8_64k_cache_key = 'api_cache_key_of_m3u8_64k'
_p_comment_quote = re.compile("\[quote\](.*?)\[/quote\]", re.I | re.M)
_p_comment_reply = re.compile("\[reply\](.*?)\[/reply\]", re.I | re.M)
_p_user_name_type = re.compile('\{.+?\}')
_p_showid = re.compile(r'^[a-f0-9]{20}$')


def isemail(data):
    return re.match(r"([^@]+@[^@]+\.[^@]+)",data) is not None


def ismobile(data):
    # return re.match(r"1\d{10}",data) is not None
    return re.match(r"^1[3587]\d{9}$|^147\d{8}$", data) is not None


def encrypt(data):
    str_data = json.dumps(data)
    if len(str_data) % 16 != 0:
        blank = ' ' * (16-len(str_data) % 16)
        str_data += blank
    obj = AES.new(settings.aes_key_user)
    raw = obj.encrypt(str_data)
    data = base64.b64encode(raw)
    return data


def decrypt(data, key=settings.aes_key_user):
    raw = base64.b64decode(data)
    obj = AES.new(key) # 'lkjhg12yuiw734nx'
    real = obj.decrypt(raw)
    return real


def zero_add(num):
    if num < 10:
        num = '0' + str(num)
    return num

# 返回时间差值（时分秒）
def time_delta_hms(create_time, collage_hour):
    end_time = create_time + datetime.timedelta(hours=+collage_hour)
    now_time = datetime.datetime.now()

    if now_time > end_time:
        return False

    time_delta = end_time - now_time
    time_delta = time_delta.days * 86400 + time_delta.seconds
    time_hours = time_delta / 3600

    if time_hours >= collage_hour:
        return False

    time_minutes = (time_delta - 3600 * time_hours) / 60
    time_seconds = (time_delta - 3600 * time_hours) - 60 * time_minutes

    time_hours = zero_add(time_hours)
    time_minutes = zero_add(time_minutes)
    time_seconds = zero_add(time_seconds)

    return ":".join(map(str, (time_hours, time_minutes, time_seconds)))

