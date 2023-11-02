from django.contrib import admin

from .models import Message, MessageHistory


# Register your models here.
admin.site.register(Message)
admin.site.register(MessageHistory)
