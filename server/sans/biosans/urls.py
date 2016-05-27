from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ConfigurationList.as_view(), name='configuration_list'),
    url(r'^(?P<pk>\d+)/$', views.ConfigurationDetail.as_view(), name='configuration_detail'),
    url(r'^create$', views.ConfigurationCreate.as_view(), name='configuration_create'),
    url(r'^(?P<pk>\d+)/update$', views.ConfigurationUpdate.as_view(), name='configuration_update'),
    url(r'^(?P<pk>\d+)/delete$', views.ConfigurationDelete.as_view(), name='configuration_delete'),
    url(r'^(?P<pk>\d+)/clone$', views.ConfigurationClone.as_view(), name='configuration_clone'),
    url(r'^(?P<pk>\d+)/assign/(?P<uid>\w{3})$', views.ConfigurationAssign.as_view(), name='configuration_assign'),

    url(r'^reduction/$', views.ReductionList.as_view(), name='reduction_list'),
    url(r'^reduction/(?P<pk>\d+)/$', views.ReductionDetail.as_view(), name='reduction_detail'),
    url(r'^reduction/create$', views.ReductionCreate.as_view(), name='reduction_create'),
    url(r'^reduction/(?P<pk>\d+)/update$', views.ReductionUpdate.as_view(), name='reduction_update'),
    url(r'^reduction/(?P<pk>\d+)/delete$', views.ReductionDelete.as_view(), name='reduction_delete'),
    url(r'^reduction/(?P<pk>\d+)/clone$', views.ReductionClone.as_view(), name='reduction_clone'),
    url(r'^reduction/(?P<pk>\d+)/script', views.ReductionScript.as_view(), name='reduction_script'),
]
