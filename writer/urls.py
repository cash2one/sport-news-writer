from django.conf.urls import patterns, include, url
from writer.views import base, news

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', base),
    url(r'^(?P<campionat>[\w-]+)/(?P<title>[\w-]+)/$', news, name='news'),
    url(r'^(?P<campionat>[\w-]+)/$', base, name='campionat'),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
