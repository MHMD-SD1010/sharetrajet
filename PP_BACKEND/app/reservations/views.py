"""
app/reservations/views.py - ViewSet pour les réservations avec vérification des documents
"""

import logging

from django.apps import AppConfig
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.trajets.models import Trajet
from app.users.models import UserDocument

from .models import Rating, Reservation
from .serializers import RatingSerializer, ReservationSerializer

logger = logging.getLogger(__name__)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des réservations avec vérification des documents
    """

    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retourne les réservations de l'utilisateur connecté"""
        user = self.request.user
        return (
            Reservation.objects.filter(Q(passager=user) | Q(trajet__conducteur=user))
            .select_related("trajet", "passager", "trajet__conducteur")
            .order_by("-created_at")
        )

    def create(self, request):
        user = request.user
        # Vérification 1: Document vérifié
        if not self._has_verified_document(user):
            return self._response_document_required()
        # Vérification 2: Validation des données
        serializer = self.get_serializer(data=request.data)
        validation_error = self._validate_serializer(serializer)
        if validation_error:
            return validation_error
        # Vérification 3: Pas de réservation existante
        trajet_id = request.data.get("trajet")
        existing_error = self._check_existing_reservation(user, trajet_id)
        if existing_error:
            return existing_error
        # Vérification 4: Places disponibles
        availability_error = self._check_availability(trajet_id, request.data)
        if availability_error:
            return availability_error
        # Création
        return self._create_reservation(serializer, user, trajet_id)

    # ========== MÉTHODES PRIVÉES ==========

    def _has_verified_document(self, user):
        return UserDocument.objects.filter(user=user, verified=True).exists()

    def _response_document_required(self):
        logger.warning("Tentative de réservation sans document vérifié")
        return Response(
            {
                "error": "Document non vérifié",
                "message": "Vous devez avoir une CNI vérifiée pour réserver.",
                "can_book": False,
                "action_required": "upload_document",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    def _validate_serializer(self, serializer):
        try:
            serializer.is_valid(raise_exception=True)
            return None
        except Exception as e:
            logger.error(f"Erreur validation: {str(e)}")
            return Response(
                {
                    "error": "Données invalides",
                    "message": str(e),
                    "details": getattr(serializer, "errors", {}),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _check_existing_reservation(self, user, trajet_id):
        existing = Reservation.objects.filter(
            trajet_id=trajet_id, passager=user, status__in=["PENDING", "CONFIRMED"]
        ).first()

        if existing:
            logger.warning(f"Réservation existante: {existing.id}")
            return Response(
                {
                    "error": "Réservation déjà existante",
                    "message": (
                        f"Vous avez déjà une réservation "
                        f"{existing.get_status_display().lower()}."
                    ),
                    "existing_reservation_id": existing.id,
                    "status": existing.status,
                },
                status=status.HTTP_409_CONFLICT,
            )
        return None

    def _check_availability(self, trajet_id, data):
        try:
            trajet = Trajet.objects.get(id=trajet_id)
            nbr_places = data.get("nbr_places", 1)
            if trajet.places_disponibles < nbr_places:
                return Response(
                    {
                        "error": "Places insuffisantes",
                        "message": f"Seulement {trajet.places_disponibles} place(s) disponible(s).",
                        "available_seats": trajet.places_disponibles,
                        "requested_seats": nbr_places,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Trajet.DoesNotExist:
            return Response(
                {
                    "error": "Trajet introuvable",
                    "message": "Le trajet demandé n'existe pas.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return None

    def _create_reservation(self, serializer, user, trajet_id):
        try:
            self.perform_create(serializer)
            logger.info(f"Réservation créée: {user.email} - Trajet {trajet_id}")
            return Response(
                {
                    "success": True,
                    "message": "Réservation créée avec succès",
                    "reservation": serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data),
            )

        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            return Response(
                {
                    "error": "Conflit de réservation",
                    "message": "Une réservation existe déjà. Actualisez la page.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            return Response(
                {
                    "error": "Erreur serveur",
                    "message": "Erreur lors de la création.",
                    "details": str(e) if settings.DEBUG else "Contactez le support",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_create(self, serializer):
        serializer.save(passager=self.request.user)

    @action(detail=False, methods=["get"], url_path="check-booking-permission")
    def check_booking_permission(self, request):
        user = request.user
        has_verified_document = UserDocument.objects.filter(
            user=user, verified=True
        ).exists()
        pending_documents = UserDocument.objects.filter(
            user=user, verified=False
        ).count()
        total_documents = UserDocument.objects.filter(user=user).count()
        logger.info(
            f"Check booking permission for {user.email}: can_book={has_verified_document}"
        )
        return Response(
            {
                "can_book": has_verified_document,
                "is_verified": has_verified_document,
                "pending_documents": pending_documents,
                "total_documents": total_documents,
                "message": (
                    "Vous pouvez effectuer des réservations"
                    if has_verified_document
                    else (
                        "Vous devez télécharger et faire vérifier votre CNI "
                        "pour réserver un trajet"
                    )
                ),
            }
        )

    @action(detail=False, methods=["get"], url_path="my-bookings")
    def my_bookings(self, request):
        bookings = (
            Reservation.objects.filter(passager=request.user)
            .select_related("trajet", "trajet__conducteur")
            .order_by("-created_at")
        )

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="my-trips-bookings")
    def my_trips_bookings(self, request):
        bookings = (
            Reservation.objects.filter(trajet__conducteur=request.user)
            .select_related("trajet", "passager")
            .order_by("-created_at")
        )

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        """Confirme une réservation (conducteur uniquement)"""
        reservation = self.get_object()

        print("=" * 80)
        print(f"CONFIRM appelé pour réservation #{pk}")
        print(f"Status AVANT: {reservation.status}")
        print(f"Conducteur: {reservation.trajet.conducteur.full_name}")
        print(f"User: {request.user.full_name}")
        print("=" * 80)

        # Vérifier que c'est bien le conducteur
        if reservation.trajet.conducteur != request.user:
            return Response(
                {"error": "Seul le conducteur peut confirmer une réservation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if reservation.status != "PENDING":
            return Response(
                {"error": "Cette réservation ne peut pas être confirmée"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CRITIQUE: Changer le status et sauvegarder SANS update_fields
        reservation.status = "CONFIRMED"
        reservation.save()  # Sans update_fields pour déclencher le signal

        print(f"🔵 APRÈS SAVE - Status: {reservation.status}")
        print("=" * 80)

        logger.info(f"Réservation {pk} confirmée par {request.user.email}")

        return Response(
            {
                "message": "Réservation confirmée avec succès",
                "reservation": self.get_serializer(reservation).data,
            }
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Rejette une réservation (conducteur uniquement)"""
        reservation = self.get_object()

        if reservation.trajet.conducteur != request.user:
            return Response(
                {"error": "Seul le conducteur peut rejeter une réservation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if reservation.status != "PENDING":
            return Response(
                {"error": "Cette réservation ne peut pas être rejetée"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Libérer les places AVANT de changer le status
        trajet = reservation.trajet
        trajet.places_disponibles += reservation.nbr_places
        trajet.save(update_fields=["places_disponibles"])

        # Changer status
        reservation.status = "REJECTED"
        reservation.save(update_fields=["status"])

        logger.info(
            f"Réservation {pk} rejetée - {reservation.nbr_places} places libérées"
        )

        return Response(
            {
                "message": "Réservation rejetée",
                "reservation": self.get_serializer(reservation).data,
            }
        )

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Annule une réservation (passager uniquement)"""
        reservation = self.get_object()

        if reservation.passager != request.user:
            return Response(
                {"error": "Seul le passager peut annuler sa réservation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if reservation.status not in ["PENDING", "CONFIRMED"]:
            return Response(
                {"error": "Cette réservation ne peut pas être annulée"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Libérer les places (peu importe le status)
        trajet = reservation.trajet
        trajet.places_disponibles += reservation.nbr_places
        trajet.save(update_fields=["places_disponibles"])

        # Changer status
        reservation.status = "CANCELLED"
        reservation.save(update_fields=["status"])

        logger.info(
            f"Réservation {pk} annulée - {reservation.nbr_places} places libérées"
        )

        return Response(
            {
                "message": "Réservation annulée avec succès",
                "reservation": self.get_serializer(reservation).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="rate")
    def rate(self, request, pk=None):
        """Note un conducteur après une réservation."""
        try:
            reservation = self.get_object()
            user = request.user

            # Validation des permissions et état
            validation_error = self._validate_rating_permissions(reservation, user)
            if validation_error:
                return validation_error

            # Validation des données
            rating_data = self._extract_and_validate_rating_data(request.data)
            if isinstance(rating_data, Response):  # C'est une erreur
                return rating_data

            # Création du rating
            rating = self._create_rating(reservation, user, rating_data)

            logger.info(
                f"Rating créé: {rating.note}/5 par {user.email} "
                f"pour {rating.rated.email}"
            )

            return Response(
                {
                    "success": True,
                    "message": "Note enregistrée avec succès",
                    "rating": RatingSerializer(rating).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"Erreur rating: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return Response(
                {"error": "Erreur serveur", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _validate_rating_permissions(self, reservation, user):
        if reservation.passager != user:
            logger.warning(f"Tentative notation par non-passager: {user.email}")
            return Response(
                {"error": "Seul le passager peut noter le conducteur"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if reservation.status != "CONFIRMED":
            return Response(
                {
                    "error": "Réservation non confirmée",
                    "message": "Vous ne pouvez noter que les réservations confirmées",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if hasattr(reservation, "rating"):
            return Response(
                {
                    "error": "Déjà noté",
                    "message": "Vous avez déjà noté ce trajet",
                    "rating": RatingSerializer(reservation.rating).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    def _extract_and_validate_rating_data(self, data):
        """Extrait et valide les données de notation."""
        note = data.get("note")
        ponctualite = data.get("ponctualite")
        convivialite = data.get("convivialite")
        conduite = data.get("conduite")
        comment = data.get("comment", "")
        if not note or not isinstance(note, int) or not 1 <= note <= 5:
            return Response(
                {"error": "La note doit être un entier entre 1 et 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        validation_error = self._validate_optional_ratings(
            ponctualite, convivialite, conduite
        )
        if validation_error:
            return validation_error
        if len(comment) > 500:
            return Response(
                {"error": "Le commentaire ne peut pas dépasser 500 caractères"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return {
            "note": note,
            "ponctualite": ponctualite,
            "convivialite": convivialite,
            "conduite": conduite,
            "comment": comment,
        }

    def _validate_optional_ratings(self, ponctualite, convivialite, conduite):
        """Valide les notes optionnelles."""
        for field_name, field_value in [
            ("ponctualite", ponctualite),
            ("convivialite", convivialite),
            ("conduite", conduite),
        ]:
            if field_value is not None:
                if not isinstance(field_value, int) or not 1 <= field_value <= 5:
                    return Response(
                        {"error": f"La note de {field_name} doit être entre 1 et 5"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        return None

    def _create_rating(self, reservation, user, rating_data):
        """Crée l'objet Rating."""
        conducteur = reservation.trajet.conducteur
        return Rating.objects.create(
            reservation=reservation,
            rater=user,
            rated=conducteur,
            note=rating_data["note"],
            ponctualite=rating_data["ponctualite"],
            convivialite=rating_data["convivialite"],
            conduite=rating_data["conduite"],
            comment=rating_data["comment"],
        )


class ReservationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.reservations"
    verbose_name = "Réservations"
