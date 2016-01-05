from django.conf.urls import patterns, url, include

from . import views

urlpatterns = [
    url(r'^$', views.Instruments.as_view(), name='list_instruments'),
    url(r'^(?P<instrument>[\w\-]+)/$', views.IPTSs.as_view(), name='list_iptss'),
    url(r'^(?P<instrument>[\w]+)/(?P<ipts>[\w\-\.]+)/$',  views.Runs.as_view(), name='list_runs'),
]
