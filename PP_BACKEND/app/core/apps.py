from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.core"

    def ready(self):
        # Import signals or perform startup registration here if needed
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
