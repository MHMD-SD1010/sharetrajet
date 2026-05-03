"""
Middleware pour l'authentification JWT via WebSocket
"""

from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class JWTAuthMiddleware:
    """
    Middleware personnalisé pour authentifier les connexions WebSocket via JWT
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Récupérer le token depuis query params
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if token:
            try:
                # Valider le token
                access_token = AccessToken(token)
                user_id = access_token["user_id"]

                # Récupérer l'utilisateur
                scope["user"] = await self.get_user(user_id)
            except Exception as e:
                print(f"❌ Erreur authentification WebSocket: {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """Récupère l'utilisateur depuis la base de données"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
