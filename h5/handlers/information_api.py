#coding=utf-8
from h5.view.base import BaseHandler , CachedPlusHandler
from h5.document.doc_tools import *
from django.conf import settings
from app.bskgk.models import CourseInfo , InfoCarousel , VideoInfo
from app.bskcommon.models import BskUser
import time, datetime
from wi_model_util.imodel import attach_foreignkey , queryset_to_dict
from app.infomation.models import *
import tornado


@handler_define
class ArticleHtml(tornado.web.RequestHandler):

    @api_define("ArticleHtml", r'/is/:id',
                [
                Param(':id', True, str, "1", "1", u'文章id'),
                Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
                Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
                description="文章HTML")
    def get(self,xid,x):
        from django.conf import settings
        from django.template import Context, Template
        import os,sys
        
        project = os.path.realpath(os.path.dirname(__file__))
        t_path = os.path.realpath(os.path.join(project, '..', '..','app/infomation/templates/info_article/show.html'))
        template = open(t_path).read()

        short_id = xid

        _id = ShortID().toID(short_id)
        
        article = Article.objects.get(pk=_id)

        t = Template(template)

        data = t.render(Context({
            'article': article, 
            'created_at': article.created_at.strftime('%Y-%m-%d'),
            }))

        self.finish(data)


@handler_define
class TopicHtml(tornado.web.RequestHandler):
    @api_define("TopicHtml", r'/t/:id', [
        Param(':id', True, str, "1", "1", u'文章id'),
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')
    ], description="活动话题HTML")
    def get(self, xid, x):
        from django.template import Context, Template
        import os

        project = os.path.realpath(os.path.dirname(__file__))
        t_path = os.path.realpath(os.path.join(project, '..', '..', 'app/infomation/templates/topic/topic_show.html'))
        template = open(t_path).read()

        short_id = xid

        _id = ShortID().toID(short_id)
        topic = Topic.objects.get(pk=_id)

        t = Template(template)

        data = t.render(Context({
            'topic': topic,
            'created_at': topic.created_at.strftime('%Y-%m-%d'),
        }))

        self.finish(data)


@handler_define
class EditorHtml(tornado.web.RequestHandler):
    @api_define("EditorHtml", r'/e/:id', [
        Param(':id', True, str, "1", "1", u'文章id'),
        Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
        Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')
    ], description="文章HTML")
    def get(self, xid, x):
        from django.template import Context, Template
        import os

        project = os.path.realpath(os.path.dirname(__file__))
        t_path = os.path.realpath(os.path.join(project, '..', '..', 'app/infomation/templates/editor/editor_show.html'))
        template = open(t_path).read()

        short_id = xid

        _id = ShortID().toID(short_id)
        editor = Editor.objects.get(pk=_id)

        t = Template(template)

        data = t.render(Context({
            'editor': editor,
            'created_at': editor.created_at.strftime('%Y-%m-%d'),
        }))

        self.finish(data)


# @handler_define
# class PageShowHtml(tornado.web.RequestHandler):

#     @api_define("PageShowHtml", r'/p/:id',
#                 [
#                 Param(':id', True, str, "1", "1", u'专题id'),
#                 Param('guid', False, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'用户guid'),
#                 Param('pid', True, str, "69b81504767483cf", "69b81504767483cf", u'pid')],
#                 description="专题HTML")
#     def get(self,xid,x):
#         from django.template import Context, Template
#         import os

#         project = os.path.realpath(os.path.dirname(__file__))
#         t_path = os.path.realpath(os.path.join(project, '..', '..', 'app/index/templates/page/show.html'))
#         template = open(t_path).read()

#         short_id = xid
#         sid = ShortID()
#         page_id = sid.toID(short_id)
#         page = Page.query(page_id)
#         # if page.folder:
#         #     return HttpResponseBadRequest('invalid id')

#         app = page.app
#         content = page.data_for_view()
#         content["STATIC_URL"] = "http://cms.platform.winlesson.com/static/"
#         content.update({"page_id": sid.toHex(page_id), 'ptype': 'p', 'app': app})
        
        
#         t = Template(template)
#         data = t.render(Context(content))
        

#         self.finish(data)



