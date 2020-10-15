from django.conf.urls import url, include
from OrdersApp import views
from django.urls import path

urlpatterns = [
    url(r'^orders/all/$', views.AllOrdersView.as_view()),
    url(r'^orders/user/(?P<user_id>[0-9a-f-]+)/$',views.ConcreteUserOrdersView.as_view()),
    url(r'^orders/(?P<order_uuid>[0-9a-f-]+)/$', views.ConcreteOrderView.as_view()),
    url(r'^orders/stats/$',views.StatsView.as_view())
]
