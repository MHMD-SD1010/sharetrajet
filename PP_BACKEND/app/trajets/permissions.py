from rest_framework import permissions


class IsDriverOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement au conducteur
    de modifier ou supprimer un trajet
    """

    def has_permission(self, request, view):
        # Les requêtes de lecture sont autorisées pour les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Les requêtes de création sont autorisées pour tous les utilisateurs authentifiés
        if request.method == "POST":
            return request.user and request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        # Les requêtes de lecture sont autorisées pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les requêtes d'écriture sont autorisées uniquement au conducteur
        return obj.conducteur == request.user


class CanModifyTrajet(permissions.BasePermission):
    """
    Permission pour modifier un trajet
    """

    def has_object_permission(self, request, view, obj):
        # Seul le conducteur peut modifier son trajet
        if obj.conducteur != request.user:
            return False

        # Ne peut pas modifier un trajet terminé ou annulé
        if obj.status in ["COMPLETED", "CANCELLED"]:
            return False

        # Ne peut pas modifier si des réservations sont confirmées
        if view.action in ["update", "partial_update"]:
            has_confirmed_reservations = obj.reservations.filter(
                status="CONFIRMED"
            ).exists()

            if has_confirmed_reservations:
                # Peut modifier certains champs seulement
                allowed_fields = ["description", "adresse_depart", "adresse_arrivee"]
                if not all(field in allowed_fields for field in request.data.keys()):
                    return False

        return True


class CanCancelTrajet(permissions.BasePermission):
    """
    Permission pour annuler un trajet
    """

    def has_object_permission(self, request, view, obj):
        # Seul le conducteur peut annuler
        if obj.conducteur != request.user:
            return False

        # Ne peut pas annuler un trajet déjà terminé ou annulé
        if obj.status in ["COMPLETED", "CANCELLED"]:
            return False

        return True


class CanViewTrajetReservations(permissions.BasePermission):
    """
    Permission pour voir les réservations d'un trajet
    """

    def has_object_permission(self, request, view, obj):
        # Seul le conducteur peut voir toutes les réservations
        if obj.conducteur == request.user:
            return True

        # Les passagers ne peuvent voir que leurs propres réservations
        if request.user.is_authenticated:
            return obj.reservations.filter(passager=request.user).exists()

        return False
