from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les propriétaires à modifier un objet
    """

    def has_object_permission(self, request, view, obj):
        # Les requêtes de lecture sont autorisées pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True

        # Les requêtes d'écriture sont autorisées uniquement au propriétaire
        return obj.user == request.user or obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission qui autorise uniquement les admins à modifier
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Permission qui permet la création sans authentification mais requiert
    l'authentification pour les autres opérations
    """

    def has_permission(self, request, view):
        if request.method == "POST" and view.action == "create":
            return True

        return request.user and request.user.is_authenticated
