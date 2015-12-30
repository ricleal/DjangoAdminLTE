from django.conf.urls import patterns, url, include

from . import views
#from .views import 

urlpatterns = [
    url(r'^$', views.ConfigurationList.as_view(), name='configuration_list'),
]
