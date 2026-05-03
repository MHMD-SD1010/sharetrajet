from rest_framework import permissions

from .models import Reservation


class IsReservationOwnerOrDriver(permissions.BasePermission):
    """
    Permission pour les réservations: passager ou conducteur du trajet
    """

    def has_object_permission(self, request, view, obj):
        # Le passager et le conducteur peuvent voir la réservation
        is_passager = obj.passager == request.user
        is_conducteur = obj.trajet.conducteur == request.user

        # Pour les modifications/suppressions
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Seul le passager peut modifier/annuler sa propre réservation
            if view.action == "cancel":
                return is_passager
            # Le conducteur peut approuver/rejeter
            if view.action in ["approve", "reject"]:
                return is_conducteur

        return is_passager or is_conducteur


class CanRateReservation(permissions.BasePermission):
    """
    Permission pour noter une réservation
    """

    def has_object_permission(self, request, view, obj):
        # L'utilisateur doit être soit le passager soit le conducteur
        return obj.passager == request.user or obj.trajet.conducteur == request.user


class IsDriverOfReservationTrip(permissions.BasePermission):
    """
    Vérifie que l'utilisateur est le conducteur du trajet associé à la réservation.
    """

    def has_object_permission(self, request, view, obj: Reservation):
        # obj ici est une instance de Reservation
        return obj.trajet.conducteur == request.user


class IsPassengerOfReservation(permissions.BasePermission):
    """
    Vérifie que l'utilisateur est le passager de la réservation.
    """

    def has_object_permission(self, request, view, obj: Reservation):
        # obj est une instance de Reservation
        return obj.passager == request.user
