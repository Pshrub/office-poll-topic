from django.conf.urls import patterns, url

from poll import views

urlpatterns = patterns('',
    # ex: /poll/
    url(r'^$', views.index, name='index'),
    # ex poll/1/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: poll/1/results
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: poll/1/vote
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # ex: poll/1/sendemail here is the view to send the emails for a given poll
    url(r'^(?P<poll_id>\d+)/sendemail/$', views.sendEmail, name='sendEmail'),
)
