from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.reservations"
    verbose_name = "Réservations"

    def ready(self):
        """Charge les signals au démarrage"""
        print("=" * 80)
        print("ReservationsConfig.ready() appelé")
        print("=" * 80)

        try:
            import app.reservations.signals  # noqa: F401

            print("Signals réservations chargés avec succès")
        except Exception as e:
            print(f"Erreur chargement signals réservations: {e}")
            import traceback

            traceback.print_exc()
