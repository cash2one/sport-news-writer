from django.conf.urls import patterns, include, url
from writer.views import base, news

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', base),
                       (r'^news/(\d+)/$', news),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
