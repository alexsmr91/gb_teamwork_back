from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    is_superuser = serializers.BooleanField()

    class Meta:
        model = Profile
        fields = [
            'username',
            'chat_room',
            'is_guest',
            'is_superuser',
        ]
