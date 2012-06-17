from django.conf.urls.defaults import *

urlpatterns = patterns('management.views',
    url(r'^$', 'manage', name='manage'),
)
