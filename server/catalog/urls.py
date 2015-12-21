from django.conf.urls import patterns, url, include

from .views import list_instruments, list_iptss, list_runs

urlpatterns = [
    url(r'^$', list_instruments, name='list_instruments'),
    url(r'^(?P<instrument>[\w]+)/$', list_iptss, name='list_iptss'),
    url(r'^(?P<instrument>[\w]+)/(?P<ipts>[\w\-\.]+)/$', list_runs, name='list_runs'),
]
