from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Met à jour les statistiques de tous les utilisateurs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id", type=int, help="ID d'un utilisateur spécifique à mettre à jour"
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.update_statistics()
                self.stdout.write(
                    self.style.SUCCESS(f"Statistiques mises à jour pour: {user.email}")
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Utilisateur avec ID {user_id} non trouvé")
                )
        else:
            users = User.objects.all()
            count = 0

            for user in users:
                user.update_statistics()
                count += 1

                if count % 100 == 0:
                    self.stdout.write(f"Traités: {count} utilisateurs...")

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nStatistiques mises à jour pour {count} utilisateurs!"
                )
            )
