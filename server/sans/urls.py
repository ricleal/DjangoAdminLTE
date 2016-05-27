from django.conf.urls import url, include, patterns
from django.contrib import admin


urlpatterns = [
    url(r'^EQ-SANS/', include('server.sans.eqsans.urls', namespace='eqsans') ),
    url(r'^BIOSANS/', include('server.sans.biosans.urls', namespace='biosans') ),
]
