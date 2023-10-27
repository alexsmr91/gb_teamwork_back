from . import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'room_number', 'phone', 'password')
