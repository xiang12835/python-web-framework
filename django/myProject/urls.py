from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from hello import hello_django

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^$', hello_django),
)