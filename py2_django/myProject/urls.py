from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)

# hello
from hello import hello_django

urlpatterns += patterns('',
    url(r'^$', hello_django),
)

# learn
from my_django.learn.views import hello, hello1, mybook, view

urlpatterns += patterns('',
    url(r'^hello$', hello),
    url(r'^hello/(\d+)$', hello1),
    url(r'^view$', view),
    url(r'^mybook$', mybook),
)

from my_django.learn.views import views, view1, view2

urlpatterns += patterns('',
    url(r'^view1$', views(view1)),
    url(r'^view2$', views(view2)),
)

# calc
urlpatterns += patterns('',
    url(r'^add$', 'calc.views.add', name='add'),
)