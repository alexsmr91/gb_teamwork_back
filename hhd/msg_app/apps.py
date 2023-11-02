from django.apps import AppConfig


class ApiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'msg_app'
    verbose_name = 'Сообщения'

    def ready(self):
        import msg_app.signals
