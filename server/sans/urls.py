from django.conf.urls import url
from .eqsans import views as eqsans


urlpatterns = [
    url(r'^EQ-SANS/$', eqsans.ConfigurationList.as_view(), name='eq-sans_configuration_list'),
    url(r'^EQ-SANS/(?P<pk>\d+)/$', eqsans.ConfigurationDetail.as_view(), name='eq-sans_configuration_detail'),
    url(r'^EQ-SANS/create$', eqsans.ConfigurationCreate.as_view(), name='eq-sans_configuration_create'),
    url(r'^EQ-SANS/(?P<pk>\d+)/update$', eqsans.ConfigurationUpdate.as_view(), name='eq-sans_configuration_update'),
    
    #url(r'^(?P<pk>\d+)/$', views.ConfigurationUpdate.as_view(), name='configuration_update'),
    #url(r'^(?P<pk>\d+)/$', views.ConfigurationCreate.as_view(), name='configuration_create'),
    
#     url(r'^(?P<pk>\d+)/delete$', views.ConfigurationDelete.as_view(), name='configuration_delete'),
#     url(r'^(?P<pk>\d+)/edit$', views.ConfigurationUpdate.as_view(), name='configuration_update'),
#     url(r'^(?P<pk>\d+)/duplicate$', views.ConfigurationDuplicate.as_view(), name='configuration_duplicate'),
                
]