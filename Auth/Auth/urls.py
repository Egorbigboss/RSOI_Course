from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken import views
from oauth2_provider import views as oauth2_views
from AuthApp.views import LoginOAuth2

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/token_auth/', views.obtain_auth_token),
    url(r'^api/', include('AuthApp.urls')),
    url(r'^accounts/login/$', LoginOAuth2.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]