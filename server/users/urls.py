from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^login$', views.perform_login, name="login"),
    url(r'^logout$', views.perform_logout, name="logout"),
    url(r'^profile/$', views.ProfileCreate.as_view(), name="profile_create"),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileUpdate.as_view(), name="profile_update"),
]

