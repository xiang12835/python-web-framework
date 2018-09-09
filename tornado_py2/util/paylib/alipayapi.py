# -*- coding: utf-8 -*-
__author__ = 'yinxing'
import urllib
import hashlib
import urllib2
import logging
import os,sys
#doc https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.qXxvNP&treeId=59&articleId=103663&docType=1
#sign https://doc.open.alipay.com/doc2/detail?treeId=58&articleId=103242&docType=1
#doc precreate
#https://doc.open.alipay.com/docs/api.htm?spm=a219a.7395905.0.0.zt7lcf&docType=4&apiId=862
import rsa
import base64
from base.core.dateutils import int_days
from datetime import datetime
import json

class AliPayConfig(object):
    """
    支付宝 公共配置
    """
    APP_ID = '2016030301179248'
    precreate_GATEWAY="https://openapi.alipay.com/gateway.do?"
    SIGN_TYPE = "RSA"
    INPUT_CHARSTE = "utf-8"
    KEY = 'fzsimh6f6q207tcdnvbsvgh99kr2mnmi'
    SELLER_ID = "channels@winlesson.com"
    PARTNER = "2088022823001725"
    ALI_SERVICE_PATH = "https://mapi.alipay.com/gateway.do"
    PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
    MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAMiwSjKsll1c5tUw0T0v7Cln+huCnZNlEM4PS0v3R66xBARy6yPyWfyQRtcTg5MOaHXHK4SwOYp9XgkQAbLxFnOPgGYxgKyMmQ7C1pOTYsJz+r9tsnm9pvRQfTk2xFHzj0frFSyLLUFZccgfqkf/6IsRYj+3HQOB2yFTdeR/vQVLAgMBAAECgYAPh0yGdUJBQSH/VwKpuF6OqaP5ovasZAKT3y0VWLHsO3gzG+1D38nEuCkzFSh2JYRBsMKWRsh9BcxT6TAod20kKt+T5hEdnNK1DhQN/n3KV2wSgQ/MeFEZBUFS86v1/u8gplcCn0fLTZgAzqeuqksmuUP/0/+zg28gp3KqrQ46KQJBAONxspvy3LZ6QjxKfp87jWJrEUbZhC8WE4UJOGUgQPHau/uBydqt6UuyCSfpYqQ1AfQb2GZ5C8lyLSFgoa81W98CQQDh4qQnf/7jyPvWz1JdOC2WG+0Y8wg61hLOQ0bJ697H/y6EuFdQ6W4YYq9vrT3oJ5hwr+iaN9t+Um8X0MyyswQVAkAOQ30eBpcM4pHw0gMq3UM6nthQhyehBFNpDnD49pLcGAmd9j/AdROiaaHlXN+QyLo8otppYsH4ei6WX0cEg+YlAkEAoteO2+MMUA5+b5e6mvV697JeNRRPpIrbt9MMX1kpnCi80nVKjUwbUH0kWHAeJxUUcnh+SV9nXyPybsraJyGjGQJBAJstDdf5bshInVq37YKG6Xs/MR7NRefmsTqd0us77uSP9HKgdxAiNyIavRQ98S/PU270xMCSdbST9CuIYNSnwMo=
-----END RSA PRIVATE KEY-----'''


class AliPayBase(object):
    """
    支付宝api 基类
    """
    def get_sign(self, param_map, sign_type="RSA"):
        #对参数排序

        import OpenSSL
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, AliPayConfig.PRIVATE_KEY)
 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8') #这三句：解决签名方法编码报错

        sign = base64.encodestring(OpenSSL.crypto.sign(private_key, content, 'sha256'))
        # private_key = rsa.PrivateKey.load_pkcs1(AliPayConfig.PRIVATE_KEY)
        # sign = rsa.sign(content, private_key, 'SHA-1')
        # ssn = base64.urlsafe_b64encode(sign)
        # print ssn
        ssn = urllib.quote_plus(sign)
        return ssn

    def create_request_data(self):
        raise NotImplementedError

    def post_data(self):
        """
        标准post 可以自己实现 ,需要定义 self.create_request_data()
        """
        data = self.create_request_data()
        try:
            result = urllib2.urlopen(
                AliPayConfig.ALI_SERVICE_PATH,
                data=urllib.urlencode(data)).read()
        except Exception, e:
            logging.error("post data error %s %s" % (data['service'],e))

        return result


class AliPayDoPay(AliPayBase):
    """
    支付宝 下单接口封装
    """
    def __init__(self, out_trade_no, subject, total_fee, body='buy', payment_type=1,sign_type="RSA"):
        self.service = "mobile.securitypay.pay"
        self.notify_url = "http://api.platform.winlesson.com/api/live/alipay/notice"
        self.out_trade_no = out_trade_no
        self.subject = subject
        self.payment_type = payment_type
        self.total_fee = total_fee
        self.body = body
        self.sign_type = sign_type

    def create_request_data(self):
       
        param_map = {
            'service':'"mobile.securitypay.pay"',
            '_input_charset':'"utf-8"',
            'notify_url':'"'+self.notify_url+'"',
            'out_trade_no':'"'+str(self.out_trade_no)+'"',
            'subject':'"'+self.subject+'"',
            'payment_type':'"'+str(self.payment_type)+'"',
            'seller_id':'"'+AliPayConfig.SELLER_ID+'"',
            'total_fee':'"'+str(self.total_fee)+'"',
            'partner':'"'+str(AliPayConfig.PARTNER)+'"',
            'body':'"'+str(self.body)+'"',
        }
        return param_map

        

    def do_pay_params(self):
        params = self.create_request_data()
        
        _sign = self.get_sign(param_map=params)
        params["sign_type"] =  '"RSA"'
        params["sign"] =  '"' + _sign + '"'

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in params.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        #result
        data = {
            "pay_params": content
        }
        return data


class AliPayDoQrCodePay(AliPayBase):
    """
    支付宝 下单接口封装
    """
    def __init__(self, orderid, goodsName, goodsPrice):
        self.notify_url = "http://api.platform.winlesson.com/api/live/alipay/notice"
        self.precreate_GATEWAY = "https://openapi.alipay.com/gateway.do?"
        self.orderid = orderid
        self.goodsName = goodsName
        self.goodsPrice = goodsPrice

    #获取二维码url
    def getAlipayUrl(self):
        # 构建公共参数
        import requests

        params = {}
        params['method'] = 'alipay.trade.precreate'
        params['version'] = '1.0'
        params['app_id'] = AliPayConfig.APP_ID
        params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['charset'] =  'utf-8'
        params['notify_url'] = self.notify_url
        params['sign_type'] = 'RSA2'

        # 构建订单参数
        biz_content = {}
        biz_content['out_trade_no'] = self.orderid  # 订单号
        biz_content['subject'] = self.goodsName  #商品名
        biz_content['total_amount'] = self.goodsPrice  # 价格
        params['biz_content'] = biz_content

        #由参数，生成签名，并且拼接得到下单参数字符串
        encode_params = self.make_payment_request(params)

        #下单
        url = self.precreate_GATEWAY + encode_params

        response = requests.get(url)
        print " * " * 20
        print response.text

        #提取下单响应
        body = response.text
        #解析下单响应json字符串
        body_dict = json.loads(body)
        return_msg = body_dict['alipay_trade_precreate_response']['msg']
        if return_msg == "Success":
                code_url = body_dict['alipay_trade_precreate_response']['qr_code']
                return code_url
        else:
            print "fail msg=============" + return_msg



    #1：生成下单请求参数字符串
    def make_payment_request(self,params_dict):
        """
        构造支付请求参数
        :param params_dict:
        :return:
        """
        query_str = self.params_to_query(params_dict,)  # 拼接参数字符串
        sign = self.make_sign(query_str)  # 生成签名
        sign = urllib.quote(sign, safe='')  #解决中文参数编码问题
        res = "%s&sign=%s" % (query_str, sign)
        return res



    def params_to_query(self,params):
        """
        生成需要签名的字符串
        :param params:
        :return:
        """
        """
        :param params:
        :return:
        """
        query = ""
        dict_items = {}
        for key, value in params.items():
            if isinstance(value, dict) == True:
                dict_items[key] = value
                params[key] = "%s"
        all_str = ''
        for key in sorted(params.keys()): #把参数按key值排序：这是支付宝下单请求的参数格式规定
            all_str = all_str + '%s=%s&' % (key, params[key])
        all_str = all_str.rstrip('&')
        biz_content_dict = dict_items['biz_content']
        content_str = ''
        for key in sorted(biz_content_dict.keys()):
            if isinstance(biz_content_dict[key], basestring) == True:
                content_str = content_str + '"%s":"%s",' % (key, biz_content_dict[key])
            else:
                content_str = content_str + '"%s":%s,' % (key, biz_content_dict[key])
        content_str = content_str.rstrip(',')
        content_str = '{' + content_str + '}'
        query = all_str % content_str
        return query


    def make_sign(self,para_str):
        """
        生成签名
        :param message:
        :return:
        """
        import OpenSSL

        root = os.path.realpath(os.path.dirname(__file__))
        ali_private_path = os.path.join(root, "ali_private2048.txt")
        print ali_private_path

        #把私钥存到一个文件里，加载出来【尝试过用rsa模块的方法加载私钥字符串，会报格式错误。查看源码得知，需要从文件流加载】
        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(ali_private_path).read())
 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8') #这三句：解决签名方法编码报错

        sign = base64.encodestring(OpenSSL.crypto.sign(private_key, para_str, 'sha256'))
        return sign


class AliPayVerifyNotice(AliPayBase):
    """
    支付宝通知结果验证
    """
    def __init__(self, notice_params):
        self.service = 'notify_verify'
        self.notice_params = notice_params

    def verify_sign(self):

        server_sign = self.get_sign(
            params_map=self.notice_params)
        client_sign = self.notice_params.get("sign")

        return server_sign == client_sign

    def create_request_data(self):
        params = {
            "partner": AliPayConfig.partner,
            "service": self.service,
            "notify_id": self.notice_params['notify_id']
        }
        return params

    def verify_notify_id(self):
        """验证通知是否"""
        result = self.post_data()
        return result == "true"

    def validate(self):
        pass


class AliPayBatchTrans(AliPayBase):
    """
    支付宝批量付款接口
    doc: https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.g88hGW&treeId=64&articleId=103773&docType=1
    """
    def __init__(self, batch_no, batch_num, batch_fee, detail_data):
        self.service = "batch_trans_notify"
        self.batch_no = batch_no
        self.batch_num = batch_num
        self.batch_free = batch_fee
        self.detail_data = detail_data

    def create_request_data(self):
        param_map = {
            'partner': AliPayConfig.PARTNER,
            'service': self.service,
            'sign_type': AliPayConfig.SIGN_TYPE,
            'seller_id': AliPayConfig.SELLER_ID,
            '_input_charset': AliPayConfig.INPUT_CHARSTE,
            'account_name': AliPayConfig.SELLER_ID,
            'Email': AliPayConfig.SELLER_ID,
            'detail_data': self.detail_data,
            'batch_no': self.batch_no,
            'batch_num': self.batch_num,
            'batch_fee': self.batch_free,
            'pay_date': str(int_days()),
        }
        sign = self.get_sign(params_map=param_map)
        param_map['sign'] = sign
        sort_param = sorted(
            [(key, urllib2.quote(unicode(value).encode('utf-8'))) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        return sort_param

    def batch_trans(self):
        data = self.post_data()
        return data

