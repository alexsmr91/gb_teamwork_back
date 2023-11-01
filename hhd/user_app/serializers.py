from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'date_joined'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'phone',
        ]
