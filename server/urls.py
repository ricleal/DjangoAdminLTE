"""

Main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings

from .catalog.views import list_instruments

# attempts to import an admin module in each installed application
# admin.autodiscover()

urlpatterns = [
    url(r'^$', list_instruments, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^catalog/', include('server.catalog.urls', namespace='catalog') ),
    url(r'^users/', include('server.users.urls', namespace='users') ),
]
