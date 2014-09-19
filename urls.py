# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('')

if settings.DEBUG or True:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )

urlpatterns += patterns('',
        url(r'^upload/(?P<name>[^\.\\\/]{1,64})', 'meimew.views.upload', name='upload'),
        url(r'^get/(?P<slug>[^/\.]{1,64})', 'meimew.views.download', name='download'),
        url(r'^\=(?P<slug>[^/\.]{1,64})', 'meimew.views.download', name='download'),
        url(r'(?P<name>[^\.\\\/]{1,64})', 'meimew.views.entry', name='entry'),
        url(r'^.*$', 'meimew.views.home', name='home'),
    )
