#coding=utf-8

from h5.views.base import BaseHandler , CachedPlusHandler
from h5.document.doc_tools import *
from django.conf import settings
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
import tornado


@handler_define
class CourseShareHtml(tornado.web.RequestHandler):

    @api_define("CourseShareHtml", r'/h_five/course/share/:id',
                [
                Param(':id', True, str, "1", "1", u'课程id'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
                description="课程ShareH5")
    def get(self,xid,x):
        course_id = xid

        videoList = VideoInfo.get_share_videos(course_id)

        if videoList:
            course_info = CourseInfo.objects.filter(course_id=course_id).first()

            index = 0
            for video in videoList:
                #print video
                duration = int(video["duration"])
                if duration:
                    fen = int(duration / 60)
                    miao = int(duration - int(duration / 60) * 60)
                    if miao < 10:
                        miao = "0{}".format(miao)

                    video["duration"] = \
                        "%s:%s" % (fen, miao)
                else:
                    video["duration"] = "00:00"

                video["videoIndex"] = index +1

                index += 1

            return self.render("play_video.html", **{"videoList": videoList,"course_info":course_info})
        else:
            self.redirect("http://a.app.qq.com/o/simple.jsp?pkgname=gwy.winlesson.app")



@handler_define
class ApiUploadImageHandler(BaseHandler):

    @api_define('ApiUploadImageHandler ', '/t/upload/image', [
        Param('image', True, file, "", "", u'api上传图片'),
    ], description="上传图片")
    def post(self):
        import random
        from app.api_util.qcloud.qcloud_file import QCloudFile
        file_metas = self.request.files["image"]
        img = None
        for meta in file_metas:
            img = meta['body']
            break


        qf = QCloudFile()
        data = img
        filename = "ab_%s_%s_%s.png" % (random.randint(1,1000000000),random.randint(1,1000000000),random.randint(1,1000000000),)

        data = qf.upload_data(data,filename)
        

        return self.write({
                            "data":data,
                            "url":"http://picture-10004299.file.myqcloud.com/shenlun/%s" % filename
                        })






