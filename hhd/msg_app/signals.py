from asgiref.sync import async_to_sync

from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer

from .models import Message


@receiver(post_save, sender=Message, weak=False)
def message_save_handler(instance: Message, created, **kwargs):
    send = async_to_sync(get_channel_layer().group_send)
    if instance.to_user is not None:
        send(
            instance.to_user.profile.chat_room,
            {
                'type': 'chat_message'
            }
        )
        if instance.from_user.profile.is_guest:
            send(
                instance.from_user.profile.chat_room,
                {
                    'type': 'chat_message'
                }
            )
        else:
            send(
                'stuff',
                {
                    'type': 'chat_message',
                    'user': instance.to_user.pk,
                }
            )
    else:
        if instance.from_user.profile.is_guest:
            send(
                instance.from_user.profile.chat_room,
                {
                    'type': 'chat_message'
                }
            )
        send(
            'stuff',
            {
                'type': 'chat_message',
                'user': instance.from_user.pk,
            }
        )

