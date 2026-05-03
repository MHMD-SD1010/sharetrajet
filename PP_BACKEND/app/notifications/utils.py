"""
app/notifications/utils.py - Utilitaires de notifications CORRIGÉS
"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification
from .serializers import NotificationSerializer


def create_notification(
    recipient,
    notification_type,
    content,
    sender=None,
    related_model=None,
    related_id=None,
):
    """
    Crée une notification ET l'envoie via WebSocket
    """
    print("=" * 80)
    print("CREATE_NOTIFICATION appelée")
    print(f"   Recipient: {recipient.full_name}")
    print(f"   Type: {notification_type}")
    print(f"   Content: {content}")
    print("=" * 80)

    try:
        notification = Notification.objects.create(
            recipient=recipient,
            type=notification_type,
            content=content,
            sender=sender,
            related_model=related_model,
            related_id=related_id,
        )

        print(f"✅ Notification créée en DB: ID={notification.id}")

        # ENVOI WEBSOCKET avec le BON nom de groupe
        try:
            channel_layer = get_channel_layer()

            # ⚠️ FIX CRITIQUE: Utiliser "notifications_" au lieu de "user_"
            group_name = f"notifications_{recipient.id}"

            print(f"📡 Envoi WebSocket au groupe: {group_name}")

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "notification_message",  # ⚠️ Correspond au handler du consumer
                    "notification": NotificationSerializer(notification).data,
                },
            )

            print("WebSocket envoyé avec succès")

        except Exception as ws_error:
            print(f"❌ Erreur WebSocket (notification quand même créée): {ws_error}")
            import traceback

            traceback.print_exc()

        return notification

    except Exception as e:
        print(f"❌ ERREUR CRITIQUE create_notification: {e}")
        import traceback

        traceback.print_exc()
        return None


def notify_new_message(sender, recipient, message):
    """
    Notification pour un nouveau message
    """
    content = f"{sender.full_name} vous a envoyé un message"

    print(f"📨 notify_new_message: {sender.full_name} → {recipient.full_name}")

    return create_notification(
        recipient=recipient,
        notification_type="MESSAGE_RECEIVED",
        content=content,
        sender=sender,
        related_model="Message",
        related_id=message.id,
    )


def notify_reservation_request(driver, passenger, reservation):
    """
    Notification pour une nouvelle demande de réservation
    """
    print("notify_reservation_request")

    content = f"{passenger.full_name} souhaite réserver votre trajet"

    return create_notification(
        recipient=driver,
        notification_type="RESERVATION_REQUEST",
        content=content,
        sender=passenger,
        related_model="Reservation",
        related_id=reservation.id,
    )


def notify_reservation_approved(passenger, driver, reservation):
    """
    Notification pour une réservation approuvée
    """
    print("notify_reservation_approved")

    content = f"{driver.full_name} a accepté votre réservation"

    return create_notification(
        recipient=passenger,
        notification_type="RESERVATION_APPROVED",
        content=content,
        sender=driver,
        related_model="Reservation",
        related_id=reservation.id,
    )


def notify_reservation_rejected(passenger, driver, reservation):
    """
    Notification pour une réservation rejetée
    """
    print("notify_reservation_rejected")

    content = f"{driver.full_name} a refusé votre réservation"

    return create_notification(
        recipient=passenger,
        notification_type="RESERVATION_REJECTED",
        content=content,
        sender=driver,
        related_model="Reservation",
        related_id=reservation.id,
    )


def notify_reservation_cancelled(driver, passenger, reservation):
    """
    Notification pour une réservation annulée par le passager
    """
    print("notify_reservation_cancelled")

    content = f"{passenger.full_name} a annulé sa réservation"

    return create_notification(
        recipient=driver,
        notification_type="RESERVATION_CANCELLED",
        content=content,
        sender=passenger,
        related_model="Reservation",
        related_id=reservation.id,
    )


def notify_welcome(user):
    """
    Notification de bienvenue
    """
    content = f"Bienvenue sur DZ-CarPool, {user.full_name}! 🎉"

    return create_notification(
        recipient=user,
        notification_type="WELCOME",
        content=content,
    )
