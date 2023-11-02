from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Profile, User


@receiver(post_save, sender=User, weak=False)
def create_user_handler(instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            chat_room=Token.generate_key()
        )
