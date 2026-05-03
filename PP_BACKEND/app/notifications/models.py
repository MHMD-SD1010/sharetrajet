"""
app/notifications/models.py - Modèles CORRIGÉS
"""

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Message(models.Model):
    """Modèle pour les messages entre utilisateurs"""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        null=True,
        blank=True,
    )

    trajet = models.ForeignKey(
        "trajets.Trajet",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )

    # ⚠️ IMPORTANT: Le champ s'appelle 'text', pas 'content'
    text = models.TextField()

    media = models.FileField(
        upload_to="messages/media/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "pdf"])],
    )
    media_type = models.CharField(max_length=50, blank=True)

    is_group_message = models.BooleanField(default=False, db_index=True)

    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # ⚠️ AJOUT: Référence à la conversation (optionnel mais utile)
    conversation = models.ForeignKey(
        "Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "messagerie"
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sender", "receiver"]),
            models.Index(fields=["trajet", "created_at"]),
            models.Index(fields=["is_read", "receiver"]),
            models.Index(fields=["is_group_message", "trajet"]),
        ]

    def __str__(self):
        if self.is_group_message:
            return f"Message de {self.sender.full_name} dans groupe trajet {self.trajet_id}"
        receiver_name = self.receiver.full_name if self.receiver else "groupe"
        return f"Message de {self.sender.full_name} à {receiver_name}"

    def mark_as_read(self):
        """Marque le message comme lu"""
        if not self.is_read:
            from django.utils import timezone

            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class Conversation(models.Model):
    """Modèle pour regrouper les messages en conversations"""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )
    trajet = models.ForeignKey(
        "trajets.Trajet",
        on_delete=models.CASCADE,
        related_name="conversations",
        null=True,
        blank=True,
    )

    is_group = models.BooleanField(default=False, db_index=True)

    last_message = models.ForeignKey(
        Message, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversations"
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ["-last_activity"]
        indexes = [
            models.Index(fields=["is_group", "trajet"]),
        ]

    def __str__(self):
        if self.is_group and self.trajet:
            return f"Groupe: {self.trajet.ville_depart} → {self.trajet.ville_arrivee}"
        participants = ", ".join([u.full_name for u in self.participants.all()[:2]])
        return f"Conversation: {participants}"

    def get_unread_count(self, user):
        """Retourne le nombre de messages non lus pour un utilisateur"""
        if self.is_group:
            return (
                Message.objects.filter(
                    trajet=self.trajet, is_group_message=True, is_read=False
                )
                .exclude(sender=user)
                .count()
            )
        else:
            return Message.objects.filter(
                receiver=user, is_read=False, sender__in=self.participants.all()
            ).count()


class Notification(models.Model):
    """Modèle pour les notifications utilisateurs"""

    NOTIFICATION_TYPES = [
        ("RESERVATION_REQUEST", "Demande de réservation"),
        ("RESERVATION_APPROVED", "Réservation approuvée"),
        ("RESERVATION_REJECTED", "Réservation rejetée"),
        ("RESERVATION_CANCELLED", "Réservation annulée"),
        ("MESSAGE_RECEIVED", "Message reçu"),
        ("TRAJET_CANCELLED", "Trajet annulé"),
        ("TRAJET_MODIFIED", "Trajet modifié"),
        ("RATING_RECEIVED", "Évaluation reçue"),
        ("DOCUMENT_VERIFIED", "Document vérifié"),
        ("DOCUMENT_REJECTED", "Document rejeté"),
        ("WELCOME", "Bienvenue"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
        null=True,
        blank=True,
    )

    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    content = models.TextField()

    related_model = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    related_id = models.IntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["related_model", "related_id"]),
        ]

    def __str__(self):
        return f"Notification pour {self.recipient.full_name}: {self.type}"

    def mark_as_read(self):
        """Marque la notification comme lue"""
        if not self.is_read:
            from django.utils import timezone

            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def get_related_object(self):
        """Récupère l'objet lié à la notification"""
        if not self.related_model or not self.related_id:
            return None

        try:
            from django.apps import apps

            model_class = apps.get_model(
                app_label=(
                    "reservations" if "Reservation" in self.related_model else "trajets"
                ),
                model_name=self.related_model,
            )
            return model_class.objects.get(pk=self.related_id)
        except Exception:
            return None
