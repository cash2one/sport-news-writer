from django.conf.urls import patterns, include, url
from writer.views import base, news, rss

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', base),
    url(r'^(?P<campionat>[\w-]+)/(?P<title>[\w-]+)/$', news, name='news'),
    url(r'^(?P<campionat>[\w-]+)/$', base, name='campionat'),
    url(r'^rss/$', rss, name='rss'),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

)
