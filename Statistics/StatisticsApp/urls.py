from django.conf.urls import url, include
from StatisticsApp import views
from django.urls import path

urlpatterns = [
    url(r'^stats/all/$', views.CreateStatsView.as_view()),
    url(r'^stats/(?P<stats_uuid>[0-9a-f-]+)/$', views.ConcreteStatsView.as_view()),
    url(r'^stats/update/$', views.UpdateStatsView.as_view())
]
