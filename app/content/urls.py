# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',

    # for common
    url(r'^common/img_upload', 'content.views.img_upload', name='img_upload'),
    url(r'^common/update_status_int', 'content.views.common_update_status_int', name="common_update_status_int"),
    url(r'^common/update_status_str', 'content.views.common_update_status_str', name="common_update_status_str"),

)


urlpatterns += patterns(
    '',

)

