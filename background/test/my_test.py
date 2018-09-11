# coding=utf-8
from __future__ import unicode_literals

import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir, os.pardir))

from base.settings import load_django_settings

load_django_settings('one_platform.base', 'one_platform.app')


from django.db import models


class Platform(models.Model):
    """ 平台 """

    STATUS_NORMAL = 0
    STATUS_CLOSED = 1

    title = models.CharField(verbose_name='标题', max_length=32, default='')
    content = models.CharField(verbose_name='平台内容', max_length=32, default='', db_index=True)
    platform_count = models.IntegerField(verbose_name='平台统计', default=0)

    status = models.IntegerField(verbose_name='状态', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        app_label = 'oper_content'
        db_table = 'platform_info'


class PlatformChannel(models.Model):
    """ 渠道 """

    STATUS_NORMAL = 0
    STATUS_CLOSED = 1

    title = models.CharField(verbose_name='标题', max_length=32, default='')
    content = models.CharField(verbose_name='渠道码', max_length=32, default='', db_index=True)
    platform = models.ForeignKey(Platform)
    # platform = models.ForeignKey(Platform, related_name="channels")
    channel_count = models.IntegerField(verbose_name='渠道统计', default=0)

    status = models.IntegerField(verbose_name='状态', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        app_label = 'oper_content'
        db_table = 'platform_channel'


class CourseInfo(models.Model):
    from django.utils import timezone
    from datetime import timedelta
    from app.bskgk.models import Category
    from app.bskgk.models import Tag

    StageLevel = (
        (0, u'挂课阶段'),
        (1, u'运营阶段'),
        (2, u'上架阶段'),
    )

    TypeChoices = (
        (1, "课程"),
        (2, "资讯"),
        (3, "H5"),
        # (4, "页面"),
        (5, "话题"),
        (6, "模考"),
        (7, "真题"),
        (8, "专项"),
        # (9, "错题本"),
        # (10, "答题卡录入"),
        # (11, "答题卡拍照"),
        (12, "智能练习"),
        # (13, "做题记录"),
        # (14, "题目收藏"),
    )

    course_id = models.CharField(max_length=32, db_column='courseId', primary_key=True)
    course_name = models.CharField(max_length=50, db_column='courseName', default='')
    course_desc = models.TextField(db_column='courseDescript', default='')
    course_note = models.TextField(verbose_name='课程备注', default='')
    course_cover = models.CharField(max_length=100, db_column='courseCover', default='')
    course_price = models.FloatField(db_column='coursePrice', default=0)
    is_prepay = models.IntegerField(verbose_name="是否预付费",default=0)
    course_total_price = models.FloatField(verbose_name="如果是预付费，课程全款价格",db_column='courseTotalPrice', default=0)

    apple_price = models.FloatField(verbose_name='苹果价格', default=0)
    apple_id = models.CharField(verbose_name='苹果ID', max_length=255, default='')
    # stop_time = models.DateTimeField(db_column='saleStopTime', default=timezone.now() + timedelta(days=30))
    saleStopTime = models.DateTimeField(db_column='saleStopTime', default=timezone.now() + timedelta(days=365))
    status = models.CharField(max_length=3, db_column='status', default='1')
    # course_type_id = models.CharField(max_length=32, db_column='courseTypeId', default='')
    is_live = models.SmallIntegerField(db_column='isLive', default=0)
    handouts_url = models.CharField(max_length=255, db_column='handoutsUrl', default='')
    create_time = models.DateTimeField(db_column='createTime', auto_now_add=True)
    intro_pic = models.CharField(max_length=255, db_column='introPic', default='')
    intro_pic_crops = models.CharField(max_length=1000, db_column='intro_pic_crops')

    merge_sub_image = models.CharField(max_length=255, default='')
    sub_intro_pics = models.CharField(max_length=2000, default='')

    video_num = models.IntegerField(verbose_name=u'课时数量', db_column='videoNum', default=0)
    handouts_name = models.CharField(max_length=100, db_column='handoutsName', default='')
    average_score = models.FloatField(db_column='averageScore', default=9.8)
    evaluate_num = models.IntegerField(db_column='evaluateNum', default=370)
    need_address = models.IntegerField(db_column='needAddress', default=0)
    lesson_id = models.IntegerField(max_length=32, db_column='lessonid')

    # 0:问答 1:互动
    content_type = models.IntegerField(verbose_name='类型', default=0)

    stage = models.IntegerField(verbose_name='层级', default=0, choices=StageLevel)
    support_balance = models.SmallIntegerField(verbose_name='是否支持余额支持', default=1 , db_column='supportBalance')
    teacher_super_cover = models.CharField(max_length=255, db_column='teacher_super_cover', default='')
    category = models.ForeignKey(Category, blank=True,null=True,db_column="category_id",default='')
    tag = models.ForeignKey(Tag, blank=True,null=True,db_column="tag_id",default='')

    is_apple_pay = models.IntegerField(verbose_name='是否支持苹果支付' , default=0)
    is_vip_free = models.IntegerField(verbose_name='是否VIP免费', default=0)
    is_xcx_share = models.IntegerField(verbose_name='小程序分享领课', default=0)
    xcx_url = models.CharField(verbose_name='小程序URL', max_length=255, default='')
    relate_course_id = models.CharField(max_length=32, db_column='relate_course_id', verbose_name="关联付费课程id",blank=True ,null=True, default='')
    is_show_evaluate = models.SmallIntegerField(verbose_name='是否展示课程评价', default=0)
    end_time = models.DateTimeField(verbose_name=u'课程下架时间', blank=True, null=True)
    is_for_teaching = models.IntegerField(verbose_name=u"是否教务管理", default=0)

    # 拼团相关
    is_show_for_xcx = models.IntegerField(verbose_name=u"是否仅在小程序投放", default=0)
    is_for_collage = models.IntegerField(verbose_name=u'是否拼团', default=0)
    collage_limit = models.IntegerField(verbose_name=u"拼团人数限制", default=0)
    collage_hour = models.IntegerField(verbose_name=u'拼团时间（小时）', default=0)
    collage_price = models.FloatField(verbose_name=u'拼团价格', default=0)
    collage_title = models.CharField(verbose_name=u"拼团名称", max_length=32, default='')
    collage_content = models.CharField(verbose_name=u"拼团内容", max_length=128, default='')
    collage_rule = models.CharField(verbose_name=u"拼团规则", max_length=255, default='')
    collage_bg_img = models.CharField(max_length=255, verbose_name=u'拼团背景图片', default='')
    collage_share_img = models.CharField(max_length=255, verbose_name=u'拼团分享图片', default='')

    # 课程详情页添加按钮
    show_button = models.IntegerField(verbose_name=u"是否显示按钮", default=0)
    button_name = models.CharField(verbose_name=u"课程详情", max_length=32, default='')
    skip_type = models.IntegerField(verbose_name=u'跳转类型', default=1, choices=TypeChoices)
    skip_course_id = models.CharField(max_length=128, verbose_name=u'跳转课程id', default='')
    skip_article_id = models.CharField(max_length=128, verbose_name=u'跳转资讯id', default='')
    skip_h5_url = models.CharField(max_length=128, verbose_name=u'h5_url', default='')

    # 公考圈相关
    is_build_group = models.IntegerField(verbose_name=u"是否建立班级群", default=0)

    class Meta:
        app_label = 'bskgk'
        db_table = 'course_info'



class CourseUserInfo(models.Model):
    course_userid = models.CharField(max_length=32, db_column='courseUserId', primary_key=True)
    course = models.ForeignKey(CourseInfo, db_column='courseId')
    # course_id = models.CharField(max_length=32, db_column='courseId')
    user_id = models.CharField(max_length=32, db_column='userId')
    purchase_time = models.DateTimeField(db_column='purchaseTime')
    order_id = models.CharField(max_length=32, db_column='orderId')
    other_system = models.CharField(max_length=3, db_column='otherSystem')

    class Meta:
        app_label = 'bskgk'
        db_table = 'course_user_info'


if __name__ == "__main__":

    # ====================== 使用 select_related 优化 ======================

    p = Platform.objects.get(id=1)

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time` FROM `platform_channel` WHERE `platform_channel`.`platform_id` = 1;
    channels = p.platformchannel_set.all()
    print "channels --> ", channels.query.__str__()
    r = [c.content for c in channels]
    print "r -->",r

    # SELECT `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_info` INNER JOIN `platform_channel` ON ( `platform_info`.`id` = `platform_channel`.`platform_id` ) WHERE `platform_channel`.`content` LIKE BINARY '%a%';
    datas = Platform.objects.filter(platformchannel__content__contains="a")
    print "datas1 --> ", datas.query.__str__()
    r = [data.content for data in datas]
    print "r1 -->",r


    # SELECT `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_info` INNER JOIN `platform_channel` ON ( `platform_info`.`id` = `platform_channel`.`platform_id` ) WHERE `platform_channel`.`content` LIKE BINARY %a%
    datas = Platform.objects.select_related("platformchannel").filter(platformchannel__content__contains="a")
    print "datas1.1 --> ", datas.query.__str__()
    r = [data.content for data in datas]
    print "r1 -->", r

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time`, `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_channel` INNER JOIN `platform_info` ON ( `platform_channel`.`platform_id` = `platform_info`.`id` ) WHERE `platform_channel`.`content` LIKE BINARY %a%
    datas = PlatformChannel.objects.select_related("platform").filter(content__contains="a")
    print "datas1.2 --> ", datas.query.__str__()
    r = [data.content for data in datas]
    print "r1 -->", r

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time`, `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_channel` INNER JOIN `platform_info` ON ( `platform_channel`.`platform_id` = `platform_info`.`id` ) WHERE `platform_channel`.`content` LIKE BINARY '%a%';
    datas = PlatformChannel.objects.filter(content__contains="a").select_related("platform")
    print "datas2 --> ", datas.query.__str__()
    r = [c.content for c in datas]
    print "r2 -->", r

    r = [c.platform.content for c in datas]
    print "r3 -->", r


    """
    django 默认每个主表的对象都有一个是外键的属性，可以通过它来查询到所有属于主表的子表的信息。这个属性的名称默认是以子表的名称小写加上_set()来表示(上面默认以b_set访问)，默认返回的是一个querydict对象。

    related_name 可以给这个外键定义好一个别的名称
    """
    # channels = p.channels.all()
    # r = [c.content for c in channels]
    # print "r1 -->", r

    # channels = p.channels.filter(content__contains="l")
    # r = [c.content for c in channels]
    # print "r2 -->", r

    channels = PlatformChannel.objects.filter(platform=p)
    r = [c.content for c in channels]
    print "r3 -->",r

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time` FROM `platform_channel` WHERE `platform_channel`.`platform_id` = 1;
    channels = PlatformChannel.objects.filter(platform_id=p.id)
    print "r4 --> ", channels.query.__str__()
    r = [c.content for c in channels]
    print "r4 -->",r

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time` FROM `platform_channel` WHERE `platform_channel`.`platform_id` = 1;
    channels = PlatformChannel.objects.filter(platform__id=p.id)
    print "r5 --> ", channels.query.__str__()

    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time` FROM `platform_channel` INNER JOIN `platform_info` ON ( `platform_channel`.`platform_id` = `platform_info`.`id` ) WHERE `platform_info`.`content` = android;
    channels = PlatformChannel.objects.filter(platform__content="android")
    print "r6 --> ", channels.query.__str__()
    r = [c.content for c in channels]
    print "r6 -->",r


    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time`, `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_channel` INNER JOIN `platform_info` ON ( `platform_channel`.`platform_id` = `platform_info`.`id` ) WHERE `platform_info`.`content` = ios;
    channels = PlatformChannel.objects.select_related("platform").filter(platform__content="ios")
    print "r7 --> ", channels.query.__str__()



    course = CourseInfo.objects.filter().first()

    # r7 -->  SELECT `course_info`.`courseId`, `course_info`.`courseName`, `course_info`.`courseDescript`, `course_info`.`course_note`, `course_info`.`courseCover`, `course_info`.`coursePrice`, `course_info`.`is_prepay`, `course_info`.`courseTotalPrice`, `course_info`.`apple_price`, `course_info`.`apple_id`, `course_info`.`saleStopTime`, `course_info`.`status`, `course_info`.`isLive`, `course_info`.`handoutsUrl`, `course_info`.`createTime`, `course_info`.`introPic`, `course_info`.`intro_pic_crops`, `course_info`.`merge_sub_image`, `course_info`.`sub_intro_pics`, `course_info`.`videoNum`, `course_info`.`handoutsName`, `course_info`.`averageScore`, `course_info`.`evaluateNum`, `course_info`.`needAddress`, `course_info`.`lessonid`, `course_info`.`content_type`, `course_info`.`stage`, `course_info`.`supportBalance`, `course_info`.`teacher_super_cover`, `course_info`.`category_id`, `course_info`.`tag_id`, `course_info`.`is_apple_pay`, `course_info`.`is_vip_free`, `course_info`.`is_xcx_share`, `course_info`.`xcx_url`, `course_info`.`relate_course_id`, `course_info`.`is_show_evaluate`, `course_info`.`end_time`, `course_info`.`is_for_teaching`, `course_info`.`is_show_for_xcx`, `course_info`.`is_for_collage`, `course_info`.`collage_limit`, `course_info`.`collage_hour`, `course_info`.`collage_price`, `course_info`.`collage_title`, `course_info`.`collage_content`, `course_info`.`collage_rule`, `course_info`.`collage_bg_img`, `course_info`.`collage_share_img`, `course_info`.`show_button`, `course_info`.`button_name`, `course_info`.`skip_type`, `course_info`.`skip_course_id`, `course_info`.`skip_article_id`, `course_info`.`skip_h5_url`, `course_info`.`is_build_group` FROM `course_info` INNER JOIN `course_tag` ON ( `course_info`.`tag_id` = `course_tag`.`id` ) WHERE `course_tag`.`name` = 国考  ORDER BY `course_info`.`createTime` DESC;
    courses = CourseInfo.objects.filter(tag__name="国考")
    r = [c.course_name for c in courses]
    print r
    print "r7 --> ", courses.query.__str__()

    # SELECT `course_info`.`courseId`, `course_info`.`courseName`, `course_info`.`courseDescript`, `course_info`.`course_note`, `course_info`.`courseCover`, `course_info`.`coursePrice`, `course_info`.`is_prepay`, `course_info`.`courseTotalPrice`, `course_info`.`apple_price`, `course_info`.`apple_id`, `course_info`.`saleStopTime`, `course_info`.`status`, `course_info`.`isLive`, `course_info`.`handoutsUrl`, `course_info`.`createTime`, `course_info`.`introPic`, `course_info`.`intro_pic_crops`, `course_info`.`merge_sub_image`, `course_info`.`sub_intro_pics`, `course_info`.`videoNum`, `course_info`.`handoutsName`, `course_info`.`averageScore`, `course_info`.`evaluateNum`, `course_info`.`needAddress`, `course_info`.`lessonid`, `course_info`.`content_type`, `course_info`.`stage`, `course_info`.`supportBalance`, `course_info`.`teacher_super_cover`, `course_info`.`category_id`, `course_info`.`tag_id`, `course_info`.`is_apple_pay`, `course_info`.`is_vip_free`, `course_info`.`is_xcx_share`, `course_info`.`xcx_url`, `course_info`.`relate_course_id`, `course_info`.`is_show_evaluate`, `course_info`.`end_time`, `course_info`.`is_for_teaching`, `course_info`.`is_show_for_xcx`, `course_info`.`is_for_collage`, `course_info`.`collage_limit`, `course_info`.`collage_hour`, `course_info`.`collage_price`, `course_info`.`collage_title`, `course_info`.`collage_content`, `course_info`.`collage_rule`, `course_info`.`collage_bg_img`, `course_info`.`collage_share_img`, `course_info`.`show_button`, `course_info`.`button_name`, `course_info`.`skip_type`, `course_info`.`skip_course_id`, `course_info`.`skip_article_id`, `course_info`.`skip_h5_url`, `course_info`.`is_build_group`, `course_tag`.`id`, `course_tag`.`name`, `course_tag`.`position`, `course_tag`.`status`, `course_tag`.`created_at` FROM `course_info` INNER JOIN `course_tag` ON ( `course_info`.`tag_id` = `course_tag`.`id` ) WHERE `course_tag`.`name` = 国考  ORDER BY `course_info`.`createTime` DESC
    courses = CourseInfo.objects.select_related("tag").filter(tag__name="国考")
    r = [c.course_name for c in courses]
    print r
    print "r8 --> ", courses.query.__str__()

    # 不好用，因为自定义了主表的主键
    # users = data.courseuserinfo_set.all()
    # datas = CourseUserInfo.objects.filter(course__is_live=1)
    # print "r7 --> ", channels.query.__str__()



# SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time` FROM `platform_channel` WHERE `platform_channel`.`status` = 0 ;
    datas = PlatformChannel.objects.filter(status=0)

    r = []
    for data in datas:
        r.append(data.platform.content)  # 需要优化

    print r


    # 使用 select_related 优化
    # SELECT `platform_channel`.`id`, `platform_channel`.`title`, `platform_channel`.`content`, `platform_channel`.`platform_id`, `platform_channel`.`channel_count`, `platform_channel`.`status`, `platform_channel`.`create_time`, `platform_info`.`id`, `platform_info`.`title`, `platform_info`.`content`, `platform_info`.`platform_count`, `platform_info`.`status`, `platform_info`.`create_time` FROM `platform_channel` INNER JOIN `platform_info` ON ( `platform_channel`.`platform_id` = `platform_info`.`id` ) WHERE `platform_channel`.`status` = 0 ;
    datas = PlatformChannel.objects.filter(status=0).select_related("platform")

    r = []
    for data in datas:
        r.append(data.platform.content)

    print r


    datas = PlatformChannel.objects.filter(platform__content="android")

    print "r9 --> ", datas.query.__str__()

    r = []
    for data in datas:
        r.append(data.content)

    print r



