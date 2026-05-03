"""
Middleware d'authentification JWT pour WebSocket
"""
import traceback
from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    """Récupère l'utilisateur depuis le token JWT"""
    try:
        print(f"🔍 Validation token JWT...")
        access_token = AccessToken(token_key)
        user_id = access_token.payload.get('user_id')
        user = User.objects.get(id=user_id)
        print(f"✅ User authentifié: {user.email} (ID: {user.id})")
        return user
    except Exception as e:
        print(f"❌ Erreur authentification WebSocket: {e}")
        traceback.print_exc()
        return AnonymousUser()


class JWTAuthMiddleware:
    """Middleware pour authentifier via token JWT dans l'URL"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        print("=" * 80)
        print("🔌 NOUVEAU WebSocket - Middleware JWT activé")
        print(f"   Path: {scope.get('path')}")
        print(f"   Type: {scope.get('type')}")
        
        try:
            # Récupérer le token depuis les query params
            query_string = scope.get('query_string', b'').decode()
            print(f"   Query string: {query_string[:100]}...")
            
            query_params = parse_qs(query_string)
            token = query_params.get('token', [None])[0]

            print(f"   Token présent: {bool(token)}")
            if token:
                print(f"   Token (preview): {token[:30]}...")

            if token:
                scope['user'] = await get_user_from_token(token)
            else:
                scope['user'] = AnonymousUser()
                print("   ⚠️ Pas de token fourni - User = Anonymous")

            print(f"   User final: {scope['user']}")
            print("=" * 80)
            
            return await self.app(scope, receive, send)
            
        except Exception as e:
            print(f"❌ ERREUR MIDDLEWARE: {e}")
            traceback.print_exc()
            print("=" * 80)
            # Re-raise pour que Daphne puisse gérer
            raise