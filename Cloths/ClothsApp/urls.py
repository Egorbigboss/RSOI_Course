from django.conf.urls import url, include
from ClothsApp import views
from django.urls import path

urlpatterns = [
    url(r'^cloths/all/$', views.AllClothsView.as_view()),
    url(r'^cloths/(?P<cloth_uuid>[0-9a-f-]+)/$', views.ConcreteClothView.as_view()),
]
