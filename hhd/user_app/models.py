from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Гость", null=False, blank=False)
    phone_code = models.CharField(max_length=4, null=True, blank=False, verbose_name='Код авторизации')
    auth_attempts = models.IntegerField(default=0, null=False, blank=False, verbose_name='Попыток авторизации')
    sending_time = models.DateTimeField(verbose_name='Время отправки SMS', null=True, blank=False)
    chat_room = models.CharField(max_length=40, verbose_name='Токен чата', unique=True, null=True)
    is_guest = models.BooleanField(default=True, verbose_name='Статус гостя', null=False, blank=False)
    updated_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.user.username} - {'Гость' if self.is_guest else 'Сотрудник'}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
