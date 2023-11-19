from rest_framework import serializers

from user_app.serializers import UserSerializer, User
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')
    updated_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'from_user',
            'to_user',
            'created_at',
            'updated_at',
        ]


class MessageCreateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    to_user = serializers.IntegerField(required=False)


class MessagesFilterSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    last_message_id = serializers.IntegerField(required=False)
    history = serializers.BooleanField(required=False)


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.CharField()
    from_user_id = serializers.IntegerField()
    is_guest_sender = serializers.BooleanField()
    last_message_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_message',
            'from_user_id',
            'is_guest_sender',
            'last_message_date',
        ]
