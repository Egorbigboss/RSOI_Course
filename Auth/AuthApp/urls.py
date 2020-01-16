
from django.conf.urls import url
from AuthApp import views


urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^check_token/$', views.CheckToken.as_view()),
]