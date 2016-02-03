from django.conf.urls import patterns, url, include

from . import views

urlpatterns = [
    url(r'^$', views.JobList.as_view(), name='job_list'),
    url(r'^(?P<pk>\d+)$', views.JobDetail.as_view(), name='job_detail'),
    url(r'^create$', views.JobCreate.as_view(), name='job_create'),
    url(r'^(?P<pk>\d+)/update$', views.JobUpdate.as_view(), name='job_update'),    
]
