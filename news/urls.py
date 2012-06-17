from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    url(r'^$', 'check', name='home'),
    url(r'^(?P<nc_id>[\d]+)/$', 'check', name='check'),
)
