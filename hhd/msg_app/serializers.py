from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(source='from_user.username')
    to_user = serializers.StringRelatedField(source='to_user.username')

    class Meta:
        model = Message
        fields = [
            'text',
            'from_user',
            'to_user',
            'created_at',
            'updated_at',
        ]
