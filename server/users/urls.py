from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name="login"),
    url(r'^logout$', views.LogoutView.as_view(), name="logout"),
    url(r'^profile/$', views.ProfileCreate.as_view(), name="profile_create"),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileUpdate.as_view(), name="profile_update"),
    url(r'^users_json$', views.get_users_json, name="users_list_json"),
]

