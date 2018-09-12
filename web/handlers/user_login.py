#coding=utf-8

from web.views.base import BaseHandler , CachedPlusHandler
from web.document.doc_tools import *
import hashlib
from django.conf import settings
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
import tornado.web


@handler_define
class SignInHandler(BaseHandler):

    @api_define("SignIn", r'/user/signin', [
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),
    ], description="登录")
    def get(self):
        return self.render("Sign/new_sign_in.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        password = hashlib.md5(password).hexdigest()
        userinfo = BskUser.get_user_by_name(username)

        if password.lower() == userinfo.password.lower():

            if userinfo and userinfo.user_id:
                self.auth_login(userinfo.user_id)

            self.redirect("/")
        else:
            self.render("Sign/new_sign_in.html")


@handler_define
class SignUpHandler(BaseHandler):

    @api_define("SignUp", r'/user/signup', [
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),
    ], description="注册")
    def get(self):
        return self.render("Sign/new_sign_up.html", **{})


@handler_define
class SignOutHandler(BaseHandler):
    @api_define("SignOut", r'/user/signout', [
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69",
              u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid'),
    ], description="登出")
    def get(self):
        self.auth_logout()
        self.redirect("/")



