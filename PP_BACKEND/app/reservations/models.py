"""
Modèles pour la gestion des réservations du projet DZ-CarPool
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Reservation(models.Model):
    """Modèle pour les réservations de trajets"""

    STATUS_CHOICES = [
        ("PENDING", "En attente"),
        ("CONFIRMED", "Confirmée"),
        ("REJECTED", "Refusée"),
        ("CANCELLED", "Annulée"),
    ]

    trajet = models.ForeignKey(
        "trajets.Trajet", on_delete=models.CASCADE, related_name="reservations"
    )
    passager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations_as_passenger",
    )

    nbr_places = models.IntegerField(
        validators=[MinValueValidator(1)], help_text="Nombre de places réservées"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING", db_index=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)

    # Prix au moment de la réservation
    price_per_seat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Prix par siège au moment de la réservation",
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Prix total de la réservation"
    )

    class Meta:
        db_table = "reservations"
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["trajet", "status"]),
            models.Index(fields=["passager", "status"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["trajet", "passager"],
                condition=models.Q(status__in=["PENDING", "CONFIRMED"]),
                name="unique_active_reservation_per_user",
            )
        ]

    def __str__(self):
        return f"Réservation #{self.id} - {self.passager.email} pour {self.trajet}"

    def save(self, *args, **kwargs):
        """Override save pour calculer le prix total"""
        if not self.price_per_seat:
            self.price_per_seat = self.trajet.price

        self.total_price = self.price_per_seat * self.nbr_places
        super().save(*args, **kwargs)

    def approve(self):
        """Approuve la réservation"""
        if self.status != "PENDING":
            raise ValueError(
                "Seules les réservations en attente peuvent être approuvées"
            )

        if not self.trajet.can_reserve(self.nbr_places):
            raise ValueError("Pas assez de places disponibles")

        self.status = "CONFIRMED"
        self.approved_at = timezone.now()
        self.save()

        # Mettre à jour la disponibilité du trajet
        self.trajet.update_disponibilite()

        # Créer une notification pour le passager
        from app.notifications.models import Notification

        Notification.objects.create(
            recipient=self.passager,
            sender=self.trajet.conducteur,
            type="RESERVATION_APPROVED",
            content=f"Votre réservation pour le trajet {self.trajet} a été approuvée",
            related_model="Reservation",
            related_id=self.id,
        )

    def reject(self, reason=""):
        """Rejette la réservation"""
        if self.status != "PENDING":
            raise ValueError("Seules les réservations en attente peuvent être rejetées")

        self.status = "REJECTED"
        self.rejection_reason = reason
        self.save()

        # Créer une notification pour le passager
        from app.notifications.models import Notification

        Notification.objects.create(
            recipient=self.passager,
            sender=self.trajet.conducteur,
            type="RESERVATION_REJECTED",
            content=f"Votre réservation pour le trajet {self.trajet} a été refusée",
            related_model="Reservation",
            related_id=self.id,
        )

    def cancel(self, reason=""):
        """Annule la réservation"""
        if self.status not in ["PENDING", "CONFIRMED"]:
            raise ValueError(
                "Seules les réservations en attente ou confirmées peuvent être annulées"
            )

        old_status = self.status
        self.status = "CANCELLED"
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save()

        # Si la réservation était confirmée, libérer les places
        if old_status == "CONFIRMED":
            self.trajet.update_disponibilite()

        # Notification au conducteur
        from app.notifications.models import Notification

        Notification.objects.create(
            recipient=self.trajet.conducteur,
            sender=self.passager,
            type="RESERVATION_CANCELLED",
            content=f"La réservation de {self.passager.full_name} a été annulée",
            related_model="Reservation",
            related_id=self.id,
        )


class Rating(models.Model):
    """Modèle pour les évaluations mutuelles après un trajet"""

    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name="rating"
    )

    # Qui note qui
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        help_text="Utilisateur qui donne la note",
    )
    rated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_ratings",
        help_text="Utilisateur qui reçoit la note",
    )

    # Note et commentaire
    note = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de 1 à 5 étoiles",
    )
    comment = models.TextField(blank=True)

    # Critères détaillés (optionnel)
    ponctualite = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    convivialite = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    conduite = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Pour les conducteurs uniquement",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ratings"
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["rated", "note"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["reservation", "rater"], name="unique_rating_per_user"
            )
        ]

    def __str__(self):
        return f"{self.rater.full_name} → {self.rated.full_name}: {self.note}/5"

    def save(self, *args, **kwargs):
        """Override save pour mettre à jour les statistiques de l'utilisateur noté"""
        super().save(*args, **kwargs)
        # Mettre à jour la moyenne de l'utilisateur noté
        self.rated.update_statistics()
