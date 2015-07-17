from django.conf.urls import patterns, include, url
from writer.views import base, news, rss, team

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', base),
    url(r'^rss/$', rss, name='rss'),
    url(r'^rss/(?P<campionat>[\w-]+)/$', rss, name='rss_campionat'),
    url(r'^rss/(?P<campionat>[\w-]+)/(?P<team>[\w-]+)/$', rss, name='rss_team'),
    url(r'^(?P<campionat>[\w-]+)/echipe/(?P<team>[\w-]+)/$', team, name='team'),
    url(r'^(?P<campionat>[\w-]+)/(?P<title>[\w-]+)/$', news, name='news'),
    url(r'^(?P<campionat>[\w-]+)/$', base, name='campionat'),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

)
