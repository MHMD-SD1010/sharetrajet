from rest_framework import serializers

from app.trajets.serializers import TrajetListSerializer
from app.users.serializers import UserSerializer

from .models import Rating, Reservation


class RatingSerializer(serializers.ModelSerializer):
    """Serializer pour les évaluations"""

    rater_detail = UserSerializer(source="rater", read_only=True)
    rated_detail = UserSerializer(source="rated", read_only=True)

    class Meta:
        model = Rating
        fields = [
            "id",
            "reservation",
            "rater",
            "rater_detail",
            "rated",
            "rated_detail",
            "note",
            "comment",
            "ponctualite",
            "convivialite",
            "conduite",
            "created_at",
        ]
        read_only_fields = ["id", "rater", "rated", "created_at"]


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer CORRIGÉ pour afficher correctement can_rate et has_rating
    """

    passager_detail = UserSerializer(source="passager", read_only=True)
    trajet_detail = TrajetListSerializer(source="trajet", read_only=True)

    # Ces champs DOIVENT être SerializerMethodField pour être calculés dynamiquement
    can_rate = serializers.SerializerMethodField()
    has_rating = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "id",
            "trajet",
            "trajet_detail",
            "passager",
            "passager_detail",
            "nbr_places",
            "status",
            "price_per_seat",
            "total_price",
            "created_at",
            "approved_at",
            "cancelled_at",
            "rejection_reason",
            "cancellation_reason",
            "can_rate",
            "has_rating",
            "rating",
        ]
        read_only_fields = [
            "id",
            "passager",
            "created_at",
            "approved_at",
            "cancelled_at",
            "price_per_seat",
            "total_price",
        ]

    def get_rating(self, obj):
        """
        Retourne le rating avec le bon format pour le frontend
        """
        try:
            if not hasattr(obj, "rating"):
                return None

            rating = obj.rating
            return {
                "id": rating.id,
                "note": rating.note,
                "ponctualite": rating.ponctualite,
                "convivialite": rating.convivialite,
                "conduite": rating.conduite,
                "comment": rating.comment or "",
                "created_at": (
                    rating.created_at.isoformat() if rating.created_at else None
                ),
            }
        except Exception as e:
            print(f"Erreur get_rating: {str(e)}")
            return None

    def get_can_rate(self, obj):
        """
        CORRECTION CRITIQUE: Vérifie si l'utilisateur PEUT noter

        Conditions:
        1. Réservation CONFIRMÉE
        2. PAS de rating existant
        3. Utilisateur authentifié
        """
        try:
            request = self.context.get("request")

            # Debug
            print(f"CAN_RATE CHECK - Booking #{obj.id}:")
            print(f"Status: {obj.status}")
            print(f"Has rating: {hasattr(obj, 'rating')}")
            print(f"Request user: {request.user if request else 'None'}")
            print(f"Passager: {obj.passager}")

            # Pas de request ou user non authentifié
            if (
                not request
                or not hasattr(request, "user")
                or not request.user.is_authenticated
            ):
                print("Pas d'utilisateur authentifié")
                return False

            # Pas le passager
            if request.user != obj.passager:
                print("Pas le passager")
                return False

            # Pas confirmée
            if obj.status != "CONFIRMED":
                print(f"Status pas CONFIRMED: {obj.status}")
                return False

            # Déjà noté
            if hasattr(obj, "rating"):
                print("Déjà noté")
                return False

            # Toutes les conditions OK
            print("PEUT NOTER!")
            return True

        except Exception as e:
            print(f"Erreur get_can_rate: {str(e)}")
            import traceback

            traceback.print_exc()
            return False

    def get_has_rating(self, obj):
        """Vérifie si la réservation a déjà un rating"""
        try:
            has_rating = hasattr(obj, "rating")
            print(f"HAS_RATING - Booking #{obj.id}: {has_rating}")
            return has_rating
        except Exception as e:
            print(f"Erreur get_has_rating: {str(e)}")
            return False


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'une réservation"""

    class Meta:
        model = Reservation
        fields = ["trajet", "nbr_places"]

    def validate(self, attrs):
        """Valide la réservation"""
        trajet = attrs["trajet"]
        nbr_places = attrs["nbr_places"]
        request = self.context.get("request")

        if trajet.conducteur == request.user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas réserver votre propre trajet"
            )

        if not trajet.can_reserve(nbr_places):
            raise serializers.ValidationError(
                f"Seulement {trajet.places_disponibles} places disponibles"
            )

        existing = Reservation.objects.filter(
            trajet=trajet, passager=request.user, status__in=["PENDING", "CONFIRMED"]
        ).exists()

        if existing:
            raise serializers.ValidationError(
                "Vous avez déjà une réservation active pour ce trajet"
            )

        return attrs

    def create(self, validated_data):
        """Crée une nouvelle réservation"""
        request = self.context.get("request")

        reservation = Reservation.objects.create(
            passager=request.user, **validated_data
        )

        # Créer une notification pour le conducteur
        try:
            from app.notifications.models import Notification

            Notification.objects.create(
                recipient=reservation.trajet.conducteur,
                sender=request.user,
                type="RESERVATION_REQUEST",
                content=(
                    f"{request.user.first_name} {request.user.last_name} demande à réserver "
                    f"{validated_data['nbr_places']} place(s)"
                ),
                related_model="Reservation",
                related_id=reservation.id,
            )
        except Exception as e:
            print(f"Erreur création notification: {str(e)}")

        return reservation


class RatingCreateSerializer(serializers.Serializer):
    """Serializer simplifié pour la création de ratings"""

    note = serializers.IntegerField(min_value=1, max_value=5)
    ponctualite = serializers.IntegerField(
        min_value=1, max_value=5, required=False, allow_null=True
    )
    convivialite = serializers.IntegerField(
        min_value=1, max_value=5, required=False, allow_null=True
    )
    conduite = serializers.IntegerField(
        min_value=1, max_value=5, required=False, allow_null=True
    )
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
