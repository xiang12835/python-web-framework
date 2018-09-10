from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'app.user.views.system_user_list', name=u'home'),
    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'sign_in_new.html'}, name="signin"),
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login',  name="signout"),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content/', include('app.content.urls')),
    url(r'^user/', include('app.user.urls')),

)
