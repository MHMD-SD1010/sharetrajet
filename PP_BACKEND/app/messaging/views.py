"""
ViewSet pour la messagerie avec support WebSocket
"""

import base64
import logging
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Q

from channels.layers import get_channel_layer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from app.notifications.models import Conversation, Message

from .serializers import ConversationSerializer, MessageSerializer

logger = logging.getLogger(__name__)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des messages"""

    queryset = Message.objects.select_related("sender", "receiver", "trajet").all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtre les messages selon l'utilisateur"""
        user = self.request.user
        return self.queryset.filter(
            Q(sender=user) | Q(receiver=user) | Q(trajet__conducteur=user)
        ).order_by("-created_at")

    def perform_create(self, serializer):
        """Crée un message avec l'expéditeur automatique"""
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=["get"])
    def conversation(self, request):
        """Récupère la conversation avec un utilisateur spécifique"""
        other_user_id = request.query_params.get("user_id")
        trajet_id = request.query_params.get("trajet_id")

        if not other_user_id:
            return Response(
                {"error": "user_id requis"}, status=status.HTTP_400_BAD_REQUEST
            )

        messages = self.queryset.filter(
            Q(sender=request.user, receiver_id=other_user_id)
            | Q(sender_id=other_user_id, receiver=request.user)
        )

        if trajet_id:
            messages = messages.filter(trajet_id=trajet_id)

        messages = messages.order_by("created_at")

        # Marquer comme lus les messages reçus
        messages.filter(receiver=request.user, is_read=False).update(is_read=True)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="trip-group/(?P<trajet_id>[^/.]+)")
    def trip_group_messages(self, request, trajet_id=None):
        """
        Récupère les messages de groupe d'un trajet + URL WebSocket
        GET /api/v1/messages/trip-group/{trajet_id}/
        """
        from app.reservations.models import Reservation
        from app.trajets.models import Trajet

        # Vérifier que le trajet existe
        try:
            trajet = Trajet.objects.get(id=trajet_id)
        except Trajet.DoesNotExist:
            return Response(
                {"error": "Trajet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier permission
        is_driver = trajet.conducteur == request.user
        has_reservation = Reservation.objects.filter(
            trajet_id=trajet_id, passager=request.user, status="CONFIRMED"
        ).exists()

        if not is_driver and not has_reservation:
            return Response(
                {
                    "error": "Accès non autorisé",
                    "message": (
                        "Vous devez avoir une réservation confirmée",
                        "pour accéder à ce groupe",
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Récupérer les messages de groupe
        messages = (
            Message.objects.filter(trajet_id=trajet_id, is_group_message=True)
            .select_related("sender")
            .order_by("created_at")
        )

        serializer = self.get_serializer(messages, many=True)

        # Générer l'URL WebSocket
        websocket_url = f"{settings.WEBSOCKET_URL}/ws/chat/group/{trajet_id}/"

        return Response(
            {
                "trajet_id": trajet_id,
                "trajet": {
                    "id": trajet.id,
                    "ville_depart": trajet.ville_depart,
                    "ville_arrivee": trajet.ville_arrivee,
                    "date_depart": trajet.date_depart,
                    "conducteur": {
                        "id": trajet.conducteur.id,
                        "full_name": trajet.conducteur.full_name,
                        "photo": (
                            trajet.conducteur.photo.url
                            if trajet.conducteur.photo
                            else None
                        ),
                    },
                },
                "messages": serializer.data,
                "websocket_url": websocket_url,
                "is_driver": is_driver,
            }
        )

    @action(detail=False, methods=["get"], url_path="private/(?P<other_user_id>[^/.]+)")
    def private_messages(self, request, other_user_id=None):
        """
        Récupère les messages privés avec un utilisateur + URL WebSocket
        GET /api/v1/messages/private/{other_user_id}/
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # Vérifier que l'autre utilisateur existe
        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        # Récupérer les messages privés
        messages = (
            Message.objects.filter(
                Q(sender=request.user, receiver=other_user)
                | Q(sender=other_user, receiver=request.user),
                is_group_message=False,
            )
            .select_related("sender", "receiver")
            .order_by("created_at")
        )

        # Marquer comme lus
        messages.filter(receiver=request.user, is_read=False).update(is_read=True)

        serializer = self.get_serializer(messages, many=True)

        # Générer l'ID de conversation (IDs triés)
        user_ids = sorted([request.user.id, int(other_user_id)])
        conversation_id = f"{user_ids[0]}_{user_ids[1]}"

        # URL WebSocket
        websocket_url = f"{settings.WEBSOCKET_URL}/ws/chat/private/{conversation_id}/"

        return Response(
            {
                "conversation_id": conversation_id,
                "other_user": {
                    "id": other_user.id,
                    "full_name": other_user.full_name,
                    "email": other_user.email,
                    "photo": other_user.photo.url if other_user.photo else None,
                },
                "messages": serializer.data,
                "websocket_url": websocket_url,
            }
        )

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Compte les messages non lus"""
        count = self.queryset.filter(receiver=request.user, is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        """Marque un message comme lu"""
        message = self.get_object()

        if message.receiver != request.user:
            return Response(
                {"error": "Vous ne pouvez marquer que vos propres messages"},
                status=status.HTTP_403_FORBIDDEN,
            )

        message.mark_as_read()
        return Response({"message": "Message marqué comme lu"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Marque tous les messages comme lus"""
        user_id = request.data.get("user_id")
        messages = self.queryset.filter(receiver=request.user, is_read=False)

        if user_id:
            messages = messages.filter(sender_id=user_id)

        count = messages.update(is_read=True)
        return Response({"message": f"{count} messages marqués comme lus"})

    @action(detail=False, methods=["post"], url_path="upload-media")
    def upload_media(self, request):
        try:
            # Validate and extract request data
            validation_error = self._validate_upload_request(request)
            if validation_error:
                return validation_error

            # Prepare message data
            message_data = self._prepare_message_data(request)
            if isinstance(message_data, Response):  # Error response
                return message_data

            # Create the message
            from app.notifications.models import Message

            message = Message.objects.create(**message_data)

            # Update conversation
            conversation_type = request.data.get("conversation_type")
            self._update_conversation(message, conversation_type)

            # Return response
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Erreur upload media: {e}", exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validate_upload_request(self, request):
        """Validate basic request parameters."""
        conversation_type = request.data.get("conversation_type")
        conversation_id = request.data.get("conversation_id")
        text = request.data.get("text", "").strip()
        media_base64 = request.data.get("media")

        if not conversation_type or not conversation_id:
            return Response(
                {"error": "conversation_type et conversation_id requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not text and not media_base64:
            return Response(
                {"error": "Message vide"}, status=status.HTTP_400_BAD_REQUEST
            )

        return None

    def _prepare_message_data(self, request):
        """Prepare message data including media file and conversation details."""
        text = request.data.get("text", "").strip()
        media_base64 = request.data.get("media")
        conversation_type = request.data.get("conversation_type")
        conversation_id = request.data.get("conversation_id")

        message_data = {
            "sender": request.user,
            "text": text,
        }

        # Process media file if present
        if media_base64:
            media_error = self._process_media_file(request, message_data)
            if media_error:
                return media_error

        # Add conversation-specific data
        conversation_error = self._add_conversation_data(
            request, message_data, conversation_type, conversation_id
        )
        if conversation_error:
            return conversation_error

        return message_data

    def _process_media_file(self, request, message_data):
        """Process and attach media file to message data."""
        try:
            media_base64 = request.data.get("media")
            media_type = request.data.get("media_type")
            media_name = request.data.get("media_name", "file")

            # Remove data URL prefix if present
            if "," in media_base64:
                media_base64 = media_base64.split(",")[1]

            # Decode base64
            file_data = base64.b64decode(media_base64)

            # Generate unique filename
            file_extension = media_name.split(".")[-1] if "." in media_name else "jpg"
            unique_filename = f"{uuid.uuid4()}.{file_extension}"

            # Create ContentFile
            media_file = ContentFile(file_data, name=unique_filename)
            message_data["media"] = media_file
            message_data["media_type"] = media_type

            logger.info(
                f"📎 Fichier uploadé: {unique_filename} ({len(file_data)} bytes)"
            )
            return None

        except Exception as e:
            logger.error(f"❌ Erreur décodage fichier: {e}")
            return Response(
                {"error": "Erreur lors du traitement du fichier"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _add_conversation_data(
        self, request, message_data, conversation_type, conversation_id
    ):
        """Add conversation-specific data based on conversation type."""
        if conversation_type == "group":
            return self._add_group_conversation_data(
                request, message_data, conversation_id
            )
        elif conversation_type == "private":
            return self._add_private_conversation_data(
                request, message_data, conversation_id
            )
        else:
            return Response(
                {"error": "Type de conversation invalide"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _add_group_conversation_data(self, request, message_data, conversation_id):
        """Add group conversation data (trajet)."""
        from app.reservations.models import Reservation
        from app.trajets.models import Trajet

        try:
            trajet_id = int(conversation_id)
            trajet = Trajet.objects.get(id=trajet_id)

            # Check permissions
            is_driver = trajet.conducteur == request.user
            has_reservation = Reservation.objects.filter(
                trajet_id=trajet_id, passager=request.user, status="CONFIRMED"
            ).exists()

            if not is_driver and not has_reservation:
                return Response(
                    {"error": "Accès non autorisé"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            message_data["trajet"] = trajet
            message_data["is_group_message"] = True
            message_data["receiver"] = None
            return None

        except (Trajet.DoesNotExist, ValueError):
            return Response(
                {"error": "Trajet non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

    def _add_private_conversation_data(self, request, message_data, conversation_id):
        """Add private conversation data (receiver)."""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            user_ids = [int(uid) for uid in conversation_id.split("_")]
            if request.user.id not in user_ids:
                return Response(
                    {"error": "Accès non autorisé"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            other_user_id = [uid for uid in user_ids if uid != request.user.id][0]
            receiver = User.objects.get(id=other_user_id)

            message_data["receiver"] = receiver
            message_data["is_group_message"] = False
            return None

        except (User.DoesNotExist, ValueError, IndexError):
            return Response(
                {"error": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def _update_conversation(self, message, conversation_type):
        """Méthode helper pour mettre à jour la conversation"""
        from app.notifications.models import Conversation

        try:
            if conversation_type == "group":
                conversation, _ = Conversation.objects.get_or_create(
                    trajet=message.trajet,
                    is_group=True,
                )
            else:
                conversation, created = Conversation.objects.get_or_create(
                    is_group=False,
                )
                if (
                    created
                    or not conversation.participants.filter(
                        id=message.sender.id
                    ).exists()
                ):
                    conversation.participants.add(message.sender)
                if message.receiver:
                    conversation.participants.add(message.receiver)

            conversation.last_message = message
            conversation.save()

        except Exception as e:
            logger.error(f"❌ Erreur update conversation: {e}")


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour la gestion des conversations"""

    queryset = Conversation.objects.prefetch_related("participants").all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtre les conversations de l'utilisateur"""
        return self.queryset.filter(participants=self.request.user).order_by(
            "-last_activity"
        )

    @action(detail=False, methods=["get"])
    def my_groups(self, request):
        """
        Liste les conversations de groupe de l'utilisateur
        GET /api/v1/conversations/my-groups/
        """
        groups = self.queryset.filter(
            participants=request.user, is_group=True
        ).select_related("trajet", "trajet__conducteur")

        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """Récupère les messages d'une conversation"""
        conversation = self.get_object()

        messages = Message.objects.filter(
            Q(sender__in=conversation.participants.all())
            & Q(receiver__in=conversation.participants.all())
        )

        if conversation.trajet:
            messages = messages.filter(trajet=conversation.trajet)

        messages = messages.order_by("-created_at")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def get_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by(
        "created_at"
    )
    serializer = MessageSerializer(messages, many=True, context={"request": request})
    return Response(serializer.data)


channel_layer = get_channel_layer()
