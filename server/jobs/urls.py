from django.conf.urls import patterns, url, include

from . import views

urlpatterns = [
    url(r'^$', views.JobList.as_view(), name='job_list'),
    url(r'^(?P<pk>\d+)$', views.JobDetail.as_view(), name='job_detail'),
    # Create object based on a generic relation
    url(r'^create/(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<key>\d+)$', views.JobCreate.as_view(), name='job_create'),
    url(r'^(?P<pk>\d+)/update$', views.JobUpdate.as_view(), name='job_update'),
    url(r'^(?P<pk>\d+)/submission', views.JobSubmission.as_view(), name='job_submission'),
    url(r'^(?P<pk>\d+)/query', views.JobQuery.as_view(), name='job_query'),
    url(r'^(?P<pk>\d+)/delete', views.JobDelete.as_view(), name='job_delete'),
    url(r'^(?P<pk>\d+)/results', views.JobResults.as_view(), name='job_results'),
]
