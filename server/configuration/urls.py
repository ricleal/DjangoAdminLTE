from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ConfigurationList.as_view(), name='configuration_list'),
    url(r'^(?P<pk>\d+)/$', views.ConfigurationDetail.as_view(), name='configuration_detail'),
    #url(r'^(?P<pk>\d+)/$', views.ConfigurationUpdate.as_view(), name='configuration_update'),
    #url(r'^(?P<pk>\d+)/$', views.ConfigurationCreate.as_view(), name='configuration_create'),
    
#     url(r'^(?P<pk>\d+)/delete$', views.ConfigurationDelete.as_view(), name='configuration_delete'),
#     url(r'^(?P<pk>\d+)/edit$', views.ConfigurationUpdate.as_view(), name='configuration_update'),
#     url(r'^(?P<pk>\d+)/duplicate$', views.ConfigurationDuplicate.as_view(), name='configuration_duplicate'),
                
]
