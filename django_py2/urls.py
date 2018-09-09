from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'content.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)

# content
from content.home import hello_django

urlpatterns += patterns('',
    url(r'^$', hello_django),
)

from django_py2.content.views import hello, hello1, mybook, view

urlpatterns += patterns('',
    url(r'^hello$', hello),
    url(r'^hello/(\d+)$', hello1),
    url(r'^view$', view),
    url(r'^mybook$', mybook),
)

from django_py2.content.views import views, view1, view2

urlpatterns += patterns('',
    url(r'^view1$', views(view1)),
    url(r'^view2$', views(view2)),
)

