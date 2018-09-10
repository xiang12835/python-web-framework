# coding=utf-8
import functools
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        (0, "管理员"),
        (1, "普通用户"),
        (2, "运营"),
    )

    NORMAL = 1
    EDITOR = 2
    SUPERUSER = 0

    role = models.IntegerField(verbose_name=u'用户角色', choices=ROLE_CHOICES, default=1)

    class Meta:
        app_label = 'user'

    @property
    def role_name(self):
        role_dic = dict(self.ROLE_CHOICES)
        return role_dic.get(self.role, "无")

    @property
    def is_manager(self):
        return self.is_super or self.is_super_editor

    @property
    def is_super(self):
        return self.role == self.SUPERUSER

    @property
    def is_super_editor(self):
        return self.role == self.EDITOR

    @property
    def is_normal_user(self):
        return self.role == self.NORMAL


class UserBoxPerm(models.Model):
    SOURCE_CHOICE = (
        (0, u"首页平台"),
        (1, u"轮播图"),
        (2, u"广告"),
        (3, u"app 详情"),
        (4, u"app 类型"),
        (5, u"排版"),
        (6, u"统计"),
    )
    src_cls_dict = {
        # 0: Banner,
        # 1: Banner,
        # 3: AppDetail,
        # 4: AppCategory,
    }
    user = models.ForeignKey(User)
    drawer_id = models.IntegerField(blank=False)  #暂时先不区分，统一默认为0
    source = models.IntegerField(choices=SOURCE_CHOICE, default=0)

    class Meta:
        app_label = 'user'

    @classmethod
    def has_perm(cls, box_id, user, src=0):
        if user.is_normal_user:
            return cls.objects.filter(drawer_id=box_id, user=user, source=src).count() > 0
        return True

    # @classmethod
    # def get_src_cls(cls, src=0):
    #     if isinstance(src, (str, unicode)):
    #         src = cls.get_src_id(src)
    #     try:
    #         return cls.src_cls_dict[src]
    #     except KeyError:
    #         return cls.src_cls_dict[0]
    #
    # @classmethod
    # def get_src_name_from_platform(cls, platform='iphone'):
    #     contrast = {
    #         'iphone': 2,
    #         'ipad': 3,
    #         'android': 4
    #     }
    #     try:
    #         return contrast[platform]
    #     except KeyError:
    #         return -1
