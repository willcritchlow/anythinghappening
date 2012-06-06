from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    url(r'^(?P<nc_id>[\d]+)/$', 'check', name='check'),
)
