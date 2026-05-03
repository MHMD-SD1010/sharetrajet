import logging
import traceback

from django.db import models
from django.db.models import Avg, Q
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.core.filters import TrajetFilter
from app.reservations.models import Rating as Avis
from app.reservations.models import Reservation
from app.users.models import UserDocument
from utils.pricing import get_fuel_prices_summary

from .models import FuelPrice, Trajet
from .permissions import (
    CanCancelTrajet,
    CanViewTrajetReservations,
)
from .serializers import (
    FuelPriceSerializer,
    TrajetCreateSerializer,
    TrajetDetailSerializer,
    TrajetListSerializer,
    TrajetSearchSerializer,
    TrajetUpdateSerializer,
)

logger = logging.getLogger(__name__)


class TrajetViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des trajets avec recherche intelligente"""

    queryset = Trajet.objects.select_related("conducteur").prefetch_related(
        "etapes", "preferences"
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TrajetFilter
    search_fields = ["ville_depart", "ville_arrivee", "description"]
    ordering_fields = ["date", "heure_depart", "price", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == "list":
            return TrajetListSerializer
        elif self.action == "create":
            return TrajetCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return TrajetUpdateSerializer
        elif self.action == "intelligent_search":
            return TrajetSearchSerializer
        return TrajetDetailSerializer

    def get_permissions(self):
        """✅ Permissions selon l'action"""
        if self.action in [
            "list",
            "retrieve",
            "search",
            "intelligent_search",
            "driver_info",
            "passengers",
            "fuel_prices",
            "_validate_search_params",
            "_build_base_queryset",
            "_build_city_filter",
            "_apply_advanced_filters",
            "_apply_price_filter",
            "_apply_time_filter",
            "_apply_preference_filter",
            "_extract_search_params",
            "places",
        ]:
            return [AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_authenticators(self):
        """✅ Désactiver JWT pour les recherches publiques"""
        action = getattr(self, "action", None)
        if action in [
            "list",
            "retrieve",
            "search",
            "intelligent_search",
            "driver_info",
            "passengers",
            "fuel_prices",
            "_validate_search_params",
            "_build_base_queryset",
            "_build_city_filter",
            "_apply_advanced_filters",
            "_apply_price_filter",
            "_apply_time_filter",
            "_apply_preference_filter",
            "_extract_search_params",
            "places",
        ]:
            return []
        return super().get_authenticators()

    def get_queryset(self):
        """Filtre le queryset selon le contexte"""
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(status="ACTIVE")
        return queryset

    def perform_create(self, serializer):
        """Crée un trajet avec le conducteur authentifié"""
        serializer.save()

    # ========== 🆕 API ENRICHIE - INFOS CONDUCTEUR ==========
    @action(
        detail=True,
        methods=["get"],
        url_path="driver_info",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def driver_info(self, request, pk=None):
        """
        API pour récupérer les informations enrichies du conducteur d'un trajet
        GET /api/v1/trajets/{id}/driver_info/
        """
        try:
            trajet = self.get_object()
            conducteur = trajet.conducteur

            # 1️⃣ Photo de profil
            profile_picture_url = None
            if conducteur.profile_picture:
                try:
                    profile_picture_url = request.build_absolute_uri(
                        conducteur.profile_picture.url
                    )
                except Exception as e:
                    logger.warning(f"Erreur photo profil: {str(e)}")

            # 2️⃣ Nombre de trajets en tant que conducteur
            trips_as_driver = Trajet.objects.filter(
                conducteur=conducteur, status__in=["ACTIVE", "COMPLETED"]
            ).count()

            # 3️⃣ Nombre de trajets en tant que passager
            trips_as_passenger = Reservation.objects.filter(
                passager=conducteur, status="CONFIRMED"
            ).count()

            # 4️⃣ Note moyenne (avis reçus)
            average_rating = (
                Avis.objects.filter(rated=conducteur).aggregate(Avg("note"))[
                    "note__avg"
                ]
                or 5.0
            )

            # 5️⃣ Statut de vérification (documents vérifiés)
            is_verified = UserDocument.objects.filter(
                user=conducteur, verified=True
            ).exists()

            # 6️⃣ Date d'inscription
            member_since = None
            date_joined_iso = None
            try:
                if hasattr(conducteur, "date_joined") and conducteur.date_joined:
                    member_since = conducteur.date_joined.strftime("%Y-%m-%d")
                    date_joined_iso = conducteur.date_joined.isoformat()
            except Exception as e:
                logger.warning(f"Erreur date inscription: {str(e)}")

            data = {
                "id": conducteur.id,
                "first_name": conducteur.first_name or "",
                "last_name": conducteur.last_name or "",
                "full_name": f"{conducteur.first_name or ''} {conducteur.last_name or ''}".strip()
                or "Utilisateur",
                "profile_picture": profile_picture_url,
                "date_joined": date_joined_iso,
                "member_since": member_since,
                "trips_as_driver": trips_as_driver,
                "trips_as_passenger": trips_as_passenger,
                "total_trips": trips_as_driver + trips_as_passenger,
                "rating": round(average_rating, 1),
                "is_verified": is_verified,
            }

            logger.info(
                f"[OK] Driver info retrieved for trajet {pk}: {data['full_name']}"
            )
            return Response(data, status=status.HTTP_200_OK)

        except Trajet.DoesNotExist:
            logger.error(f"Trajet {pk} non trouve")
            return Response(
                {"error": "Trajet non trouve"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"[ERROR] driver_info: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {
                    "error": "Erreur lors de la recuperation des informations du conducteur"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ========== 🆕 API ENRICHIE - INFOS PASSAGERS ==========
    @action(
        detail=True,
        methods=["get"],
        url_path="passengers",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def passengers(self, request, pk=None):
        """
        🎯 API pour récupérer les passagers confirmés d'un trajet avec leurs infos
        GET /api/v1/trajets/{id}/passengers/
        """
        try:
            trajet = self.get_object()

            # Récupérer toutes les réservations confirmées
            reservations = Reservation.objects.filter(
                trajet=trajet, status="CONFIRMED"
            ).select_related("passager")

            passengers_data = []
            for reservation in reservations:
                passager = reservation.passager

                # Photo de profil
                profile_picture_url = None
                if passager.profile_picture:
                    profile_picture_url = request.build_absolute_uri(
                        passager.profile_picture.url
                    )

                passengers_data.append(
                    {
                        "id": passager.id,
                        "first_name": passager.first_name,
                        "last_name": passager.last_name,
                        "full_name": f"{passager.first_name} {passager.last_name}",
                        "profile_picture": profile_picture_url,
                        "nbr_places": reservation.nbr_places,
                        "reservation_id": reservation.id,
                    }
                )

            logger.info(
                f"✅ {len(passengers_data)} passengers retrieved for trajet {pk}"
            )
            return Response(
                {
                    "trajet_id": trajet.id,
                    "passengers_count": len(passengers_data),
                    "passengers": passengers_data,
                },
                status=status.HTTP_200_OK,
            )

        except Trajet.DoesNotExist:
            return Response(
                {"error": "Trajet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"❌ Erreur passengers: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Erreur lors de la récupération des passagers"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=True,
        methods=["get"],
        url_path="places",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def places(self, request, pk=None):
        """Retourne le nombre de places disponibles en temps réel"""
        try:
            trajet = self.get_object()

            # Calcul manuel FIABLE
            reservations_confirmees = (
                Reservation.objects.filter(
                    trajet=trajet, status__in=["PENDING", "CONFIRMED"]
                ).aggregate(total=models.Sum("nbr_places"))["total"]
                or 0
            )

            places_calculees = trajet.nbr_places - reservations_confirmees

            # ✅ Mettre à jour la base de données si nécessaire
            if trajet.places_disponibles != places_calculees:
                logger.warning(
                    f"⚠️ Trajet {trajet.id}: DB={trajet.places_disponibles}, "
                    f"Calculé={places_calculees}. Correction..."
                )
                trajet.places_disponibles = places_calculees
                trajet.save(update_fields=["places_disponibles"])

            return Response(
                {
                    "places_disponibles": places_calculees,
                    "trajet_id": trajet.id,
                    "nbr_places_total": trajet.nbr_places,
                    "reservations_total": reservations_confirmees,
                }
            )
        except Exception as e:
            logger.error(f"Erreur get places: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {"error": "Erreur lors de la récupération des places"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ========== RECHERCHE SIMPLE (PUBLIC) ==========
    @action(
        detail=False,
        methods=["post"],
        url_path="search",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def search(self, request):
        """
        🔍 RECHERCHE SIMPLE - Pour la recherche initiale (page d'accueil)
        POST /api/v1/trajets/search/
        """
        data = request.data

        ville_depart = data.get("ville_depart", "").strip()
        ville_arrivee = data.get("ville_arrivee", "").strip()
        date = data.get("date")
        nbr_places = data.get("nbr_places", 1)

        if not ville_depart or not ville_arrivee:
            return Response(
                {"error": "ville_depart et ville_arrivee sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Recherche flexible
        depart_parts = [p.strip() for p in ville_depart.split(",") if p.strip()]
        arrivee_parts = [p.strip() for p in ville_arrivee.split(",") if p.strip()]

        depart_q = Q()
        for part in depart_parts:
            depart_q |= Q(ville_depart__icontains=part)

        arrivee_q = Q()
        for part in arrivee_parts:
            arrivee_q |= Q(ville_arrivee__icontains=part)

        queryset = (
            Trajet.objects.filter(status="ACTIVE", places_disponibles__gte=nbr_places)
            .filter(depart_q)
            .filter(arrivee_q)
            .select_related("conducteur")
        )

        if date:
            queryset = queryset.filter(date=date)

        queryset = queryset.order_by("date", "heure_depart", "price")
        serializer = TrajetListSerializer(queryset, many=True)

        logger.info(f"🔍 Recherche simple: {queryset.count()} trajet(s) trouvé(s)")

        return Response(
            {
                "results": serializer.data,
                "count": queryset.count(),
                "search_params": {
                    "depart": ville_depart,
                    "arrivee": ville_arrivee,
                    "date": date,
                    "places": nbr_places,
                },
            },
            status=status.HTTP_200_OK,
        )

    # ========== RECHERCHE INTELLIGENTE (PUBLIC) ==========
    @action(
        detail=False,
        methods=["post"],
        url_path="intelligent-search",  # ✅ CHANGÉ: Tiret au lieu d'underscore
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def intelligent_search(self, request):
        """
        🔍 RECHERCHE INTELLIGENTE - Avec filtres avancés
        POST /api/v1/trajets/intelligent-search/
        """
        try:
            data = request.data
            logger.info(f"🔍 INTELLIGENT SEARCH - Données reçues: {data}")

            # Validation des paramètres obligatoires
            validation_error = self._validate_search_params(data)
            if validation_error:
                return validation_error

            # Construction de la requête de base
            queryset = self._build_base_queryset(data)

            # Application des filtres avancés
            queryset = self._apply_advanced_filters(queryset, data)

            # Tri et sérialisation
            queryset = queryset.order_by("date", "heure_depart", "price")
            serializer = TrajetListSerializer(queryset, many=True)

            logger.info(f"✅ Résultats finaux: {len(serializer.data)} trajets")

            return Response(
                {
                    "results": serializer.data,
                    "count": queryset.count(),
                    "search_params": self._extract_search_params(data),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"❌ Erreur intelligent_search: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {
                    "error": "Erreur lors de la recherche",
                    "detail": str(e),
                    "type": "server_error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _validate_search_params(self, data):
        """Valide les paramètres de recherche obligatoires."""
        ville_depart = data.get("ville_depart", "").strip()
        ville_arrivee = data.get("ville_arrivee", "").strip()

        if not ville_depart or not ville_arrivee:
            return Response(
                {"error": "ville_depart et ville_arrivee sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def _build_base_queryset(self, data):
        """Construit la requête de base avec les filtres de ville et places."""
        ville_depart = data.get("ville_depart", "").strip()
        ville_arrivee = data.get("ville_arrivee", "").strip()
        nbr_places = data.get("nbr_places", 1)

        # Construction des filtres de ville flexibles
        depart_q = self._build_city_filter(ville_depart)
        arrivee_q = self._build_city_filter(ville_arrivee)

        # Requête de base
        return (
            Trajet.objects.filter(status="ACTIVE", places_disponibles__gte=nbr_places)
            .filter(depart_q)
            .filter(arrivee_q)
            .select_related("conducteur")
            .prefetch_related("preferences")
        )

    def _build_city_filter(self, city_name):
        """Construit un filtre Q pour recherche flexible sur les villes."""
        city_parts = [p.strip() for p in city_name.split(",") if p.strip()]
        city_q = Q()
        for part in city_parts:
            city_q |= Q(ville_depart__icontains=part) | Q(ville_arrivee__icontains=part)
        return city_q

    def _apply_advanced_filters(self, queryset, data):
        """Applique les filtres avancés au queryset."""
        # Filtre par date
        date = data.get("date")
        if date:
            queryset = queryset.filter(date=date)

        # Filtre par prix maximum
        queryset = self._apply_price_filter(queryset, data.get("price_max"))

        # Filtre par horaire de départ
        queryset = self._apply_time_filter(queryset, data.get("departure_time"))

        # Filtre confort
        if data.get("is_confort"):
            queryset = queryset.filter(is_confort=True)

        # Filtre par préférences
        queryset = self._apply_preference_filter(
            queryset, data.get("preference_ids", [])
        )

        return queryset

    def _apply_price_filter(self, queryset, price_max):
        """Applique le filtre de prix maximum."""
        if price_max:
            return queryset.filter(price__lte=price_max)
        return queryset

    def _apply_time_filter(self, queryset, departure_time):
        """Applique le filtre d'horaire de départ."""
        if not departure_time:
            return queryset

        time_filters = {
            "morning": Q(heure_depart__lt="12:00"),
            "afternoon": Q(heure_depart__gte="12:00", heure_depart__lt="18:00"),
            "evening": Q(heure_depart__gte="18:00"),
        }

        time_filter = time_filters.get(departure_time)
        if time_filter:
            return queryset.filter(time_filter)
        return queryset

    def _apply_preference_filter(self, queryset, preference_ids):
        """Applique le filtre de préférences."""
        if preference_ids and len(preference_ids) > 0:
            return queryset.filter(preferences__id__in=preference_ids).distinct()
        return queryset

    def _extract_search_params(self, data):
        """Extrait les paramètres de recherche pour la réponse."""
        return {
            "depart": data.get("ville_depart", "").strip(),
            "arrivee": data.get("ville_arrivee", "").strip(),
            "date": data.get("date"),
            "places": data.get("nbr_places", 1),
        }

    # ========== AUTRES ACTIONS ==========
    @action(detail=False, methods=["get"])
    def my_trips(self, request):
        """Liste les trajets de l'utilisateur connecté"""
        queryset = self.queryset.filter(conducteur=request.user)
        status_filter = request.query_params.get("status")

        # ✅ CORRECTION: Filtrer par status EXACT, pas par choix
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrajetListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TrajetListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated, CanCancelTrajet],
    )
    def cancel(self, request, pk=None):
        """Annule un trajet"""
        trajet = self.get_object()
        self.check_object_permissions(request, trajet)

        trajet.status = "CANCELLED"
        trajet.save()

        from app.notifications.models import Notification

        for reservation in trajet.reservations.filter(
            status__in=["PENDING", "CONFIRMED"]
        ):
            Notification.objects.create(
                recipient=reservation.passager,
                sender=request.user,
                type="TRAJET_CANCELLED",
                content=f"Le trajet {trajet} a été annulé par le conducteur",
                related_model="Trajet",
                related_id=trajet.id,
            )
            reservation.cancel("Trajet annulé par le conducteur")

        return Response(
            {
                "message": "Trajet annulé avec succès",
                "trajet": TrajetDetailSerializer(trajet).data,
            }
        )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated, CanViewTrajetReservations],
    )
    def reservations(self, request, pk=None):
        """Liste les réservations d'un trajet"""
        trajet = self.get_object()
        self.check_object_permissions(request, trajet)

        from app.reservations.serializers import ReservationSerializer

        reservations = trajet.reservations.select_related("passager").all()

        if request.user != trajet.conducteur:
            reservations = reservations.filter(passager=request.user)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """Liste les trajets à venir"""
        today = timezone.now().date()
        queryset = self.queryset.filter(
            conducteur=request.user, date__gte=today, status="ACTIVE"
        ).order_by("date", "heure_depart")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrajetListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TrajetListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def past(self, request):
        """Liste les trajets passés"""
        today = timezone.now().date()
        queryset = self.queryset.filter(
            Q(conducteur=request.user),
            Q(date__lt=today) | Q(status__in=["COMPLETED", "CANCELLED"]),
        ).order_by("-date", "-heure_depart")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrajetListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TrajetListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        """Statistiques d'un trajet (conducteur uniquement)"""
        trajet = self.get_object()

        if trajet.conducteur != request.user:
            return Response(
                {"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN
            )

        reservations = trajet.reservations.all()

        stats = {
            "total_reservations": reservations.count(),
            "pending": reservations.filter(status="PENDING").count(),
            "confirmed": reservations.filter(status="CONFIRMED").count(),
            "rejected": reservations.filter(status="REJECTED").count(),
            "cancelled": reservations.filter(status="CANCELLED").count(),
            "places_reserved": sum(
                r.nbr_places for r in reservations.filter(status="CONFIRMED")
            ),
            "places_disponibles": trajet.places_disponibles,
            "revenue_estimate": sum(
                r.total_price for r in reservations.filter(status="CONFIRMED")
            ),
        }

        return Response(stats)

    @action(
        detail=False,
        methods=["get"],
        url_path="fuel-prices",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def fuel_prices(self, request):
        """
        Liste les prix du carburant pour l'API frontend
        GET /api/v1/trajets/fuel-prices/
        """
        try:
            data = get_fuel_prices_summary()
            if data:
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {
                    "error": "Impossible de charger les prix du carburant",
                    "message": "Le fichier prix_carburants.json est introuvable",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erreur fuel_prices: {str(e)}")
            return Response(
                {"error": "Erreur serveur", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FuelPriceViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des prix du carburant"""

    queryset = FuelPrice.objects.all()
    serializer_class = FuelPriceSerializer
    permission_classes = [permissions.AllowAny]  # ✅ CORRECTION: Public
    authentication_classes = []  # ✅ CORRECTION: Désactiver JWT

    def list(self, request):
        """
        Liste tous les prix du carburant
        GET /api/v1/trajets/fuel-prices/
        """
        try:
            # Récupérer depuis utils.pricing
            data = get_fuel_prices_summary()

            if data:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "error": "Impossible de charger les prix du carburant",
                        "message": "Le fichier prix_carburants.json est introuvable",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            logger.error(f"Erreur fuel_prices: {str(e)}")
            return Response(
                {"error": "Erreur serveur", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
