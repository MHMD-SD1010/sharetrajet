"""
app/reservations/urls.py - CORRECTION FINALE
"""

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ReservationViewSet

router = DefaultRouter()
# FIX: Utiliser '' au lieu de 'reservations'
# Car le prefix est déjà dans urls.py principal
router.register(r"", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]

# URLs MAINTENANT CORRECTES:
# POST   /api/v1/reservations/                           - Créer une réservation
# GET    /api/v1/reservations/                           - Liste
# GET    /api/v1/reservations/{id}/                      - Détails
# PUT    /api/v1/reservations/{id}/                      - Modifier
# DELETE /api/v1/reservations/{id}/                      - Supprimer
# GET    /api/v1/reservations/my-bookings/               - Mes réservations
# GET    /api/v1/reservations/my-trips-bookings/         - Réservations de mes trajets
# POST   /api/v1/reservations/{id}/confirm/              - Confirmer
# POST   /api/v1/reservations/{id}/reject/               - Rejeter
# POST   /api/v1/reservations/{id}/cancel/               - Annuler
# GET    /api/v1/reservations/check-booking-permission/  - Vérifier permission
