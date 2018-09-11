#!/usr/bin/env python
# -*- coding: utf-8 -*-

decode_client_id = 10026
#用于调用youku openapi 外网
client_id = '74c61f909cf2fcf7'
# 二维码登录加密key
passport_qrcode_key = "vy9nsq7dd1o7c0mc9ixacnweoot8pp4z"
pid = 'XMTAyOA=='
pid_auth = 'ZThiMGNhM2M3ZDVmNTAxM2Y5ZDQxNzMyZDQzZTkxMDI='

aes_key = 'v804rerzc5alkgyp'

has_history = True

cache_servers0 = ('localhost:11211',)
cache_servers1 = ('localhost:11211',)

search_cache_servers0 = (
    'localhost:11211',
    'localhost:11211',
)

# 用户中心服务器
user_center_server = [
        '10.111.88.109',
        '10.111.88.110',
        '10.111.88.111',
        '10.111.88.112',
    ]

#passport v1服务器
passport_server_v1 = "10.100.188.39"

openapi_server2 = '10.105.88.74'

play_yks_server = [  # yks server
    '10.103.188.118',
]

passport_server = [
    '10.100.188.76:80',
]

passport_thrid_part_server=[
    "10.105.88.67",
]

# ykss
ykss_server={
    "server":"10.103.88.155",
}

#restapi服务器地址，restapi.youku.com
restapi_server = "10.10.221.107:8081"

use_new_playapi_server = True

category_map = {84: u'纪录片', 96: u'电影', 97: u'电视剧', 85: u'综艺', 90: u'亲子', 91: u'资讯', 98: u'体育', 104: u'汽车',
                105: u'科技', 86: u'娱乐', 92: u'原创', 95: u'音乐', 99: u'游戏', 89: u'时尚', 88: u'旅游', 94: u'搞笑',
                100: u'动漫', 102: u'广告', 103: u'生活', 87: u'教育', 172: u'网剧', 176: u'自拍', 175: u'创意视频', 174: u'拍客',
                171: u'微电影'}

category_map_rev = dict([(y, x) for x, y in category_map.items()])

is_doc = False
is_debug = False

# 缓存超时时间, 单位秒
cache_expire_S = 60
cache_expire_MS = 60 * 5
cache_expire_M = 60 * 10
cache_expire_L = 60 * 30
cache_expire_XL = 60 * 60
cache_expire_XXL = 60 * 60 * 12
cache_expire_XXXL = 60 * 60 * 24
cache_expire_MAX = 60 * 60 * 24 * 2

cache_expire_Ten_Minute = 60 * 10
cache_expire_Twenty_Minute = 60 * 20
cache_expire_One_Hour = 60 * 60
cache_expire_Two_Hour = 60 * 60 * 2
cache_expire_Four_Hour = 60 * 60 * 4
cache_expire_One_Day = 60 * 60 * 24 * 1
cache_expire_Two_Day = 60 * 60 * 24 * 2
cache_expire_One_Week = 60 * 60 * 24 * 7
cache_expire_One_Month =  60 * 60 * 24 * 30

aes_key_user = 'lkjkcn34lici345x'