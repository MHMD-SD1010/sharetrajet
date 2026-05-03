from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from app.notifications.models import Notification
from app.reservations.models import Rating, Reservation
from app.trajets.models import Trajet

User = get_user_model()


@receiver(post_save, sender=Reservation)
def create_reservation_notification(sender, instance, created, **kwargs):
    """
    Crée une notification lors d'une nouvelle réservation
    """
    if created:
        Notification.objects.create(
            recipient=instance.trajet.conducteur,
            sender=instance.passager,
            type="RESERVATION_REQUEST",
            content=f"Nouvelle demande de réservation de {instance.passager.full_name}",
            related_model="Reservation",
            related_id=instance.id,
        )


@receiver(post_save, sender=Rating)
def create_rating_notification(sender, instance, created, **kwargs):
    """
    Crée une notification lors d'une nouvelle évaluation
    """
    if created:
        Notification.objects.create(
            recipient=instance.rated,
            sender=instance.rater,
            type="RATING_RECEIVED",
            content=f"{instance.rater.full_name} vous a évalué {instance.note}/5",
            related_model="Rating",
            related_id=instance.id,
        )


@receiver(pre_delete, sender=Trajet)
def notify_trajet_deletion(sender, instance, **kwargs):
    """
    Notifie les passagers lors de la suppression d'un trajet
    """
    for reservation in instance.reservations.filter(
        status__in=["PENDING", "CONFIRMED"]
    ):
        Notification.objects.create(
            recipient=reservation.passager,
            sender=instance.conducteur,
            type="TRAJET_CANCELLED",
            content=f"Le trajet {instance.ville_depart} → {instance.ville_arrivee} a été supprimé",
            related_model="Trajet",
            related_id=instance.id,
        )


@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    """
    Crée une notification de bienvenue pour les nouveaux utilisateurs
    """
    if created:
        Notification.objects.create(
            recipient=instance,
            type="MESSAGE_RECEIVED",
            content=f"Bienvenue sur share trajet, {instance.first_name or 'cher utilisateur'}! "
            f"Commencez par compléter votre profil et vérifier vos documents.",
        )
