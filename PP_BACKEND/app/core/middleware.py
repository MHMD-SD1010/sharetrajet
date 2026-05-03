import logging

from django.contrib.auth import get_user_model
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


class RequestLoggingMiddleware:
    """
    Middleware pour logger toutes les requêtes API
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log avant la requête
        start_time = timezone.now()

        # Traiter la requête
        response = self.get_response(request)

        # Log après la requête
        duration = (timezone.now() - start_time).total_seconds()

        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": f"{duration:.3f}s",
            "user": getattr(request.user, "email", "Anonymous"),
            "ip": self.get_client_ip(request),
        }

        if response.status_code >= 400:
            logger.warning(f"Request failed: {log_data}")
        else:
            logger.info(f"Request processed: {log_data}")

        return response

    @staticmethod
    def get_client_ip(request):
        """Récupère l'IP réelle du client"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class UserActivityMiddleware:
    """
    Middleware pour tracker la dernière activité des utilisateurs
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Mettre à jour last_activity pour les utilisateurs authentifiés
        if request.user.is_authenticated:
            # Utiliser update() pour éviter de déclencher les signaux
            User.objects.filter(pk=request.user.pk).update(updated_at=timezone.now())

        return response


class CORSMiddleware:
    """
    Middleware personnalisé pour gérer CORS de manière plus fine
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Ajouter des headers CORS personnalisés si nécessaire
        if request.path.startswith("/api/"):
            origin = request.META.get("HTTP_ORIGIN", "")

            # Liste des origines autorisées
            allowed_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "https://dzcarpool.com",
            ]

            if origin in allowed_origins:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Credentials"] = "true"

        return response


class RateLimitMiddleware:
    """
    Middleware simple de rate limiting
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_cache = {}

    def __call__(self, request):
        # Implémenter la logique de rate limiting
        ip = self.get_client_ip(request)
        current_time = timezone.now()

        # Nettoyer les entrées expirées (plus d'1 minute)
        self.rate_limit_cache = {
            k: v
            for k, v in self.rate_limit_cache.items()
            if (current_time - v["timestamp"]).seconds < 60
        }

        # Vérifier le rate limit
        if ip in self.rate_limit_cache:
            cache_entry = self.rate_limit_cache[ip]
            cache_entry["count"] += 1

            # Limite: 100 requêtes par minute
            if cache_entry["count"] > 100:
                from django.http import JsonResponse

                return JsonResponse(
                    {"error": "Rate limit exceeded. Please try again later."},
                    status=429,
                )
        else:
            self.rate_limit_cache[ip] = {"count": 1, "timestamp": current_time}

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
