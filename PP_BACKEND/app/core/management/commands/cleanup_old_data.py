from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.notifications.models import Notification
from app.trajets.models import Trajet
from app.users.models import RefreshToken


class Command(BaseCommand):
    help = "Nettoie les anciennes données (trajets terminés, notifications lues, tokens expirés)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Nombre de jours à conserver (défaut: 90)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mode simulation, n'effectue aucune suppression",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        cutoff_date = timezone.now() - timedelta(days=days)

        if dry_run:
            self.stdout.write(
                self.style.WARNING("MODE SIMULATION - Aucune suppression réelle")
            )

        # Nettoyer les trajets terminés/annulés anciens
        old_trajets = Trajet.objects.filter(
            date__lt=cutoff_date.date(), status__in=["COMPLETED", "CANCELLED"]
        )
        trajets_count = old_trajets.count()

        if not dry_run:
            old_trajets.delete()

        self.stdout.write(f"Trajets à supprimer: {trajets_count}")

        # Nettoyer les notifications lues anciennes
        old_notifications = Notification.objects.filter(
            created_at__lt=cutoff_date, is_read=True
        )
        notifs_count = old_notifications.count()

        if not dry_run:
            old_notifications.delete()

        self.stdout.write(f"Notifications à supprimer: {notifs_count}")

        # Nettoyer les tokens expirés
        expired_tokens = RefreshToken.objects.filter(expires_at__lt=timezone.now())
        tokens_count = expired_tokens.count()

        if not dry_run:
            expired_tokens.delete()

        self.stdout.write(f"Tokens expirés à supprimer: {tokens_count}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nMode simulation terminé. "
                    "Relancez sans --dry-run pour effectuer le nettoyage réel."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nNettoyage terminé!\n"
                    f"Total supprimé: {trajets_count + notifs_count + tokens_count} éléments"
                )
            )
