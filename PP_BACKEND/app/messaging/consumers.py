"""
app/messaging/consumers.py - Consumer WebSocket avec URLs média HTTP complètes
"""

import json
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer pour la messagerie en temps réel"""

    async def connect(self):
        """Connexion WebSocket"""
        print("=" * 80)
        print("🔌 ChatConsumer.connect() appelé")
        
        url_route = self.scope.get("url_route", {})
        kwargs = url_route.get("kwargs", {})
        print(f"   URL kwargs: {kwargs}")

        if "trajet_id" in kwargs:
            self.conversation_type = "group"
            self.conversation_id = kwargs["trajet_id"]
            print(f"   Type: GROUP - Trajet ID: {self.conversation_id}")
        elif "conversation_id" in kwargs:
            self.conversation_type = "private"
            self.conversation_id = kwargs["conversation_id"]
            print(f"   Type: PRIVATE - Conversation ID: {self.conversation_id}")
        else:
            logger.error(f"❌ Route WebSocket invalide: {kwargs}")
            print(f"❌ Route invalide - Fermeture 4000")
            await self.close(code=4000)
            return

        self.room_group_name = f"chat_{self.conversation_type}_{self.conversation_id}"
        self.user = self.scope.get("user")
        
        print(f"   User from scope: {self.user}")
        print(f"   Is authenticated: {self.user.is_authenticated if self.user else False}")

        if not self.user or not self.user.is_authenticated:
            logger.warning("❌ Utilisateur non authentifié")
            print("❌ User non authentifié - Fermeture 4001")
            await self.close(code=4001)
            return

        print("🔍 Vérification des permissions...")
        has_permission = await self.check_permission()
        print(f"   Permission accordée: {has_permission}")
        
        if not has_permission:
            logger.warning(f"❌ Permission refusée pour {self.user.email}")
            print(f"❌ Permission refusée - Fermeture 4003")
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"✅ {self.user.email} connecté à {self.room_group_name}")
        print(f"✅ CONNEXION ACCEPTÉE !")
        print("=" * 80)

        await self.send_message_history()

    async def disconnect(self, close_code):
        """Déconnexion"""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
            logger.info(
                f"Utilisateur {self.user.email} déconnecté de {self.room_group_name}"
            )

    async def receive(self, text_data):
        """Réception d'un message"""
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "message")

            if message_type == "message":
                await self.handle_message(data)
            elif message_type == "typing":
                await self.handle_typing(data)
            else:
                logger.warning(f"Type de message inconnu: {message_type}")

        except json.JSONDecodeError:
            logger.error("JSON invalide")
            await self.send_error("Format JSON invalide")
        except Exception as e:
            logger.error(f"Erreur receive: {e}", exc_info=True)
            await self.send_error(str(e))

    async def handle_message(self, data):
        """Traite un message texte"""
        text = data.get("text", "").strip()

        if not text:
            await self.send_error("Message vide")
            return

        message = await self.save_message(text)

        if not message:
            await self.send_error("Erreur de sauvegarde")
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": await self.format_message(message)},
        )

    async def handle_typing(self, data):
        """Gère l'indicateur de saisie"""
        is_typing = data.get("is_typing", False)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_typing",
                "user": {
                    "id": self.user.id,
                    "full_name": self.user.full_name,
                    "email": self.user.email,
                },
                "is_typing": is_typing,
            },
        )

    async def chat_message(self, event):
        """Envoie un message au WebSocket"""
        await self.send(text_data=json.dumps(event["message"]))

    async def user_typing(self, event):
        """Envoie l'indicateur de saisie"""
        if event["user"]["id"] != self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "typing",
                        "user": event["user"],
                        "is_typing": event["is_typing"],
                    }
                )
            )

    async def send_message_history(self):
        """Envoie l'historique des messages"""
        messages = await self.get_message_history()
        formatted_messages = []

        for msg in messages:
            formatted_messages.append(await self.format_message(msg))

        logger.info(f"Envoi de {len(formatted_messages)} messages d'historique")
        await self.send(
            text_data=json.dumps({"type": "history", "messages": formatted_messages})
        )

    async def send_error(self, error_message):
        """Envoie une erreur au client"""
        await self.send(text_data=json.dumps({"type": "error", "error": error_message}))

    @database_sync_to_async
    def check_permission(self):
        """Vérifie les permissions d'accès"""
        if self.conversation_type == "group":
            from app.reservations.models import Reservation
            from app.trajets.models import Trajet

            try:
                trajet_id = int(self.conversation_id)
                trajet = Trajet.objects.get(id=trajet_id)

                is_driver = trajet.conducteur == self.user
                has_reservation = Reservation.objects.filter(
                    trajet=trajet, passager=self.user, status="CONFIRMED"
                ).exists()

                return is_driver or has_reservation
            except (Trajet.DoesNotExist, ValueError):
                return False

        elif self.conversation_type == "private":
            try:
                user_ids = [int(uid) for uid in self.conversation_id.split("_")]
                return self.user.id in user_ids
            except (ValueError, AttributeError):
                return False

        return False

    @database_sync_to_async
    def save_message(self, text):
        """Sauvegarde le message en base de données"""
        from app.notifications.models import Message

        try:
            message_data = {
                "sender": self.user,
                "text": text,
            }

            if self.conversation_type == "group":
                from app.trajets.models import Trajet

                trajet_id = int(self.conversation_id)
                trajet = Trajet.objects.get(id=trajet_id)

                message_data["trajet"] = trajet
                message_data["is_group_message"] = True
                message_data["receiver"] = None

            elif self.conversation_type == "private":
                user_ids = [int(uid) for uid in self.conversation_id.split("_")]
                other_user_id = [uid for uid in user_ids if uid != self.user.id][0]
                receiver = User.objects.get(id=other_user_id)

                message_data["receiver"] = receiver
                message_data["is_group_message"] = False

            message = Message.objects.create(**message_data)
            logger.info(f"Message sauvegardé: ID={message.id}")

            self.update_conversation(message)

            return message

        except Exception as e:
            logger.error(f"Erreur sauvegarde: {e}", exc_info=True)
            return None

    @database_sync_to_async
    def get_message_history(self):
        """Récupère l'historique des messages"""
        from app.notifications.models import Message

        if self.conversation_type == "group":
            trajet_id = int(self.conversation_id)
            messages = (
                Message.objects.filter(trajet_id=trajet_id, is_group_message=True)
                .select_related("sender")
                .order_by("created_at")[:100]
            )

        elif self.conversation_type == "private":
            user_ids = [int(uid) for uid in self.conversation_id.split("_")]
            other_user_id = [uid for uid in user_ids if uid != self.user.id][0]

            messages = (
                Message.objects.filter(
                    Q(sender=self.user, receiver_id=other_user_id)
                    | Q(sender_id=other_user_id, receiver=self.user),
                    is_group_message=False,
                )
                .select_related("sender", "receiver")
                .order_by("created_at")[:100]
            )

        return list(messages)

    @database_sync_to_async
    def format_message(self, message):
        """Formate un message avec URLs complètes (HTTP)"""
        # Photo de profil
        photo_url = None
        if (
            hasattr(message.sender, "profile_picture")
            and message.sender.profile_picture
        ):
            try:
                photo_url = message.sender.profile_picture.url
                if not photo_url.startswith("http"):
                    backend_url = getattr(
                        settings, "BACKEND_URL", "http://localhost:8000"
                    ).rstrip("/")
                    photo_url = f"{backend_url}{photo_url}"
            except Exception as e:
                logger.error(f"Erreur photo profil: {e}")
                photo_url = None

        data = {
            "id": message.id,
            "sender": {
                "id": message.sender.id,
                "full_name": message.sender.full_name,
                "email": message.sender.email,
                "photo": photo_url,
            },
            "text": message.text,
            "created_at": message.created_at.isoformat(),
            "is_read": message.is_read,
        }

        # ✅ Média du message (CORRECTION: utiliser BACKEND_URL, pas WEBSOCKET_URL)
        if message.media:
            try:
                media_path = message.media.url

                if media_path.startswith("http"):
                    data["media_url"] = media_path
                else:
                    # ✅ BACKEND_URL pour HTTP, pas WEBSOCKET_URL
                    backend_url = getattr(
                        settings, "BACKEND_URL", "http://localhost:8000"
                    ).rstrip("/")
                    data["media_url"] = f"{backend_url}{media_path}"

                data["media_type"] = message.media_type

                logger.info(f"URL média construite: {data['media_url']}")

            except Exception as e:
                logger.error(f"Erreur construction URL média: {e}")

        return data

    def update_conversation(self, message):
        """Met à jour la conversation"""
        from app.notifications.models import Conversation

        try:
            if self.conversation_type == "group":
                conversation, _ = Conversation.objects.get_or_create(
                    trajet=message.trajet,
                    is_group=True,
                )
            else:
                conversation = None

                existing_conversations = Conversation.objects.filter(
                    is_group=False, participants=message.sender
                ).filter(participants=message.receiver)

                if existing_conversations.exists():
                    conversation = existing_conversations.first()
                else:
                    conversation = Conversation.objects.create(is_group=False)
                    conversation.participants.add(message.sender, message.receiver)

            conversation.last_message = message
            conversation.save()

            logger.info(f"Conversation mise à jour: {conversation.id}")

        except Exception as e:
            logger.error(f"Erreur update conversation: {e}", exc_info=True)
