from functools import wraps

from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response


def cache_response(timeout=300, key_prefix="view"):
    """
    Décorateur pour mettre en cache les réponses des vues
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Construire la clé de cache
            cache_key = (
                f"{key_prefix}:"
                f"{request.path}:"
                f"{request.user.id if request.user.is_authenticated else 'anon'}"
            )

            # Vérifier le cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return Response(cached_response)

            # Exécuter la vue
            response = func(self, request, *args, **kwargs)

            # Mettre en cache si succès
            if response.status_code == 200:
                cache.set(cache_key, response.data, timeout)

            return response

        return wrapper

    return decorator


def require_verified_account(func):
    """
    Décorateur pour exiger un compte vérifié (téléphone ou documents)
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentification requise"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Vérifier si au moins le téléphone ou un document est vérifié
        has_verified_phone = request.user.phone_verified
        has_verified_document = request.user.documents.filter(verified=True).exists()

        if not (has_verified_phone or has_verified_document):
            return Response(
                {
                    "error": (
                        "Compte non vérifié. "
                        "Veuillez vérifier votre téléphone ou soumettre un document."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return func(self, request, *args, **kwargs)

    return wrapper


def admin_only(func):
    """
    Décorateur pour limiter l'accès aux administrateurs
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(
                {"error": "Accès réservé aux administrateurs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return func(self, request, *args, **kwargs)

    return wrapper
