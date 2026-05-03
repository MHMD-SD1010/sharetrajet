from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.notifications"
    verbose_name = "Notifications"

    def ready(self):
        """Charge les signals au démarrage de l'application"""
        print("=" * 80)
        print("NotificationsConfig.ready() appelé")
        print("=" * 80)

        try:
            import app.notifications.signals  # noqa: F401

            print("Signals notifications chargés avec succès")
        except Exception as e:
            print(f"Erreur chargement signals: {e}")
            import traceback

            traceback.print_exc()
