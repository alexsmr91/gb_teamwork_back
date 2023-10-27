from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserListAPIView.as_view(), name='api_users'),

]
