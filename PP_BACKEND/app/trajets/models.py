from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Trajet(models.Model):
    """Modèle pour les trajets de covoiturage"""

    STATUS_CHOICES = [
        ("ACTIVE", "Actif"),
        ("COMPLETED", "Terminé"),
        ("CANCELLED", "Annulé"),
    ]

    FUEL_TYPE_CHOICES = [
        ("essence_sans_plomb", "Essence Sans Plomb"),
        ("gasoil", "Gasoil"),
        ("gpl", "GPL"),
        ("electrique", "Électrique"),
    ]

    conducteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trajets_as_driver",
    )

    # Informations de trajet
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    adresse_depart = models.TextField(blank=True)
    adresse_arrivee = models.TextField(blank=True)

    date = models.DateField(db_index=True)
    heure_depart = models.TimeField()

    # Capacité et disponibilité
    nbr_places = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Nombre total de places disponibles",
    )
    places_disponibles = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Nombre de places encore disponibles",
    )

    # Tarification
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Prix par siège fixé par le conducteur",
    )
    price_platform = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Commission de la plateforme (15%)",
    )
    price_driver = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Montant net reversé au conducteur",
    )
    suggested_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prix conseillé basé sur le coût du carburant (cahier des charges)",
    )

    # Distance et options
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Distance du trajet en km",
    )
    is_confort = models.BooleanField(
        default=False, help_text="Option Trajet Confort (+30%)"
    )
    pause_required = models.BooleanField(
        default=False, help_text="Pause obligatoire pour trajets > 300km"
    )

    # Informations véhicule et carburant
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        default="gasoil",
        help_text="Type de carburant utilisé par le véhicule",
    )
    fuel_consumption = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("8.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Consommation du véhicule (L/100km ou kWh/100km pour électrique)",
    )

    wilaya_depart = models.CharField(
        max_length=100,
        blank=True,
        help_text="Wilaya de départ extraite automatiquement de l'adresse",
    )

    # ✅ CORRECTION : Relation many-to-many avec through
    preferences = models.ManyToManyField(
        "users.Preference",
        blank=True,
        related_name="trajets",
        through="TrajetPreference",  # ✅ Ajoutez cette ligne
        help_text="Préférences du conducteur pour ce trajet",
    )

    # Statut et métadonnées
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Informations additionnelles
    description = models.TextField(blank=True)
    luggage_allowed = models.BooleanField(default=True)

    class Meta:
        db_table = "trajets"
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ["-date", "-heure_depart"]
        indexes = [
            models.Index(fields=["ville_depart", "ville_arrivee", "date"]),
            models.Index(fields=["conducteur", "status"]),
            models.Index(fields=["date", "status"]),
            models.Index(fields=["fuel_type"]),
            models.Index(fields=["wilaya_depart"]),
        ]

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} - {self.date}"

    def save(self, *args, **kwargs):
        """Override save pour calculer automatiquement les prix et la pause"""
        commission = self.price * Decimal(str(settings.PLATFORM_COMMISSION_RATE))
        self.price_platform = commission
        self.price_driver = self.price - commission

        if self.is_confort:
            supplement = self.price * Decimal(str(settings.CONFORT_SUPPLEMENT_RATE))
            self.price = self.price + supplement
            self.price_platform = self.price * Decimal(
                str(settings.PLATFORM_COMMISSION_RATE)
            )
            self.price_driver = self.price - self.price_platform

        if self.distance > settings.LONG_DISTANCE_THRESHOLD_KM:
            self.pause_required = True

        if not self.pk:
            self.places_disponibles = self.nbr_places

        super().save(*args, **kwargs)

    def get_total_price_for_passenger(self, nb_places=1):
        """Calcule le prix total pour un passager avec commission"""
        base_price = self.price * nb_places
        commission = base_price * Decimal(str(settings.PLATFORM_COMMISSION_RATE))
        return base_price + commission

    def can_reserve(self, nb_places):
        """Vérifie si le nombre de places demandé est disponible"""
        return (
            self.status == "ACTIVE"
            and self.places_disponibles >= nb_places
            and nb_places > 0
        )

    def update_disponibilite(self):
        """Met à jour le nombre de places disponibles"""
        from app.reservations.models import Reservation

        reserved = (
            Reservation.objects.filter(trajet=self, status="CONFIRMED").aggregate(
                total=models.Sum("nbr_places")
            )["total"]
            or 0
        )

        self.places_disponibles = self.nbr_places - reserved
        self.save()


# ✅ AJOUT : Modèle intermédiaire TrajetPreference
class TrajetPreference(models.Model):
    """Table de liaison entre Trajet et Preference"""

    trajet = models.ForeignKey(
        "Trajet", on_delete=models.CASCADE, related_name="trajet_preferences"
    )
    preference = models.ForeignKey(
        "users.Preference", on_delete=models.CASCADE, related_name="preference_trajets"
    )

    class Meta:
        db_table = "trajets_preferences"
        unique_together = [("trajet", "preference")]
        indexes = [
            models.Index(fields=["trajet"]),
            models.Index(fields=["preference"]),
        ]

    def __str__(self):
        return f"{self.trajet} - {self.preference}"


class TrajetEtape(models.Model):
    """Modèle pour les étapes d'un trajet"""

    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="etapes")
    ville = models.CharField(max_length=100)
    adresse = models.TextField(blank=True)
    heure_arrivee = models.TimeField()
    ordre = models.IntegerField(
        validators=[MinValueValidator(1)], help_text="Ordre de l'étape dans le trajet"
    )

    class Meta:
        db_table = "trajet_etapes"
        verbose_name = "Étape de Trajet"
        verbose_name_plural = "Étapes de Trajet"
        ordering = ["ordre"]
        unique_together = ["trajet", "ordre"]

    def __str__(self):
        return f"{self.trajet} - Étape {self.ordre}: {self.ville}"


class FuelPrice(models.Model):
    """
    Modèle pour stocker les prix du carburant par wilaya
    Synchronisé avec prix_carburants.json (cahier des charges)
    """

    FUEL_TYPES = [
        ("essence_sans_plomb", "Essence Sans Plomb"),
        ("gasoil", "Gasoil"),
        ("gpl", "GPL"),
        ("electrique", "Électrique"),
    ]

    wilaya_code = models.CharField(max_length=2, db_index=True, default="")
    wilaya_name = models.CharField(max_length=100, default="")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    price_per_liter = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    effective_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "fuel_prices"
        verbose_name = "Prix Carburant"
        verbose_name_plural = "Prix Carburants"
        unique_together = ["wilaya_code", "fuel_type", "effective_date"]
        ordering = ["-effective_date", "wilaya_name"]
        indexes = [
            models.Index(fields=["wilaya_name", "fuel_type"]),
        ]

    def __str__(self):
        return f"{self.wilaya_name} - {self.get_fuel_type_display()}: {self.price_per_liter} DA/L"
