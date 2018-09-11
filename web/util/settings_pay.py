#!/usr/bin/python
# -*- coding: utf-8 -*-

pay_paycenter_conf = {
    'ip': '10.103.88.183',
    'host': 'premium.paycenter.youku.com',
    'key': 'b2bde3024d5584d843329062df0c3882',
}

ios_pay_paycenter_conf = pay_paycenter_conf  # 分开为了测试方便，安卓用线上测，ios得用测试环境测

pay_vrfcenter_conf = {
    'ip': '10.103.88.182',
    'host': 'premium.vrfcenter.youku.com',
    'key': 'b2bde3024d5584d843329062df0c3882',
}

ios_pay_vrfcenter_conf = pay_vrfcenter_conf  # 分开为了测试方便，安卓用线上测，ios得用测试环境测

pay_boss_conf = {
    'ip': '10.103.88.184',
    'host': 'premium.boss.youku.com',
    'key': 'b2bde3024d5584d843329062df0c3882',
}

shanghai_pay_conf = {
    'ip': '10.5.111.115',
    'host': 'zhifu.youku.com',
    'key': 'youkuwuxian',
    'trade_no': '20150323ZH02253606',
}

pay_vip_new_conf = {  # 新会员系统
    'ip': '10.100.188.59',
    'host': 'premium.api.vip.youku.com',
    'key': 'df71a3cfdb4e345e38fcf047ee038609',
    'pub_key': 'P006',
}

pay_qing_vip_conf = {  # 新轻会员系统
    'ip': '10.100.188.95',
    'host': 'vrfcenter.api.vip.youku.com',
    'key': '3e64a83bd0fc4e6981c4bdb784f6a38d',
    'pub_key': 'P008',
}

ios_send_log_server = '10.111.188.53:80'

user_grade_server = '10.100.188.105'

pay_houdong_dashang = (
    '10.103.188.98',
)