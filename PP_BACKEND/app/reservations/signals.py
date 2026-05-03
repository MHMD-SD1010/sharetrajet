from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from app.notifications.models import Conversation, Message
from app.notifications.utils import (
    notify_reservation_approved,
    notify_reservation_cancelled,
    notify_reservation_rejected,
    notify_reservation_request,
)

from .models import Reservation

print("=" * 80)
print("FICHIER app/reservations/signals.py CHARGÉ")
print("=" * 80)


@receiver(post_save, sender=Reservation)
def handle_reservation_notifications(sender, instance, created, **kwargs):
    """
    Gère les notifications ET la création de conversation de groupe
    """
    _log_reservation_signal(instance, created)

    if created:
        _handle_new_reservation(instance)
    else:
        _handle_status_change(instance)


def _log_reservation_signal(instance, created):
    """Log reservation signal information."""
    print("=" * 80)
    print("SIGNAL RESERVATION DÉCLENCHÉ")
    print(f"   ID: {instance.id}")
    print(f"   Status: {instance.status}")
    print(f"   Created: {created}")
    print(f"   Passager: {instance.passager.full_name}")
    print(f"   Conducteur: {instance.trajet.conducteur.full_name}")
    print("=" * 80)


def _handle_new_reservation(instance):
    """Handle new reservation creation."""
    if instance.status != "PENDING":
        return

    print("Nouvelle réservation - Notification au conducteur")
    try:
        notify_reservation_request(
            driver=instance.trajet.conducteur,
            passenger=instance.passager,
            reservation=instance,
        )
        print("Notification RESERVATION_REQUEST envoyée")
    except Exception as e:
        print(f"Erreur notification REQUEST: {e}")
        import traceback

        traceback.print_exc()


def _handle_status_change(instance):
    """Handle reservation status changes."""
    print(f"Changement de statut détecté: {instance.status}")

    status_handlers = {
        "CONFIRMED": _handle_confirmed_reservation,
        "REJECTED": _handle_rejected_reservation,
        "CANCELLED": _handle_cancelled_reservation,
    }

    handler = status_handlers.get(instance.status)
    if handler:
        handler(instance)


def _handle_confirmed_reservation(instance):
    """Handle confirmed reservation."""
    print("Réservation confirmée")
    # 1️⃣ Notification au passager
    try:
        notify_reservation_approved(
            passenger=instance.passager,
            driver=instance.trajet.conducteur,
            reservation=instance,
        )
        print("Notification CONFIRMED envoyée au passager")
    except Exception as e:
        print(f"Erreur notification CONFIRMED: {e}")
        import traceback

        traceback.print_exc()

    try:
        create_or_update_group_conversation(instance)
        print("Conversation de groupe créée/mise à jour")
    except Exception as e:
        print(f"Erreur conversation groupe: {e}")
        import traceback

        traceback.print_exc()


def _handle_rejected_reservation(instance):
    """Handle rejected reservation."""
    print("Réservation rejetée")
    try:
        notify_reservation_rejected(
            passenger=instance.passager,
            driver=instance.trajet.conducteur,
            reservation=instance,
        )
        print("Notification REJECTED envoyée au passager")
    except Exception as e:
        print(f"Erreur notification REJECTED: {e}")
        import traceback

        traceback.print_exc()


def _handle_cancelled_reservation(instance):
    print("Réservation annulée")
    try:
        notify_reservation_cancelled(
            driver=instance.trajet.conducteur,
            passenger=instance.passager,
            reservation=instance,
        )
        print("Notification CANCELLED envoyée au conducteur")
    except Exception as e:
        print(f"Erreur notification CANCELLED: {e}")
        import traceback

        traceback.print_exc()


def create_or_update_group_conversation(reservation):
    print(f"Création/MAJ conversation groupe pour trajet {reservation.trajet.id}")
    trajet = reservation.trajet
    # Récupérer ou créer la conversation de groupe
    conversation, created = Conversation.objects.get_or_create(
        trajet=trajet,
        is_group=True,
    )
    if created:
        print(f"Nouvelle conversation créée (ID: {conversation.id})")
    else:
        print(f"Conversation existante (ID: {conversation.id})")

    # Ajouter le conducteur
    if not conversation.participants.filter(id=trajet.conducteur.id).exists():
        conversation.participants.add(trajet.conducteur)
        print(f"Conducteur ajouté: {trajet.conducteur.full_name}")

    # Ajouter TOUS les passagers confirmés
    confirmed_reservations = trajet.reservations.filter(status="CONFIRMED")
    print(f"Total réservations confirmées: {confirmed_reservations.count()}")

    for res in confirmed_reservations:
        if not conversation.participants.filter(id=res.passager.id).exists():
            conversation.participants.add(res.passager)
            print(f"Passager ajouté: {res.passager.full_name}")

    conversation.save()

    if created:
        try:
            Message.objects.create(
                sender=trajet.conducteur,
                conversation=conversation,
                trajet=trajet,
                is_group_message=True,
                text=(
                    f"Bienvenue dans la conversation du trajet {trajet.ville_depart} → "
                    f"{trajet.ville_arrivee} !"
                ),
            )
            print("Message de bienvenue créé")
        except Exception as e:
            print(f"Erreur message bienvenue: {e}")

    # Message pour le nouveau passager
    try:
        Message.objects.create(
            sender=trajet.conducteur,
            conversation=conversation,
            trajet=trajet,
            is_group_message=True,
            text=f"{reservation.passager.first_name} a rejoint le trajet !",
        )
        print(f"Message d'annonce créé pour {reservation.passager.first_name}")
    except Exception as e:
        print(f"Erreur message annonce: {e}")

    total = conversation.participants.count()
    print(f"Conversation finalisée - {total} participants")

    return conversation


@receiver(post_save, sender=Reservation)
def update_places_on_reservation_create(sender, instance, created, **kwargs):
    if created and instance.status == "PENDING":
        # Réserver les places dès la création
        trajet = instance.trajet
        trajet.places_disponibles -= instance.nbr_places
        trajet.save(update_fields=["places_disponibles"])
        print(
            f"Places réservées: {instance.nbr_places} - Restantes: {trajet.places_disponibles}"
        )

    # Si le statut change vers CONFIRMED (depuis PENDING)
    elif not created and instance.status == "CONFIRMED":
        # Les places sont déjà réservées, ne rien faire
        print("Réservation confirmée - Places déjà réservées")


@receiver(pre_delete, sender=Reservation)
def restore_places_on_reservation_delete(sender, instance, **kwargs):
    if instance.status in ["PENDING", "CONFIRMED"]:
        trajet = instance.trajet
        trajet.places_disponibles += instance.nbr_places
        trajet.save(update_fields=["places_disponibles"])
        print(
            f"Places restaurées: {instance.nbr_places} - Disponibles: {trajet.places_disponibles}"
        )
