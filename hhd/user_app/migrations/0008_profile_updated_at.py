# Generated by Django 4.2.6 on 2023-11-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_profile_phone_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
    ]
