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

urlpatterns += patterns('',
    url(r'^$', hello_django),
)