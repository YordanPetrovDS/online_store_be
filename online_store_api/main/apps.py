from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "online_store_api.main"

    def ready(self):
        from . import signals
