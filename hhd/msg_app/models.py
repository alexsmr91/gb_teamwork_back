from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    text = models.TextField(verbose_name='Текст', null=False, blank=False)
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name='От пользователя',
        related_name='from_user'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        verbose_name='Пользователю',
        related_name='to_user'
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} - {self.created_at}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MessageHistory(models.Model):
    new_text = models.TextField(verbose_name='Новое сообщение', null=False, blank=False)
    old_text = models.TextField(verbose_name='Старое сообщение', null=False, blank=False)
    user_changed = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False, verbose_name='Пользователь')
    message = models.ForeignKey(Message, on_delete=models.PROTECT, null=False, blank=False, verbose_name='Сообщение')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f"{self.user_changed} -> {self.message} - {self.created_at}"

    class Meta:
        verbose_name = 'История сообщения'
        verbose_name_plural = 'История сообщений'
