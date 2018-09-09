#coding=utf-8

from tornado_py2.document.doc_tools import *
from tornado_py2.util.public import hit_config
from tornado_py2.view.base import BaseHandler
# from app.index.lib.util import DateUtil
# from app.index.models import Platform, Device, Switch
from django.conf import settings
import time, datetime
# from app.index.models import HomePopup
# from app.bskcommon.models import BskUser , UserVoucher
# from app.bskgk.models import CourseUserInfo , OrderInfo, AppVersion, FeedBack, AppVersionChannel
#
# from app.api_util.qcloud.auth_bucket import get_bucket_sign


@handler_define
class Initial(BaseHandler):

    def prepare(self):
        self.platform = self.get_argument('platform', '')
        self.device = self.get_argument('device', '')

        try:
            app_type = int(self.platform)
            self.platform = self.arg("from",'android')
        except Exception,e:
            pass
            
        if self.platform == 'android' and self.device == 'pad':
            self.device = 'phone'


        self.pid = self.get_argument('pid', '')
        self.operator = self.get_argument('operator', '')
        self.ver = self.get_argument('ver', '')
        self.device_ver = self.get_argument('device_ver', '')
        self.area = self.get_argument('area', '')[0:2]

        self.params = {
            'pid': self.pid,
            'operator': self.operator,
            'ver': self.ver,
            'device_ver': self.device_ver,
            'area': self.area,
        }
        self.today = DateUtil.get_today_int_date()

    @api_define("Initial", r'/initial',
                [Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69",
                       u'用户guid'),
                 Param('user_id', True, str, "201609172200021311004891", "201609172200021311004891", u'user_id'),
                 Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),
                 Param('app_type', True, str, '2', '2', u'应用(2:必胜公考/1:必胜课)'),
                 Param('platform', True, str, 'android', 'android', u'平台(android/ios) or 2'),
                 Param('from', True, str, 'android', 'android', u'平台(android/ios)'),
                 Param('device', True, str, 'phone', 'phone', u'终端类型(phone/pad)'),
                 Param('operator', True, int, '1', '1', u'1:移动,2:电信,3:联通:'),
                 Param('ver', True, str, '5.0', '5.0', u'版本'),
                 Param('device_ver', True, str, 'iphone9.0', 'iphone9.0', u'设备型号版本'),
                 Param('area', True, str, '010', '010', u'地域code'),],
                description="初始化接口")
    def get(self):
        app_id = self.get_argument('app_id', '')
        result = {}
        result['status'] = "success"
        server_time = int(time.time())
        result['server_time'] = server_time

        platform_id, device_id = Platform.get_platform_hash(self.platform), Device.get_device_hash(self.device)
        if not platform_id or not device_id:
            return self.send_error(400, desc='invalid platform,or device')

        is_update_cache = self.request.headers.get('Is-Update-Cache', '')
        rets = self.get_common_switch_data(platform_id=platform_id,
                                           app_type = self.arg_int('app_type' , 2),
                                           device_id=device_id,
                                           is_update_cache=is_update_cache,
                                           **self.params)

        #rets = self.get_addition_words(rets)
        result.update({'switches': rets.get("results",{})})
        result["code"] = 200
        result["msg"] = ""

        return self.write(result)

    def get_common_switch_data(self, platform_id, app_type ,device_id, is_update_cache='NO', **params):
        rets = {}
        try:
            switches = self.get_switch_info(platform_id , app_type, device_id, is_update_cache=is_update_cache)
            
            results = {}
            for swi in switches:
                if swi['is_valid']:
                    temp = {}
                    config_str = swi['configs']


                    if config_str:
                        state = hit_config(switch_id=swi['id'], config_str=config_str, model_ob=1, **params)
                        temp.update({swi['name']: state})
                    else:
                        temp.update({swi['name']: swi['state']})

                    results.update(temp)
            rets.update({'results': results})
        except Exception, e:
            logging.error(e)

        return rets

    def get_switch_info(self, platform_id, app_type, device_id, is_update_cache=''):
        switches = Switch.objects.filter(platform_id=platform_id, device_id=device_id , app_type=app_type).values()
        ss = []
        for swi in switches:
            ss.append(swi)
        return ss




@handler_define
class HomePopupAPI(BaseHandler):

    @api_define("首页弹窗接口", r'/home/popup',
                [
                Param('user_id', True, str, "201609172200021311004891", "201609172200021311004891", u'user_id'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69",
                       u'用户guid'),
                Param('ver', True, str, "2.6.0", "2.6.0", u'ver'),
                Param('from', True, str, "", "android", u'from'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),],
                description="首页弹窗接口",
                return_desc="""
                pop_way =  1:"h5",2:"课程",
                """)
    def get(self):
        from app.statstic.models import UserData
        from wi_cache import push_cache

        user_id = self.arg('user_id')
        ver = self.arg("ver")
        _from =self.arg('from' , "other")

        pops = HomePopup.get_valid_popup()
        
        is_send = False
        pop = None

    
        if pops:

            for _pop in pops:
                pop = _pop
                if pop.pop_type == HomePopup.TYPE_VIP:
                    #print "here TYPE_VIP"
                    is_send = BskUser.is_vip(user_id)
                    
                elif pop.pop_type == HomePopup.TYPE_NOT_VIP:
                    #print "here TYPE_NOT_VIP"
                    ccount = CourseUserInfo.get_sys_course_count(user_id)
                    if ccount==0:
                        is_send = True
                    else:
                        is_send = False

                elif pop.pop_type == HomePopup.TYPE_NOT_VIP_AND_NOT_NEW_USER:
                    is_send = not BskUser.is_vip(user_id)
                    if is_send:
                        if BskUser.is_first_week_register_user(user_id):
                            is_send = False
                        else:
                            is_send = True

                elif pop.pop_type == HomePopup.TYPE_Register:
                    is_send = BskUser.is_dubble_week_register_user(user_id)

                elif pop.pop_type == HomePopup.TYPE_THIS_DAY_NEW_USER:
                    is_send = BskUser.is_today_register_user(user_id)
                elif pop.pop_type == HomePopup.TYPE_ANDROID:
                    if _from == "android":
                        is_send = True
                    else:
                        is_send = False
                elif pop.pop_type == HomePopup.TYPE_IOS:
                    
                    if _from == "ios":
                        is_send = True
                    else:
                        is_send = False

                else:
                    #投放全部
                    is_send = True

                if pop.area == "":
                    pass

                # 判断地区
                if is_send and pop.area:
                    user = UserData.objects.filter(user_id=user_id).first()
                    if user and user.province in pop.area.split(","):
                        is_send = True
                    else:
                        is_send = False

                if is_send:
                    key = "home:%s:push:%s" % (user_id, pop.id)
                    has_pop = push_cache.get(key)
                    if has_pop:
                        is_send = False
                        continue
                    else:
                        #set poped
                        push_cache.set(key,user_id,60*60*24*2)
                        break


        result = {}
        result["code"] = 200
        result["msg"] = ""

        if pop and is_send:

            if pop.pop_way == 2:
                if ver>="2.6.0":
                    is_send = True
                else:
                    is_send = False
            elif pop.pop_way == 3:
                if ver>="3.5.0":
                    is_send = True
                else:
                    is_send = False

                if ver<="1.1.0":
                    is_send = True


        if is_send:
            result["popup"] = pop.to_json()
            result["popup"]["title"] = "活动"
            result["status"] = "success"

        return self.write(result)


@handler_define
class XCXPopupAPI(BaseHandler):

    @api_define("XCXPopupAPI", r'/home/popup/xcx', [
        Param('user_id', False, str, "201609172200021311004891", "201609172200021311004891", u'user_id'),
        Param('from', True, str, "", "android", u'from'),
    ], description="小程序弹窗接口", return_desc="""
    pop_way =  1:"h5",2:"课程",
    """)
    def get(self):

        from wi_cache import push_cache

        user_id = self.arg('user_id')
        _from = self.arg('from', "other")

        pops = HomePopup.get_valid_xcx_popup()

        is_send = False
        pop = None
        result = {}
        result["code"] = 200
        result["msg"] = ""

        for _pop in pops:
            pop = _pop
            if pop.pop_type == HomePopup.TYPE_VIP:
                # print "here TYPE_VIP"
                is_send = BskUser.is_vip(user_id)

            elif pop.pop_type == HomePopup.TYPE_NOT_VIP:
                # print "here TYPE_NOT_VIP"
                ccount = CourseUserInfo.get_sys_course_count(user_id)
                if ccount == 0:
                    is_send = True
                else:
                    is_send = False

            elif pop.pop_type == HomePopup.TYPE_NOT_VIP_AND_NOT_NEW_USER:
                is_send = not BskUser.is_vip(user_id)
                if is_send:
                    if BskUser.is_first_week_register_user(user_id):
                        is_send = False
                    else:
                        is_send = True

            elif pop.pop_type == HomePopup.TYPE_Register:
                is_send = BskUser.is_dubble_week_register_user(user_id)

            elif pop.pop_type == HomePopup.TYPE_THIS_DAY_NEW_USER:
                is_send = BskUser.is_today_register_user(user_id)
            elif pop.pop_type == HomePopup.TYPE_ANDROID:
                if _from == "android":
                    is_send = True
                else:
                    is_send = False
            elif pop.pop_type == HomePopup.TYPE_IOS:

                if _from == "ios":
                    is_send = True
                else:
                    is_send = False

            else:
                # 投放全部
                is_send = True

            if is_send:
                key = "home:%s:push:%s" % (user_id, pop.id)
                has_pop = push_cache.get(key)
                if has_pop:
                    continue
                else:
                    # set poped
                    push_cache.set(key, user_id, 60 * 60 * 24 * 1)
                    break

        if is_send:
            result["popup"] = pop.to_json()
            result["popup"]["title"] = "活动"
            result["status"] = "success"

        return self.write(result)


@handler_define
class GetBucketSignHandler(BaseHandler):

    @api_define("GetBucketSignHandler", r'/api/bskgk/v2/bucket/sign',
                [
                Param('expired', True, str, "", "", u'expired'),
                Param('file_name', True, str, "", "", u'file_name'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69",
                       u'用户guid'),
                Param('ver', True, str, "2.6.0", "2.6.0", u'ver'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),],
                description="初始化腾讯云bucket接口",
                return_desc="""
                api.msg.platform.winlesson.com
                """)
    def post(self):
        expired = self.get_argument("expired", 30 * 24 * 60 * 60)
        _from = self.get_argument("from", "unknown")
        file_name = self.get_argument("fileName", "")

        bucket = "audio"
        bucket_sign = get_bucket_sign(bucket, expired, _type=2, fileid=file_name)

        ret = {
            "code": "200",
            "msg": "请求成功",
            "result": {
                "bucket_sign": bucket_sign,
                "appid": "10004299",
            }
        }

        return self.write(ret)

@handler_define
class GetQqGroupKeyHandler(BaseHandler):
    

    @api_define("GetQqGroupKeyHandler", r'/api/bskgk/qq_group/key',
                [
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69",
                       u'用户guid'),
                Param('ver', True, str, "2.6.0", "2.6.0", u'ver'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),],
                description="初始化QQ群",
                return_desc="""
                """)
    def post(self):
        
        group_key = {
            "id": 1,
            "groupId":"623829735",
            "androidGroupKey": "3ROCXfCI7AEGdC3nMDH95pgSzfiNTPmU",
            "iosGroupKey": "9b85c6b0ebb9a421cc1def27a5c9a27681049376d320003839de788de86a593f",
            "status": 1,
            "createTime": "2017-05-17 17:39:51"
        }

        ret = {
            "code": "200",
            "msg": "请求成功",
            "result": {
                "groupKey": group_key,
            }
        }
        
        return self.write(ret)


@handler_define
class GetNewAppVersionHandler(BaseHandler):
    @api_define("GetNewAppVersionHandler", r'/api/version/app/new', [
        Param('platform', True, str, "", "2", u'平台 - 1:必胜客,2:必胜公考'),
        Param('type', True, str, "", "0", u'类型 - 1:android,2:ios'),
        Param('channel_id', True, str, "1", "1", u'渠道ID')
    ], description="APP更新信息", return_desc="""""")
    def post(self):
        try:
            platform = self.arg_int("platform", 2)
        except Exception as e:
            logging.error(e)
            platform = 2

        type = self.arg_int("type", 0)
        channel_id = self.arg_int("channel_id", 0)
        ver = self.arg("ver", "3.3.0")

        if type == 1 and channel_id:  # android
            v_info = AppVersionChannel.get_app_version_by_channel(type, platform, ver, channel_id)
        else:
            v_info = AppVersion.get_app_version(type, platform)
            
        ret = {
            "code": "200",
            "msg": "请求成功",
            "result": {
                "versionInfo": v_info,
            }
        }

        return self.write(ret)


@handler_define
class FeedBackHandler(BaseHandler):
    @api_define("FeedBackHandler", r'/api/bskgk/feeback', [
        Param('userid', True, str, "", "110119", u'用户id'),
        Param('content', True, str, "", "xxxx", u'内容'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')
    ], description="问题反馈", return_desc="""""")
    def post(self):

        ret = {}
        user_id = self.arg("userid")
        content = self.arg("content", "")
        success = FeedBack.create_feedback(user_id, content)

        if success:
            ret["status"] = "success"
        else:
            ret["status"] = "error"
        ret["code"] = "200"
        ret["msg"] = "请求成功"

        return self.write(ret)




@handler_define
class QCloudCallBackHandler(BaseHandler):
    @api_define("QCloudCallBackHandler", r'/api/qcloud/vod/callback', [
    ], description="腾讯云点播回调反馈", return_desc="""""")
    def post(self):

        from app.bskgk.models import MegerVideoFileInfo
        from app.api_util.qcloud.sms import SmsSingleSender
        from app.api_util.qcloud.qcloud_video import QCloudVideoAPI
        import json

        #body = "{\x22version\x22:\x224.0\x22,\x22eventType\x22:\x22ConcatComplete\x22,\x22data\x22:{\x22vodTaskId\x22:\x22concat-13df6a2be3c7a084cd6737e5611db3cb\x22,\x22fileInfo\x22:[{\x22fileId\x22:\x227447398156776966404\x22,\x22fileUrl\x22:\x22http://1251323988.vod2.myqcloud.com/008afa4cvodcq1251323988/7b8c23fc7447398156776966404/playlist.f9.mp4\x22,\x22fileType\x22:\x22mp4\x22,\x22status\x22:0,\x22message\x22:\x22\x22}]}}"
        body = self.request.body

        try:
            json_data = json.loads(body)
        except Exception,e:
            logging.error(e)

        #print json_data

        ret = {}
        ret["status"] = "success"

        vodTaskId = json_data.get('data',{}).get("vodTaskId")
        eventType = json_data.get('eventType')
        #视频拼接完成
        if eventType == "ConcatComplete":
            #print vodTaskId
            mvod = MegerVideoFileInfo.objects.filter(vod_task_id=vodTaskId).first()

            

            if mvod:
                mvod.body = body#self.request.body
                

                appid = settings.BSK_SMS_SETTINGS["appid"]
                appkey = settings.BSK_SMS_SETTINGS["appkey"]
                single_sender = SmsSingleSender(appid, appkey)
                templ_id = 10504
                params = ["%s:%s"% (mvod.file_name, mvod.status)]
                p = "17600590677"
                r = single_sender.send_with_param("86", p, templ_id, params, "", "", "")

                
                for fi in  json_data.get("data",{}).get("fileInfo"):
                    file_id = fi.get("fileId")
                    if file_id:
                        api = QCloudVideoAPI()
                        data = api.convert_video_file(file_id)
                        mvod.transfer_vod_task_id = data.get('vodTaskId')
                mvod.save()

        elif eventType == "TranscodeComplete":
            mvod = MegerVideoFileInfo.objects.filter(transfer_vod_task_id=vodTaskId).first()
            if mvod:
                mvod.transfer_body = body #self.request.body
                mvod.save()

                appkey = settings.BSK_SMS_SETTINGS["appkey"]
                single_sender = SmsSingleSender(appid, appkey)
                templ_id = 10504
                params = ["%s:%s"% (mvod.file_name, mvod.transfer_status)]
                p = "17600590677"
                r = single_sender.send_with_param("86", p, templ_id, params, "", "", "")




        return self.write(ret)



