from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'
    verbose_name = 'Профили гостей'

    def ready(self):
        import user_app.signals
