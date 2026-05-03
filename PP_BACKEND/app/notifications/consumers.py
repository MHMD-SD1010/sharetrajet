"""
app/notifications/consumers.py - Consumer WebSocket pour notifications
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Notification
from .serializers import NotificationSerializer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connexion WebSocket"""
        self.user = self.scope.get("user")

        if not self.user or not self.user.is_authenticated:
            print("❌ Utilisateur non authentifié, fermeture connexion")
            await self.close()
            return

        # Chaque utilisateur a son propre canal de notifications
        self.notification_group = f"notifications_{self.user.id}"

        # Rejoindre le groupe de notifications de l'utilisateur
        await self.channel_layer.group_add(self.notification_group, self.channel_name)

        await self.accept()
        print("=" * 80)
        print(f"✅ {self.user.full_name} connecté aux notifications")
        print(f"   User ID: {self.user.id}")
        print(f"   Group: {self.notification_group}")
        print(f"   Channel: {self.channel_name}")
        print("=" * 80)

        # Envoyer les notifications non lues au chargement
        await self.send_unread_notifications()

    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        if hasattr(self, "notification_group"):
            await self.channel_layer.group_discard(
                self.notification_group, self.channel_name
            )
            print(f"❌ {self.user.full_name} déconnecté des notifications")

    async def receive(self, text_data):
        """Réception de messages du client"""
        try:
            data = json.loads(text_data)
            action = data.get("action")

            print(f"📥 Message reçu du client: {action}")

            if action == "mark_as_read":
                notification_id = data.get("notification_id")
                await self.mark_notification_as_read(notification_id)
            elif action == "mark_all_read":
                await self.mark_all_as_read()
            else:
                print(f"⚠️ Action inconnue: {action}")

        except Exception as e:
            print(f"❌ Erreur receive: {e}")
            import traceback

            traceback.print_exc()

    async def notification_message(self, event):
        """
        ✅ HANDLER POUR LES NOTIFICATIONS
        Appelé quand channel_layer.group_send() envoie un message de type "notification_message"
        """
        print("=" * 80)
        print("notification_message handler appelé")
        print(f"User: {self.user.full_name}")
        print(f"   Event keys: {event.keys()}")
        print("=" * 80)

        notification = event.get("notification")

        if not notification:
            print("❌ Pas de notification dans l'event")
            return

        print(f"✅ Envoi notification WS à {self.user.full_name}")
        print(f"   Type: {notification.get('type')}")
        print(f"   Content: {notification.get('content')}")

        # Envoyer au client
        await self.send(
            text_data=json.dumps(
                {"type": "new_notification", "notification": notification}
            )
        )

        print("Notification envoyée au client")

    @database_sync_to_async
    def get_unread_notifications_sync(self):
        """Récupère les notifications non lues depuis la base"""
        notifications = (
            Notification.objects.filter(recipient=self.user, is_read=False)
            .select_related("sender")
            .order_by("-created_at")[:20]
        )

        return NotificationSerializer(notifications, many=True).data

    async def send_unread_notifications(self):
        """Envoie les notifications non lues au client"""
        notifications = await self.get_unread_notifications_sync()
        print(f"📬 Envoi de {len(notifications)} notifications non lues")

        await self.send(
            text_data=json.dumps(
                {"type": "unread_notifications", "notifications": notifications}
            )
        )

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """Marque une notification comme lue"""
        try:
            notification = Notification.objects.get(
                id=notification_id, recipient=self.user
            )
            notification.mark_as_read()
            print(f"✅ Notification {notification_id} marquée comme lue")
            return True
        except Notification.DoesNotExist:
            print(f"❌ Notification {notification_id} introuvable")
            return False

    @database_sync_to_async
    def mark_all_as_read(self):
        """Marque toutes les notifications comme lues"""
        count = Notification.objects.filter(recipient=self.user, is_read=False).update(
            is_read=True
        )

        print(f"✅ {count} notifications marquées comme lues")
        return count
