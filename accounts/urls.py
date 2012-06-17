from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
)

urlpatterns += patterns('accounts.views',
    url(r'^create/$', 'create', name='create'),
    url(r'^logout/$', 'logout_view', name='logout'),
)
