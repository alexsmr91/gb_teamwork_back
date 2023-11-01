from uuid import uuid4
from django.db import models
from django.utils import timezone
from hhd.settings import OTP_LEN
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    username = models.CharField(max_length=64)
    room_number = models.CharField(max_length=64)
    phone = models.IntegerField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=OTP_LEN)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "phone"  # использовать телефон вместо юзернейм для логина
    REQUIRED_FIELDS = ["username"]  # чтобы работала команда createsuperuser

    # str == fix for DRF template
    def __str__(self):
        if self.username:
            return f'{self.username} (+{self.phone})'
        else:
            return f'+{self.phone}'

    def generate_code(self):
        from random import choices
        code = ''.join(choices('0123456789', k=OTP_LEN))
        print('Где то здесь должна быть отправка СМС')
        print(f'Your SMS CODE: {code}')
        self.otp = code
        self.otp_created_at = timezone.now()
        self.save()

    def verify_code(self, code):
        if self.otp == code:
            self.is_verified = True
            self.save()
            return self
        return None
