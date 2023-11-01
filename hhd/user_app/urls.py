from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserListAPIViewSet, SMSCodeAuthView

router = DefaultRouter()
router.register('users', UserListAPIViewSet)


urlpatterns = [
    path('api/users', include(router.urls)),
    path('otp-auth', SMSCodeAuthView.as_view()),
]
