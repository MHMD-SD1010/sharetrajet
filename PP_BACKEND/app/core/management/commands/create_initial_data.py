from django.core.management.base import BaseCommand

from app.users.models import Preference, Role


class Command(BaseCommand):
    help = "Crée les données initiales (rôles et préférences)"

    def handle(self, *args, **options):
        # Créer les rôles
        roles_data = [
            {"name": "USER", "description": "Utilisateur standard"},
            {"name": "ADMIN", "description": "Administrateur"},
            {"name": "MODERATOR", "description": "Modérateur"},
        ]

        roles_created = 0
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]},
            )
            if created:
                roles_created += 1
                self.stdout.write(f"Rôle créé: {role.name}")

        # Créer les préférences
        preferences_data = [
            {
                "name": "Musique",
                "description": "Aime écouter de la musique pendant le trajet",
            },
            {"name": "Silence", "description": "Préfère le silence pendant le trajet"},
            {"name": "Discussion", "description": "Aime discuter pendant le trajet"},
            {"name": "Fumeur", "description": "Fume ou accepte les fumeurs"},
            {
                "name": "Non-fumeur",
                "description": "Ne fume pas et n'accepte pas les fumeurs",
            },
            {
                "name": "Animaux acceptés",
                "description": "Accepte les animaux de compagnie",
            },
            {"name": "Climatisation", "description": "Véhicule climatisé"},
        ]

        prefs_created = 0
        for pref_data in preferences_data:
            pref, created = Preference.objects.get_or_create(
                name=pref_data["name"],
                defaults={"description": pref_data["description"]},
            )
            if created:
                prefs_created += 1
                self.stdout.write(f"Préférence créée: {pref.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDonnées initiales créées avec succès!\n"
                f"Rôles: {roles_created}, Préférences: {prefs_created}"
            )
        )
