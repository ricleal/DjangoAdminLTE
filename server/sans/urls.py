from django.conf.urls import url
from .eqsans import views as eqsans


urlpatterns = [
    url(r'^EQ-SANS/$', eqsans.ConfigurationList.as_view(), name='eq-sans_configuration_list'),
    url(r'^EQ-SANS/(?P<pk>\d+)/$', eqsans.ConfigurationDetail.as_view(), name='eq-sans_configuration_detail'),
    url(r'^EQ-SANS/create$', eqsans.ConfigurationCreate.as_view(), name='eq-sans_configuration_create'),
    url(r'^EQ-SANS/(?P<pk>\d+)/update$', eqsans.ConfigurationUpdate.as_view(), name='eq-sans_configuration_update'),
    
    url(r'^EQ-SANS/reduction/$', eqsans.ReductionList.as_view(), name='eq-sans_reduction_list'),
    url(r'^EQ-SANS/reduction/(?P<pk>\d+)/$', eqsans.ReductionDetail.as_view(), name='eq-sans_reduction_detail'),
    url(r'^EQ-SANS/reduction/create$', eqsans.ReductionCreate.as_view(), name='eq-sans_reduction_create'),
]