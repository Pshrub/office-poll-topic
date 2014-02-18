from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'office_poll_topic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^poll/', include('poll.urls') ),
    url(r'^admin/', include(admin.site.urls) ),
)
