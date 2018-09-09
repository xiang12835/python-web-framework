# -*- coding: utf-8 -*-

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

class WePayConfig(object):
    MCHID = "1360564702"
    APPID = "wxb3d762ce7e312921"
    KEY = "LBHjaJ0lNJivKlkobMS4rf7ApR7FruAv"



class WePayBase(object):
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
        sign_content = "{0}&key={1}".format(content, WePayConfig.KEY)
        #print sign_content
        smd5 = hashlib.md5()
        #print sign_content
        smd5.update(sign_content)
        return smd5.hexdigest().upper()

    def random_str(self):
        content = string.lowercase + string.digits
        return ''.join(random.sample(content, 16))


class WePayDoPay(WePayBase):
    """
    微信下单接口
    """
    def __init__(self,  out_trade_no, total_fee, body='buy', subject='buy', payment_type="APP",ip="",openid=''):
        
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

        if settings.DEBUG:
            self.notify_url = "http://test.api.platform.winlesson.com/api/live/wepay/notice"
        else:
            self.notify_url = "http://api.platform.winlesson.com/api/live/wepay/notice"

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


    def post_xml(self, second=30):
        data = urllib2.urlopen(
            self.url, self.create_xml(),
            timeout=second).read()

        #print data
        return data

    def create_xml(self):
        """生成接口参数xml"""
        param_map = {
            'appid': WePayConfig.APPID,
            'mch_id': WePayConfig.MCHID,
            'spbill_create_ip': self.ip,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
            'body': self.body,
            'total_fee': self.total_fee,
            'notify_url': self.notify_url,
            'trade_type': self.trade_type
        }

        if self.openid:
            param_map['openid'] = self.openid


        param_map['sign'] = self.get_sign(param_map)
        self.xml = self.dict_to_xml(param_map)
        
        return self.xml


    def qr_code_xml(self,prepay_id):
        param_map = {
            "return_code":"SUCCESS",
            'appid': WePayConfig.APPID,
            'mch_id': WePayConfig.MCHID,
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



    def do_pay_params(self):
        prepay_id = self._get_prepay_id()
        param_map = {
            'prepayid': prepay_id,
            'appid': WePayConfig.APPID,
            'partnerid': WePayConfig.MCHID,
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




class WePayNotice(WePayBase):
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


class WeXinNativeLink(object):
    """静态链接二维码"""

    url = None #静态链接

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def __init__(self, paySettings):
        self.parameters = {}
        self.APPID = paySettings["wx_app_id"]
        self.APPSECRET = paySettings["wx_app_secret"]
        self.MCHID = paySettings["wx_mch_id"]
        self.KEY = paySettings["wxpay_key"]

    def setParameter(self, parameter, parameterValue):
        """设置参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)


    def createLink(self):
        if any(self.parameters[key] is None for key in ("product_id", )):
            raise ValueError("missing parameter")

        self.parameters["appid"] = self.APPID  #公众账号ID
        self.parameters["mch_id"] = self.MCHID  #商户号
        time_stamp = int(time.time())
        self.parameters["time_stamp"] = "{0}".format(time_stamp)  #时间戳
        self.parameters["nonce_str"] = self.random_str()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名          
        bizString = self.formatBizQueryParaMap(self.parameters, False)
        self.url = "weixin://wxpay/bizpayurl?"+bizString

    def getUrl(self):
        """返回链接"""
        self.createLink()
        return self.url


    def random_str(self):
        content = string.lowercase + string.digits
        return ''.join(random.sample(content, 16))

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)


    def getSign(self, obj):
        """生成签名"""
        #签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        #签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String,self.KEY)
        #签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        #签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_



