# Generated by Django 4.2.6 on 2023-11-18 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('msg_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователю'),
        ),
    ]
