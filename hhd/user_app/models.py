from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    phone = models.IntegerField(verbose_name="Номер телефона", null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Гость", null=False, blank=False)

    def __str__(self):
        return f"{self.pk} - "

    class Meta:
        unique_together = ('user_id', 'phone')
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
