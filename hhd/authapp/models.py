from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    room_number = models.CharField(max_length=64)
    phone = models.IntegerField(default=79991112233)
    role = models.IntegerField(default=1)         # подумать над ролями, создать таблицу с ролями
