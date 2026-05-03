"""
app/messaging/urls.py (ou app/notifications/urls.py)
"""

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"conversations", ConversationViewSet, basename="conversation")

app_name = "messaging"

urlpatterns = [
    path("", include(router.urls)),
]

# ✅ Les routes générées automatiquement seront:
# POST   /api/v1/messaging/messages/upload-media/      - Upload de média
# GET    /api/v1/messaging/messages/                   - Liste des messages
# POST   /api/v1/messaging/messages/                   - Créer un message
# GET    /api/v1/messaging/messages/{id}/              - Détail d'un message
# etc...

# ⚠️ IMPORTANT: L'URL complète dépend de comment vous incluez ces URLs dans config/urls.py
# Si vous avez: path('api/v1/messaging/', include('app.messaging.urls'))
# Alors l'endpoint sera: /api/v1/messaging/messages/upload-media/
#
# Si vous avez: path('api/v1/', include('app.messaging.urls'))
# Alors l'endpoint sera: /api/v1/messages/upload-media/
