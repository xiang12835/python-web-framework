from django.conf.urls import patterns, include, url

from django_py2.content.views import hello, hello1, mybook, view, views, view1, view2

urlpatterns = patterns(
    '',
    url(r'^hello$', hello),
    url(r'^hello/(\d+)$', hello1),
    url(r'^view$', view),
    url(r'^mybook$', mybook),
    url(r'^view1$', views(view1)),
    url(r'^view2$', views(view2)),
)

