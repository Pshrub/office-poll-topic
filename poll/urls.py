from django.conf.urls import patterns, url

from poll import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex polls/1/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: polls/1/results
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: polls/1/vote
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
