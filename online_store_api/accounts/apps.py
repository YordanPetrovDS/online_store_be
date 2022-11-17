from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "online_store_api.accounts"

    def ready(self):
        from . import signals
