from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
     path('admin/', admin.site.urls),
     url('',include('frontend.urls')), 
     url(r'^api/', include('GatewayApp.urls')),
]
