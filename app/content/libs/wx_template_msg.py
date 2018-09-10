# coding=utf-8
import json
import requests
import logging

class WeixinTemplateMessage(object):
    """ 微信模版消息
    doc: https://mp.weixin.qq.com/debug/wxadoc/dev/api/notice.html
    id: wxf7ddea990f9c685f
    secrect: 27138800f4f6609e62b489333ca4167a

    """

    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self.token_url = "https://api.weixin.qq.com/cgi-bin/token"
        self.send_url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send"
        self.template_url = "https://api.weixin.qq.com/cgi-bin/wxopen/template/list"
        self.template_library_url = "https://api.weixin.qq.com/cgi-bin/wxopen/template/library/list"
        self.keyword_url = "https://api.weixin.qq.com/cgi-bin/wxopen/template/library/get"
        self.add_url = "https://api.weixin.qq.com/cgi-bin/wxopen/template/add"
        self.del_url = "https://api.weixin.qq.com/cgi-bin/wxopen/template/del"

    def send_get_request(self, url):
        r = requests.get(url, verify=False)

        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        # 禁用安全请求警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        return r.json()

    def send_post_request(self, url, payload):
        r = requests.post(url, data=json.dumps(payload), verify=False)
        return r.json()



    def get_access_token(self):
        """获取 access_token

        token_url:
        https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

        :return:
        """

        url = self.token_url + "?grant_type=client_credential" + "&appid=" + self.appid+"&secret="+self.secret
        json_data = self.send_get_request(url)
        return json_data.get("access_token", "")

    def post_template_library_list(self, offset=0, count=20):
        """1.获取小程序模板库标题列表

        https://api.weixin.qq.com/cgi-bin/wxopen/template/library/list?access_token=ACCESS_TOKEN

        :param:

        POST参数说明：

        参数	必填	说明
        access_token	是	接口调用凭证
        offset	是	offset和count用于分页，表示从offset开始，拉取count条记录，offset从0开始，count最大为20。
        count	是	offset和count用于分页，表示从offset开始，拉取count条记录，offset从0开始，count最大为20。

        :return:
        """
        access_token = self.get_access_token()
        url = self.template_library_url + "?access_token=" + access_token

        payload = {'access_token': access_token, 'offset': offset, 'count': count}
        json_data = self.send_post_request(url, payload)
        return json_data

    def post_keyword_list_in_this_template(self, template_title_id):
        """2.获取模板库某个模板标题下关键词库

        https://api.weixin.qq.com/cgi-bin/wxopen/template/library/get?access_token=ACCESS_TOKEN
        :param:

        POST参数说明：

        参数	必填	说明
        access_token	是	接口调用凭证
        id	是	模板标题id，可通过接口获取，也可登录小程序后台查看获取
        :return:
        """
        access_token = self.get_access_token()
        url = self.keyword_url + "?access_token=" + access_token

        payload = {'access_token': access_token, 'id': template_title_id}
        json_data = self.send_post_request(url, payload)
        return json_data

    def add_template(self, template_title_id, keyword_id_list):
        """3.组合模板并添加至帐号下的个人模板库

        https://api.weixin.qq.com/cgi-bin/wxopen/template/add?access_token=ACCESS_TOKEN

        :param:

        POST参数说明：

        access_token	是	接口调用凭证
        id	是	模板标题id，可通过接口获取，也可登录小程序后台查看获取
        keyword_id_list	是	开发者自行组合好的模板关键词列表，关键词顺序可以自由搭配（例如[3,5,4]或[4,5,3]），最多支持10个关键词组合
        :return:
        """
        access_token = self.get_access_token()
        url = self.add_url + "?access_token=" + access_token

        payload = {'access_token': access_token, 'id': template_title_id, 'keyword_id_list': keyword_id_list}
        json_data = self.send_post_request(url, payload)
        return json_data

    def post_my_template_list(self, offset=0, count=20):
        """4.获取帐号下已存在的模板列表

        https://api.weixin.qq.com/cgi-bin/wxopen/template/list?access_token=ACCESS_TOKEN

        :param:

        POST参数说明：
        参数	            必填  	说明
        access_token	是	    接口调用凭证
        offset	        是	    offset和count用于分页，表示从offset开始，拉取count条记录，offset从0开始，count最大为20。最后一页的list长度可能小于请求的count
        count	        是	    offset和count用于分页，表示从offset开始，拉取count条记录，offset从0开始，count最大为20。最后一页的list长度可能小于请求的count

        :return:
        """
        access_token = self.get_access_token()
        url = self.template_url + "?access_token=" + access_token

        payload = {'access_token': access_token, 'offset': offset, 'count': count}
        json_data = self.send_post_request(url, payload)
        return json_data

    def del_template(self, template_id):
        """5.删除帐号下的某个模板

        https://api.weixin.qq.com/cgi-bin/wxopen/template/del?access_token=ACCESS_TOKEN

        :param:

        POST参数说明：

        access_token	是	接口调用凭证
        template_id	是	要删除的模板id

        :return:
        """
        access_token = self.get_access_token()
        url = self.del_url + "?access_token=" + access_token

        payload = {'access_token': access_token, 'template_id': template_id}
        json_data = self.send_post_request(url, payload)
        return json_data

    def send_template_msg(self, touser, template_id, data, form_id, page='', color='', emphasis_keyword=''):
        """发送模板消息
        send_url:
        https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=ACCESS_TOKEN

        :param data:

        POST参数说明：

        参数	    必填	说明
        touser	是	接收者（用户）的 openid
        template_id	是	所需下发的模板消息的id
        page	否	点击模板卡片后的跳转页面，仅限本小程序内的页面。支持带参数,（示例index?foo=bar）。该字段不填则模板无跳转。
        form_id	是	表单提交场景下，为 submit 事件带上的 formId；支付场景下，为本次支付的 prepay_id
        data	是	模板内容，不填则下发空模板
        color	否	模板内容字体的颜色，不填默认黑色
        emphasis_keyword	否	模板需要放大的关键词，不填则默认无放大

        示例：
        {
          "touser": "OPENID",
          "template_id": "TEMPLATE_ID",
          "page": "index",
          "form_id": "FORMID",
          "data": {
              "keyword1": {
                  "value": "339208499",
                  "color": "#173177"
              },
              "keyword2": {
                  "value": "2015年01月05日 12:30",
                  "color": "#173177"
              },
              "keyword3": {
                  "value": "粤海喜来登酒店",
                  "color": "#173177"
              } ,
              "keyword4": {
                  "value": "广州市天河区天河路208号",
                  "color": "#173177"
              }
          },
          "emphasis_keyword": "keyword1.DATA"
        }

        :return:
        正常时的返回JSON数据包示例：
        {
          "errcode": 0,
          "errmsg": "ok"
        }
        错误时会返回错误码信息，说明如下：
        返回码	说明
        40037	template_id不正确
        41028	form_id不正确，或者过期
        41029	form_id已被使用
        41030	page不正确
        45009	接口调用超过限额（目前默认每个帐号日调用限额为100万）
        """

        access_token = self.get_access_token()
        url = self.send_url + "?access_token=" + access_token
        # print url
        logging.info(url)
        payload = {
            "touser": touser,
            "template_id": template_id,
            "page": page,
            "form_id": form_id,
            "data": data
        }
        # print payload
        json_data = self.send_post_request(url, payload)
        return json_data


if __name__ == "__main__":
    appid = "wxf7ddea990f9c685f"
    secret = "27138800f4f6609e62b489333ca4167a"

    m = WeixinTemplateMessage(appid, secret)
    # print m.get_access_token()

    # template_library_list = m.post_template_library_list()
    # print json.dumps(template_library_list, ensure_ascii=False, sort_keys=True, indent=4)

    # keyword_list = m.post_keyword_list_in_this_template("AT0020")
    # print json.dumps(keyword_list, ensure_ascii=False, sort_keys=True, indent=4)

    # new_template = m.add_template("AT0020", [1,2,3])
    # print json.dumps(new_template, ensure_ascii=False, sort_keys=True, indent=4)

    # my_template_list = m.post_my_template_list()
    # print json.dumps(my_template_list, ensure_ascii=False, sort_keys=True, indent=4)

    # del_r = m.del_template("sr3SSjbj9vGK_TL0rzFSxHjvhtWyqe7yn1gV6zEE4AY")
    # print json.dumps(del_r, ensure_ascii=False, sort_keys=True, indent=4)

    touser = 'oakPr0DNNSILHSGF4gV0kXiC-_1Q'
    template_id = "9LwrK7euoAKFeS1nGbouCPHiBQfpV_NMgRt0NqPy8HI"
    page = "pages/activity/pt/pt?pt_id=22"
    # page = "pages/index/index?iurl=https%3A%2F%2Fxcx.winlesson.com%2Fvideo%2Fcourse_id%2F201807181425378520576832"
    form_id = 'wx11151509412030c97a2fb37e1255311777'
    data = {
        "keyword1": {
            "value": "我是课程",
            # "color": "#173177"
        },
        "keyword2": {
            "value": "我是拼员",
            # "color": "#173177"
        },
        "keyword3": {
            "value": "用参与拼团的手机号登陆必胜公考APP，进入“我的课程”，可缓存视频至手机，随时随地观看>>",
            # "color": "#173177"
        }
    }
    r = m.send_template_msg(touser, template_id, data, form_id, page=page, color='', emphasis_keyword='')
    print r




