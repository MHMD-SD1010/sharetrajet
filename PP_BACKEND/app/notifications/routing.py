from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from app.messaging.consumers import ChatConsumer
from app.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    # Notifications
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    # Messagerie - Groupe
    path("ws/chat/group/<int:trajet_id>/", ChatConsumer.as_asgi()),
    # Messagerie - Privée
    path("ws/chat/private/<str:conversation_id>/", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
