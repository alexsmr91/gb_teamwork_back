from . import serializers
from .models import CustomUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class UserListAPIViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = CustomUser.objects.get_queryset().order_by('date_joined')

    def get_serializer_class(self):
        if self.request.version == '1.0':
            return serializers.UserSerializer
        # if self.request.version == '2.0':
        #     pass
