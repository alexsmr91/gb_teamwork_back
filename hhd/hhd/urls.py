"""
URL configuration for hhd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from user_app.views import *
from msg_app.views import *
from rest_framework.authtoken import views
from msg_app.views import MessageAPIView


router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='Message')

urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-token-auth-guest/', get_auth_token_with_code_view),
    path('send-sms/<int:phone>/', send_sms_view),
    path('profile/', profile_api_view),
    path('messages/', MessageAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

