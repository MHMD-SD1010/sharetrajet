"""
ASGI config for DZ-CarPool project.
"""
import os
from django.core.asgi import get_asgi_application

# ✅ Charger Django AVANT d'importer Channels
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()

# ✅ Importer Channels APRÈS get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter

from app.messaging.routing import websocket_urlpatterns
from app.core.middleware_websocket import JWTAuthMiddleware

# ============================================
# ✅ VERSION DEBUG - Sans AllowedHostsOriginValidator
# ============================================
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})



from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
