#coding=utf-8
from h5.views.base import BaseHandler , CachedPlusHandler
from h5.document.doc_tools import *
from django.conf import settings
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
import tornado
from xml.etree.ElementTree import XML
import logging

@handler_define
class WeixinGetScanPayQrcodeHandler(BaseHandler):
    """
    微信扫码支付模式一获取支付二维码
    主要作为线下支付用途
    """


    def gen_image_path(self ,product_id):

        native_handler = WeXinNativeLink(settings.BSK_WXPAY_SETTING)
        native_handler.setParameter("product_id", product_id)

        url = native_handler.getUrl()
        logging.info(url)
        res = mk_qr(url, filename_pre_fix='order_')
        cdn_url = res.get('url', '')

        return cdn_url


    @api_define("WeixinScanPayHandler", r'/api/wx/qrcode',
                [ 
                    Param('product_id', True, str, "", "201711081448037254818846", u'订单id'),
                ],
                description="微信二维码支付")
    def get(self):
        product_id = self.arg('product_id')

        curl = self.gen_image_path(product_id)
        return self.write({"curl":curl})



@handler_define
class WeixinGetScanPayQrcodeGZHHandler(BaseHandler):
    """
    微信扫码支付模式一公众号
    主要作为线下支付用途
    """

    def gen_image_path(self ,url):

        res = mk_qr(url, filename_pre_fix='gzh_order_', add_icon=True)
        cdn_url = res.get('url', '')

        return cdn_url


    @api_define("WeixinGetScanPayQrcodeGZHHandler", r'/api/wx/gzh/qrcode',
                [ 
                    Param('product_id', True, str, "", "201711081448037254818846", u'订单id'),
                ],
                description="微信二维码公众号")
    def get(self):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect" % ("wx6457a8b0deb2c4e9","https://h5.platform.winlesson.com/api/gzh/wx_pay/page")
        curl = self.gen_image_path(url)
        return self.write({"curl":curl,"url":url})


@handler_define
class TianJinWeixinGetScanPayQrcodeGZHHandler(BaseHandler):
    """
    微信扫码支付模式一公众号
    主要作为线下支付用途
    """

    def gen_image_path(self ,url):

        res = mk_qr(url, filename_pre_fix='gzh_order_', add_icon=True)
        cdn_url = res.get('url', '')

        return cdn_url


    @api_define("TianJinWeixinGetScanPayQrcodeGZHHandler", r'/api/wx/gzh/tianjin/qrcode',
                [ 
                    Param('product_id', True, str, "", "201711081448037254818846", u'订单id'),
                ],
                description="微信二维码公众号")
    def get(self):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect" % ("wxb136a982abd01e9f","https://h5.platform.winlesson.com/api/gzh/wx_pay/tianjin/page")
        curl = self.gen_image_path(url)
        return self.write({"curl":curl,"url":url})





@handler_define
class WeixinGetScanPayZhifuHandler(BaseHandler):
    """
    1.支付地址跳转,公众号支付
    """

    @api_define("WeixinGetScanPayZhifuHandler", r'/api/gzh/pay',
                [ 
                    Param('product_id', True, str, "", "201711081448037254818846", u'订单id'),
                ],
                description="微信二维码支付")
    def get(self):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect" % ("wx6457a8b0deb2c4e9","https://h5.platform.winlesson.com/api/gzh/wx_pay/tianjin/page")
        return self.write({"curl":url})


@handler_define
class TianJinWeixinGetScanPayZhifuHandler(BaseHandler):
    """
    1.支付地址跳转,公众号支付
    """

    @api_define("WeixinGetScanPayZhifuHandler", r'/api/gzh/tianjin/pay',
                [ 
                    Param('product_id', True, str, "", "201711081448037254818846", u'订单id'),
                ],
                description="微信二维码支付")
    def get(self):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect" % ("wxb136a982abd01e9f","https://h5.platform.winlesson.com/api/gzh/wx_pay/page")
        return self.write({"curl":url})





@handler_define
class WeixinGetScanPayZhifuPageHandler(tornado.web.RequestHandler):
    """
    2.公众号支付，支付输入金额地址
    """
    @api_define("WeixinGetScanPayZhifuPageHandler", r'/api/gzh/wx_pay/page',
                [ 
                    Param('code', True, str, "", "", u'code'),
                ],
                description="微信二维码支付")
    def get(self,x):
        code = self.get_argument('code','')
        app_id = "5"
        openid = ""
        access_data = WexinAPI.get_access_token(code,app_id)
        #print access_data
        access_token = access_data.get("access_token")
        openid = access_data.get("openid")


        return self.render("h5pay/gzh_pay.html", **{"openid": openid,"code":code,"access_token":access_token})



@handler_define
class WeixinGetScanPayZhifuPageHandler(tornado.web.RequestHandler):
    """
    2.公众号支付，支付输入金额地址
    """
    @api_define("WeixinGetScanPayZhifuPageHandler", r'/api/gzh/wx_pay/tianjin/page',
                [ 
                    Param('code', True, str, "", "", u'code'),
                ],
                description="微信二维码支付")
    def get(self,x):
        code = self.get_argument('code','')
        app_id = "9"
        openid = ""
        access_data = WexinAPI.get_access_token(code,app_id)
        print access_data
        logging.error(access_data)
        access_token = access_data.get("access_token")
        openid = access_data.get("openid")


        return self.render("tjH5pay/index.html", **{"openid": openid,"code":code,"access_token":access_token})





@handler_define
class WeixinGetScanPayZhifuCommitHandler(BaseHandler):
    """
    3.公众号支付，生成支付订单
    """
    @api_define("WeixinGetScanPayZhifuCommitHandler", r'/api/gzh/wx_pay/commit/page/',
                [ 
                    Param('openid', True, str, "", "", u'openid'),
                    Param('access_token', True, str, "", "", u'access_token'),
                    Param('amount', True, str, "", "", u'amount'),
                    Param('is_tianjin', True, str, "", "", u'is_tianjin公众号1|0'),
                ],
                description="微信二维码支付")
    def get(self):
        openid = self.arg('openid')
        access_token = self.arg('access_token')
        amount = float(self.arg('amount',0))
        if self.arg('is_tianjin',"0") == "1":
            is_tianjin = True
        else:
            is_tianjin = False
            

        good_name = "winlesson_pay"

        logging.error("openid=%s"%openid)
        logging.error("access_token=%s"%access_token)
        logging.error("is_tianjin=%s" % is_tianjin)

        userinfo = WexinAPI.get_user_info(access_token,openid)
        logging.error(userinfo)

        
        order_id = get_primary_key()
        #1.创建系统订单
        OrderInfo.create_order_for_gongzhuhao(order_id,amount)
        #2.创建公众号支付订单
        out_trade_no = order_id
        wgr = WxGzhResult()
        wgr.out_trade_no = out_trade_no
        wgr.access_token = access_token
        wgr.openid = openid
        wgr.unionid = userinfo.get('unionid','')
        wgr.nickname = userinfo.get("nickname",'')
        wgr.sex = userinfo.get('sex','1')
        wgr.save()


        pay = GZHPayDoPay(
            out_trade_no=out_trade_no,
            subject=good_name,
            total_fee= int(amount * 100),
            body=good_name,
            ip = self.user_ip,
            openid = openid,
            is_tianjin = is_tianjin,
        )
        params = pay.do_pay_params_dict()
        return self.write({"params":params,"ip":self.user_ip})

        
@handler_define
class WeixinGetScanPayZhifuNotifyHandler(BaseHandler):
    """
    4.公众号支付，生成支付订单，支付回调通知
    """
    
    @api_define("WeChat WeixinGetScanPayZhifuNotifyHandler Url", r'/api/gzh/wx_pay/notify', [
    ], description=u"微信支付成功通知接口",)
    def post(self):
        body = self.request.body

        if not body:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                    ''')

        logging.error(body)
        xml = XML(body)


        wp = GZHPayDoPay( out_trade_no='',
                subject='',
                total_fee='',
                body='',
                ip = self.user_ip)

        success = wp.verify_notice_sign(xml)
        logging.error("sign: %s" % success)

        if not success:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[Sign error]]></return_msg>
                    </xml>
                    ''')

        json_data = self.create_order(xml)
        if not json_data:
            json_data = {}

        logging.error(json_data)
        out_trade_no = json_data.get('out_trade_no','')
        amount = float(json_data.get('cash_fee',0))
        mch_id = json_data.get('mch_id','') 
        #1.更新订单状态
        OrderInfo.apply_gongzhuhao(out_trade_no, amount, mch_id)

        #2.更新公众号订单
        wgr = WxGzhResult.objects.filter(out_trade_no=out_trade_no).first()
        if not wgr:
            wgr = WxGzhResult()

        
        wgr.appid = json_data.get('appid','')
        wgr.bank_type = json_data.get('bank_type','')
        wgr.cash_fee = json_data.get('cash_fee','')
        wgr.is_subscribe = json_data.get('is_subscribe','')
        wgr.mch_id = json_data.get('mch_id','')
        wgr.nonce_str = json_data.get('nonce_str','')
        wgr.openid = json_data.get('openid','')
        wgr.out_trade_no = json_data.get('out_trade_no','')
        wgr.result_code = json_data.get('result_code','')
        wgr.sign = json_data.get('sign','')
        wgr.total_fee = json_data.get('total_fee','')
        wgr.trade_type = json_data.get('trade_type','')
        wgr.transaction_id  = json_data.get('transaction_id','')
        wgr.save()


        self.write('''
                <xml>
                  <return_code><![CDATA[SUCCESS]]></return_code>
                  <return_msg><![CDATA[OK]]></return_msg>
                </xml>
                ''')
        

    @classmethod
    def create_order(cls,xml):
        root = xml
        logging.error(xml)
        wcn = {}
        wcn["app_id"] = root.find('appid').text
        wcn["bank_type"] = root.find('bank_type').text
        wcn["cash_fee"] = root.find('cash_fee').text
        wcn["is_subscribe"] = root.find('is_subscribe').text
        wcn["mch_id"] = root.find('mch_id').text
        wcn["nonce_str"] = root.find('nonce_str').text
        wcn["openid"] = root.find('openid').text
        wcn["out_trade_no"] = root.find('out_trade_no').text
        wcn["result_code"] = root.find('result_code').text
        wcn["sign"] = root.find('sign').text
        wcn["total_fee"] = root.find('total_fee').text
        wcn["trade_type"] = root.find('trade_type').text
        wcn["transaction_id"] = root.find('transaction_id').text

        return wcn


        



@handler_define
class WeixinGetScanPayZhifuNotifyHandler(BaseHandler):
    """
    4.公众号支付，生成支付订单，支付回调通知
    """
    
    @api_define("WeChat WeixinGetScanPayZhifuNotifyHandler Url", r'/api/gzh/wx_pay/tianjin/notify', [
    ], description=u"微信支付成功通知接口",)
    def post(self):
        body = self.request.body

        if not body:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                    ''')

        logging.error(body)
        xml = XML(body)


        wp = GZHPayDoPay( out_trade_no='',
                subject='',
                total_fee='',
                body='',
                ip = self.user_ip,
                is_tianjin=True,
                )

        success = wp.verify_notice_sign(xml)
        logging.error("sign: %s" % success)

        if not success:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[Sign error]]></return_msg>
                    </xml>
                    ''')

        json_data = self.create_order(xml)
        if not json_data:
            json_data = {}

        logging.error(json_data)
        out_trade_no = json_data.get('out_trade_no','')
        amount = float(json_data.get('cash_fee',0))
        mch_id = json_data.get('mch_id','') 

        #1.更新订单状态
        OrderInfo.apply_gongzhuhao(out_trade_no, amount, mch_id)

        #2.更新公众号订单
        wgr = WxGzhResult.objects.filter(out_trade_no=out_trade_no).first()
        if not wgr:
            wgr = WxGzhResult()

        
        wgr.appid = json_data.get('appid','')
        wgr.bank_type = json_data.get('bank_type','')
        wgr.cash_fee = json_data.get('cash_fee','')
        wgr.is_subscribe = json_data.get('is_subscribe','')
        wgr.mch_id = json_data.get('mch_id','')
        wgr.nonce_str = json_data.get('nonce_str','')
        wgr.openid = json_data.get('openid','')
        wgr.out_trade_no = json_data.get('out_trade_no','')
        wgr.result_code = json_data.get('result_code','')
        wgr.sign = json_data.get('sign','')
        wgr.total_fee = json_data.get('total_fee','')
        wgr.trade_type = json_data.get('trade_type','')
        wgr.transaction_id  = json_data.get('transaction_id','')
        wgr.save()


        self.write('''
                <xml>
                  <return_code><![CDATA[SUCCESS]]></return_code>
                  <return_msg><![CDATA[OK]]></return_msg>
                </xml>
                ''')
        

    @classmethod
    def create_order(cls,xml):
        root = xml
        logging.error(xml)
        wcn = {}
        wcn["app_id"] = root.find('appid').text
        wcn["bank_type"] = root.find('bank_type').text
        wcn["cash_fee"] = root.find('cash_fee').text
        wcn["is_subscribe"] = root.find('is_subscribe').text
        wcn["mch_id"] = root.find('mch_id').text
        wcn["nonce_str"] = root.find('nonce_str').text
        wcn["openid"] = root.find('openid').text
        wcn["out_trade_no"] = root.find('out_trade_no').text
        wcn["result_code"] = root.find('result_code').text
        wcn["sign"] = root.find('sign').text
        wcn["total_fee"] = root.find('total_fee').text
        wcn["trade_type"] = root.find('trade_type').text
        wcn["transaction_id"] = root.find('transaction_id').text

        return wcn





@handler_define
class BCYinLianSuccessHtml(tornado.web.RequestHandler):

    @api_define("BCYinLianSuccessHtml", r'/bc/yinlian/success',
                [
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
                description="银联支付成功")
    def get(self,x):
        
         return self.render("pay_yinlian_success.html")





