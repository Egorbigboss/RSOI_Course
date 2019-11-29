from django.conf.urls import url, include
from DeliveryApp import views
from django.urls import path

urlpatterns = [
    url(r'^delivery/user/(?P<user_id>[0-9a-f-]+)/$',views.ConcreteUserDeliveryView.as_view()),
    url(r'^delivery/(?P<uuid>[0-9a-f-]+)/$', views.ConcreteDeliveryView.as_view())
]
