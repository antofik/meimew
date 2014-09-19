from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'meimew.views.home', name='home'),
)
