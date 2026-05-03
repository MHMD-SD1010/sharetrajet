from django.urls import re_path

from app.messaging.consumers import ChatConsumer
from app.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/group/(?P<trajet_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/private/(?P<conversation_id>[\w_]+)/$", ChatConsumer.as_asgi()),
    re_path(r"^ws/notifications/$", NotificationConsumer.as_asgi()),
]
