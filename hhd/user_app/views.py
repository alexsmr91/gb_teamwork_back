from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins, permissions
from .serializers import UserSerializer
from .models import CustomUser
from .backends import CustomBackend
from rest_framework.authtoken.models import Token


class UserListAPIViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = CustomUser.objects.get_queryset().order_by('date_joined')

    def get_serializer_class(self):
        return UserSerializer


class SMSCodeAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        phone = request.data.get('phone')
        code = request.data.get('code')
        if isinstance(phone, int):
            user = CustomBackend.authenticate_by_sms(phone=phone, code=code)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                response = {'token': f'{token}'}
            else:
                response = {'ok': 'sending sms code'}
            print(user)
        else:
            response = {'notok': 'field phone is required'}

        return Response(response)
