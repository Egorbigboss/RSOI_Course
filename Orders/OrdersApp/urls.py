from django.conf.urls import url, include
from OrdersApp import views
from django.urls import path

urlpatterns = [
    url(r'^orders/all/', views.AllOrdersView.as_view()),
    url(r'^orders/(?P<order_uuid>\w+)/$', views.ConcreteOrderView.as_view()),
]
