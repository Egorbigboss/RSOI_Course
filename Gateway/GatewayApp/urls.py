from django.conf.urls import url
from GatewayApp import views


urlpatterns = [
     url(r'^cloths/$', views.ClothsView.as_view()),
     url(r'^cloths/create/$',views.CreateCloth.as_view()),
     url(r'^cloths/(?P<cloth_uuid>[0-9a-f-]+)/$',
         views.ConcreteClothView.as_view()),

     url(r'^orders/$', views.OrdersView.as_view()),
     url(r'^orders/(?P<order_uuid>[0-9a-f-]+)/$',
         views.ConcreteOrderView.as_view()),
     url(r'^orders/user/create/$',views.CreateOrderView.as_view()),
     url(r'^orders/user/(?P<user_id>\d+)/$',views.ConcreteUserOrdersView.as_view()),

     url(r'^delivery/user/(?P<user_id>\d+)/$', views.ConcreteUserDeliveryView.as_view()),
     url(r'^delivery/user/create/$',views.CreateDeliveryList.as_view())
]
