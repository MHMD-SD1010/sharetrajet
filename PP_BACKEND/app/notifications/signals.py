from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.users.models import User

from .models import Message
from .utils import notify_new_message, notify_welcome

print("FICHIER app/notifications/signals.py CHARGÉ")
print("=" * 80)


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    """Envoie une notification de bienvenue lors de la création d'un compte"""
    if getattr(settings, "TESTING", False):
        return
    if created and instance.is_active:
        notify_welcome(instance)


@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    """
    Envoie une notification pour TOUS les messages
    """
    if not created:
        return

    print("=" * 80)
    print("SIGNAL MESSAGE DÉCLENCHÉ")
    print(f"Sender: {instance.sender.full_name}")
    print(f"Is Group: {instance.is_group_message}")
    print("=" * 80)

    # Messages de GROUPE
    if instance.is_group_message and instance.trajet:
        trajet = instance.trajet
        participants = []

        if trajet.conducteur != instance.sender:
            participants.append(trajet.conducteur)

        for reservation in trajet.reservations.filter(status="CONFIRMED"):
            if reservation.passager != instance.sender:
                participants.append(reservation.passager)

        print(f"{len(participants)} participants à notifier")

        for participant in participants:
            notify_new_message(
                sender=instance.sender,
                recipient=participant,
                message=instance,
            )

    # Messages PRIVÉS
    elif not instance.is_group_message and instance.receiver:
        print(f"Message privé vers {instance.receiver.full_name}")
        notify_new_message(
            sender=instance.sender,
            recipient=instance.receiver,
            message=instance,
        )


# NOTE: Les signals pour Reservation sont maintenant gérés dans app/reservations/signals.py
# pour éviter les doublons et avoir une logique centralisée
