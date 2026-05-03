"""
app/trajets/serializers.py - Serializers corrigés
"""

from decimal import Decimal

from rest_framework import serializers

from app.users.models import Preference, UserDocument
from app.users.serializers import PreferenceSerializer, UserSerializer
from utils.pricing import calculate_suggested_price, extract_wilaya_from_location

from .models import FuelPrice, Trajet, TrajetEtape


class TrajetEtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrajetEtape
        fields = ["id", "ville", "adresse", "heure_arrivee", "ordre"]
        read_only_fields = ["id"]


class TrajetCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'un trajet"""

    etapes = TrajetEtapeSerializer(many=True, required=False, write_only=True)
    preference_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Trajet
        fields = [
            "ville_depart",
            "ville_arrivee",
            "adresse_depart",
            "adresse_arrivee",
            "date",
            "heure_depart",
            "nbr_places",
            "price",
            "distance",
            "is_confort",
            "fuel_type",
            "fuel_consumption",
            "description",
            "luggage_allowed",
            "etapes",
            "preference_ids",
        ]
        read_only_fields = []

    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("Utilisateur connecté requis")

        has_verified_doc = UserDocument.objects.filter(
            user=request.user, verified=True
        ).exists()
        if not has_verified_doc:
            raise serializers.ValidationError("CNI vérifié requis")
        return attrs

    def validate_date(self, value):
        from django.utils import timezone

        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La date du trajet ne peut pas être dans le passé."
            )
        return value

    def validate_nbr_places(self, value):
        if value < 1 or value > 8:
            raise serializers.ValidationError(
                "Le nombre de places doit être entre 1 et 8."
            )
        return value

    def validate_distance(self, value):
        if value <= 0:
            raise serializers.ValidationError("La distance doit être positive.")
        return value

    def create(self, validated_data):
        etapes_data = validated_data.pop("etapes", [])
        preference_ids = validated_data.pop("preference_ids", [])

        request = self.context.get("request")
        conducteur = request.user

        # Extraire la wilaya
        validated_data["wilaya_depart"] = (
            extract_wilaya_from_location(validated_data["ville_depart"]) or "Alger"
        )

        # Calculer le prix conseillé
        suggested_price_data = calculate_suggested_price(
            distance=float(validated_data["distance"]),
            ville_depart=validated_data["ville_depart"],
            fuel_type=validated_data.get("fuel_type", "gasoil"),
            fuel_consumption=float(validated_data.get("fuel_consumption", 8.0)),
            nbr_places=validated_data["nbr_places"],
        )

        if isinstance(suggested_price_data, dict):
            suggested_price = suggested_price_data.get(
                "suggested_price_per_seat", Decimal("0")
            )
        else:
            suggested_price = Decimal(suggested_price_data)

        validated_data["suggested_price"] = suggested_price

        # Créer le trajet
        trajet = Trajet.objects.create(conducteur=conducteur, **validated_data)

        # Associer les préférences
        if preference_ids:
            preferences = Preference.objects.filter(id__in=preference_ids)
            trajet.preferences.set(preferences)

        # Créer les étapes
        for ordre, etape_data in enumerate(etapes_data, start=1):
            TrajetEtape.objects.create(trajet=trajet, ordre=ordre, **etape_data)

        return trajet


class TrajetListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des trajets"""

    conducteur_name = serializers.CharField(
        source="conducteur.full_name", read_only=True
    )
    conducteur_rating = serializers.DecimalField(
        source="conducteur.average_rating",
        max_digits=3,
        decimal_places=2,
        read_only=True,
    )
    conducteur_picture = serializers.ImageField(
        source="conducteur.profile_picture", read_only=True
    )

    class Meta:
        model = Trajet
        fields = [
            "id",
            "conducteur",
            "conducteur_name",
            "conducteur_rating",
            "conducteur_picture",
            "ville_depart",
            "ville_arrivee",
            "date",
            "heure_depart",
            "nbr_places",
            "places_disponibles",
            "price",
            "distance",
            "is_confort",
            "pause_required",
            "fuel_type",
            "status",
            "created_at",
            "luggage_allowed",  # ✅ Remplace small_luggage_only
        ]
        read_only_fields = ["id", "conducteur", "created_at", "places_disponibles"]


class TrajetDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour un trajet"""

    conducteur = UserSerializer(read_only=True)
    etapes = TrajetEtapeSerializer(many=True, read_only=True)

    # ✅ AJOUT : Préférences du trajet
    preferences = PreferenceSerializer(many=True, read_only=True)

    # ✅ AJOUT : Liste des passagers ayant réservé
    passagers_reserves = serializers.SerializerMethodField()

    total_reservations = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = [
            "id",
            "conducteur",
            "ville_depart",
            "ville_arrivee",
            "adresse_depart",
            "adresse_arrivee",
            "wilaya_depart",
            "date",
            "heure_depart",
            "nbr_places",
            "places_disponibles",
            "price",
            "price_platform",
            "price_driver",
            "suggested_price",
            "distance",
            "is_confort",
            "pause_required",
            "fuel_type",
            "fuel_consumption",
            "status",
            "description",
            "luggage_allowed",
            "preferences",  # ✅ AJOUT
            "passagers_reserves",  # ✅ AJOUT
            "etapes",
            "total_reservations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "conducteur",
            "price_platform",
            "price_driver",
            "places_disponibles",
            "pause_required",
            "wilaya_depart",
            "created_at",
            "updated_at",
        ]

    def get_total_reservations(self, obj):
        """Retourne le nombre total de réservations confirmées"""
        return obj.reservations.filter(status="CONFIRMED").count()

    def get_passagers_reserves(self, obj):
        """Retourne la liste des passagers ayant une réservation confirmée"""
        from app.reservations.models import Reservation

        reservations = Reservation.objects.filter(
            trajet=obj, status="CONFIRMED"
        ).select_related("passager")

        passagers_data = []
        for reservation in reservations:
            passager = reservation.passager
            passagers_data.append(
                {
                    "id": passager.id,
                    "nom": passager.last_name,
                    "prenom": passager.first_name,
                    "profile_picture": (
                        self.context.get("request").build_absolute_uri(
                            passager.profile_picture.url
                        )
                        if passager.profile_picture
                        else None
                    ),
                    "nbr_places": reservation.nbr_places,
                }
            )

        return passagers_data


class TrajetUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour d'un trajet"""

    class Meta:
        model = Trajet
        fields = [
            "adresse_depart",
            "adresse_arrivee",
            "date",
            "heure_depart",
            "nbr_places",
            "price",
            "is_confort",
            "fuel_type",
            "fuel_consumption",
            "description",
            "luggage_allowed",
            "status",
        ]

    def validate_status(self, value):
        """Valide le changement de statut"""
        if self.instance and self.instance.status == "COMPLETED":
            raise serializers.ValidationError(
                "Un trajet terminé ne peut pas être modifié."
            )
        return value

    def validate_nbr_places(self, value):
        """Valide que le nouveau nombre de places n'est pas inférieur aux réservations"""
        if self.instance:
            reserved = self.instance.nbr_places - self.instance.places_disponibles
            if value < reserved:
                raise serializers.ValidationError(
                    f"Impossible de réduire à {value} places. "
                    f"{reserved} places sont déjà réservées."
                )
        return value


class TrajetSearchSerializer(serializers.Serializer):
    """
    Serializer pour la recherche intelligente de trajets
    """

    ville_depart = serializers.CharField(required=True)
    ville_arrivee = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    nbr_places = serializers.IntegerField(required=False, default=1, min_value=1)

    # Filtres optionnels
    price_max = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )
    is_confort = serializers.BooleanField(required=False)
    fuel_type = serializers.ChoiceField(
        choices=["essence_sans_plomb", "gasoil", "gpl", "electrique"],
        required=False,
    )

    # Filtre par période de la journée
    departure_time = serializers.ChoiceField(
        choices=["morning", "afternoon", "evening"], required=False
    )

    # Filtre par préférences
    preference_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )


class FuelPriceSerializer(serializers.ModelSerializer):
    """Serializer pour les prix du carburant"""

    class Meta:
        model = FuelPrice
        fields = [
            "id",
            "wilaya_code",
            "wilaya_name",
            "fuel_type",
            "price_per_liter",
            "effective_date",
        ]
        read_only_fields = ["id", "effective_date"]
