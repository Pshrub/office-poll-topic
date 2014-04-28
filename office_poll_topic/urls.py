from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'office_poll_topic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^poll/', include('poll.urls', namespace='poll') ),
    url(r'^admin/', include(admin.site.urls) ),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout', 'django.contrib.auth.views.logout'),
)
