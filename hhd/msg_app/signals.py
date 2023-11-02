from asgiref.sync import async_to_sync

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from channels.layers import get_channel_layer

from .models import MessageHistory, Message


@receiver(pre_save, sender=Message, weak=False)
def pre_message_save_handler(**kwargs):
    pass


@receiver(post_save, sender=Message, weak=False)
def message_save_handler(instance, created, **kwargs):
    async_to_sync(get_channel_layer().group_send)(
        instance.to_user.profile_set.first().chat_room,
        {
            'type': 'chat_message',
            'message': instance.text,
            'created': created
        }
    )
    if instance.from_user.profile_set.first().is_guest:
        async_to_sync(get_channel_layer().group_send)(
            'stuff',
            {
                'type': 'chat_message',
                'message': instance.text,
                'created': created
            }
        )
