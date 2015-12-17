from django.conf.urls import patterns, url, include

from .views import list_instruments, list_iptss

urlpatterns = [
    url(r'^$', list_instruments, name='list_instruments'),
    url(r'^(?P<instrument>[\w]+)/$', list_iptss, name='list_iptss'),
]
