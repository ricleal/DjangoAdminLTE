from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.perform_login, name="login"),
    url(r'^logout$', views.perform_logout, name="logout"),
]
