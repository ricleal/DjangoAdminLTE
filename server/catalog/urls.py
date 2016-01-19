from django.conf.urls import patterns, url, include

from . import views

urlpatterns = [
    url(r'^$', views.Instruments.as_view(), name='list_instruments'),
    url(r'^(?P<instrument>[\w\-]+)/$', views.IPTSs.as_view(), name='list_iptss'),
    url(r'^(?P<instrument>[\w\-]+)/(?P<ipts>[\w\-\.]+)/$',  views.Runs.as_view(), name='list_runs'),
    url(r'^(?P<instrument>[\w\-]+)/json$', views.get_iptss_json, name='list_iptss_json'),
    url(r'^(?P<instrument>[\w\-]+)/(?P<ipts>[\w\-\.]+)/json$',  views.get_runs_json, name='list_runs_json'),
]
