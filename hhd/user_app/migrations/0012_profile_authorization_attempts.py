# Generated by Django 4.2.6 on 2023-11-03 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_remove_profile_authorization_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='authorization_attempts',
            field=models.IntegerField(default=0, verbose_name='Попыток авторизации'),
        ),
    ]
