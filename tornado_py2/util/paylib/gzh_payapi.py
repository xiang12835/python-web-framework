# -*- coding: utf-8 -*-
__author__ = 'yinxing'
import hashlib
import urllib2
import random
import string
import time
import copy
import xml.etree.ElementTree as ET
import logging
from base.core.dateutils import int_days
from django.conf import settings

# doc -- https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_2
#        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_1
# test api -- http://mp.weixin.qq.com/debug/cgi-bin/readtmpl?t=pay/index&pass_ticket=Vk3Mm8MK6EcgHMomyKlmt7Rj6ktvDqMJ4VAiUleuaveLdfnQtlJDTHolUEts8nIq
# niubility -- http://www.cocoachina.com/bbs/read.php?tid=321546
# xxxxxxxxxx https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.qXxvNP&treeId=59&articleId=103663&docType=1

class GZHPayConfig(object):
    MCHID = "1330629001"
    APPID = "wx6457a8b0deb2c4e9"
    KEY = "N6gV89VvHtXPsq9ldx1MIy4HU5dhNO4x"
    SECRET = "f7a62874cc10f044acfa48f59d1a0519"

class TianJinGZHPayConfig(object):
    MCHID = "1509026971"
    APPID = "wxb136a982abd01e9f"
    KEY = "7A065671B72D66D0FE4AF05BDDC27B1E"
    #'7A065671B72D66D0FE4AF05BDDC27B1E'
    SECRET = "b756aa5035f2e044ad7a53708ef726f8"



class GZHPayBase(object):
    """
    微信支付基类
    """

    # def post_xml(self, second=30):
    #     raise NotImplementedError

    def dict_to_xml(self, param_map):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in param_map.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml):
        data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            data[child.tag] = value
        return data

    def get_sign(self, param_map):
        """生成签名"""
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        if self.is_tianjin:
            key = TianJinGZHPayConfig.KEY
        else:
            key = GZHPayConfig.KEY
    

        sign_content = "{0}&key={1}".format(content, key)
        #print sign_content
        smd5 = hashlib.md5()
        #print sign_content
        smd5.update(sign_content)
        return smd5.hexdigest().upper()

    def random_str(self):
        content = string.lowercase + string.digits
        return ''.join(random.sample(content, 16))


class GZHPayDoPay(GZHPayBase):
    """
    微信下单接口
    """
    def __init__(self,  out_trade_no, total_fee, body='buy', subject='buy', payment_type="JSAPI",ip="",openid='',is_tianjin=False,notify_url=""):
        
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

        if settings.DEBUG:
            self.notify_url = "https://h5.platform.winlesson.com/api/gzh/wx_pay/notify"
        else:
            if is_tianjin:
                self.notify_url = "https://h5.platform.winlesson.com/api/gzh/wx_pay/tianjin/notify"
            else:
                self.notify_url = "https://h5.platform.winlesson.com/api/gzh/wx_pay/notify"

        if notify_url:
            self.notify_url = notify_url

        self.out_trade_no = str(out_trade_no)
        self.subject = subject
        self.trade_type = payment_type
        self.total_fee = str(total_fee)
        self.body = body
        self.ip = ip
        self.prepay_id = ''
        self.xml = ''
        self.code_url = ''
        self.nonce_str = self.random_str()
        self.openid = openid
        self.is_tianjin = is_tianjin


    def post_xml(self, second=30):
        data = urllib2.urlopen(
            self.url, self.create_xml(),
            timeout=second).read()

        #print data
        return data

    def create_xml(self):
        """生成接口参数xml"""

        if self.is_tianjin:
            appid =  TianJinGZHPayConfig.APPID
            mch_id = TianJinGZHPayConfig.MCHID
        else:
            appid =  GZHPayConfig.APPID
            mch_id = GZHPayConfig.MCHID


        param_map = {
            'appid': appid,
            'mch_id': mch_id,
            #'spbill_create_ip': self.ip,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
            'body': self.body,
            'total_fee': self.total_fee,
            'notify_url': self.notify_url,
            'trade_type': self.trade_type,
            "sign_type": 'MD5',
        }

        

        if self.openid:
            param_map['openid'] = self.openid

        print param_map


        param_map['sign'] = self.get_sign(param_map)

        logging.error(param_map)
        self.xml = self.dict_to_xml(param_map)
        
        return self.xml


    def qr_code_xml(self,prepay_id):

        if self.is_tianjin:
            appid =  TianJinGZHPayConfig.APPID
            mch_id = TianJinGZHPayConfig.MCHID
        else:
            appid =  GZHPayConfig.APPID
            mch_id = GZHPayConfig.MCHID


        param_map = {
            "return_code":"SUCCESS",
            'appid': appid,
            'mch_id': mch_id,
            'nonce_str': self.nonce_str,
            "prepay_id":prepay_id,
            "result_code":"SUCCESS",
        }

        param_map['sign'] = self.get_sign(param_map)
        xml = self.dict_to_xml(param_map)
        return xml



    def _get_prepay_id(self):
        """获取prepay_id"""

        result = self.xml_to_dict(self.post_xml())
        #print " * " * 20
        #print result
        logging.error(result)
        result_code = result.get('result_code')
        err_code = result.get('err_code')
        if result_code != "SUCCESS":
            e = Exception()
            e.desc = result.get("return_msg","")
            e.message = result.get("return_msg","")
            logging.error(result)
            raise e

        self.prepay_id = result.get('prepay_id')
        self.nonce_str = result.get("nonce_str")
        self.code_url = result.get("code_url")
        return self.prepay_id


    def do_pay_params_dict(self):
        prepay_id = self._get_prepay_id()

        if self.is_tianjin:
            appid =  TianJinGZHPayConfig.APPID
            mch_id = TianJinGZHPayConfig.MCHID
        else:
            appid =  GZHPayConfig.APPID
            mch_id = GZHPayConfig.MCHID


        param_map = {
            'appId': appid,
            #'partnerid': GZHPayConfig.MCHID,
            'package': 'prepay_id=%s' % prepay_id,
            'nonceStr': self.nonce_str,
            'timeStamp': str(int(time.time())),
            "signType" : "MD5",
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = self.get_sign(param_map)
        param_map["paySign"] =  sign

        return param_map


    def do_pay_params(self):
        prepay_id = self._get_prepay_id()

        if self.is_tianjin:
            appid =  TianJinGZHPayConfig.APPID
            mch_id = TianJinGZHPayConfig.MCHID
        else:
            appid =  GZHPayConfig.APPID
            mch_id = GZHPayConfig.MCHID


        param_map = {
            'prepayid': prepay_id,
            'appid': appid,
            'partnerid': mch_id,
            'package': 'Sign=WXPay',
            'noncestr': self.nonce_str,
            'timestamp': str(int(time.time()))
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = self.get_sign(param_map)

        pay_params = '&'.join(['='.join(x) for x in sort_param])
        pay_params +="&sign=" + sign


        data = {
            "prepay_id": prepay_id,
            'pay_params': pay_params
        }
        return data

    def verify_notice_sign(self,xml):
        """
        校验签名
        """
        root = xml
        param_map = {}
        sign = ""
        for child in root:
            if child.tag !="sign":
                param_map[child.tag] = child.text
            else:
                sign = child.text

        we_sign = self.get_sign(param_map)

        if sign == we_sign:
            return True
        else:
            return False




class GZHPayNotice(GZHPayBase):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.recieve_param = self._format_params(
            xml_data=xml_data)

    def _format_params(self, xml_data):
        """将微信的请求xml转换成dict，以方便数据处理"""
        return self.xml_to_dict(xml=xml_data)

    def validate(self):
        """校验签名"""
        tmp = copy.deepcopy(self.recieve_param)
        del tmp['sign']
        sign = self.get_sign(tmp) #本地签名

        return self.recieve_param['sign'] == sign

    def return_data(self, data):
        """设置返回微信的xml数据"""
        return self.dict_to_xml(data)



