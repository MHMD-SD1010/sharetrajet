# app/messaging/serializers.py
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from app.notifications.models import Conversation, Message

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les utilisateurs"""

    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "photo"]

    def get_photo(self, obj):
        """Récupère l'URL de la photo de profil"""
        if obj.profile_picture:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            # Fallback si pas de request
            photo_url = obj.profile_picture.url
            if not photo_url.startswith("http"):
                backend_url = getattr(
                    settings, "BACKEND_URL", "http://localhost:8000"
                ).rstrip("/")
                return f"{backend_url}{photo_url}"
            return photo_url
        return None


class MessageSerializer(serializers.ModelSerializer):
    """Serializer pour les messages"""

    sender = UserMinimalSerializer(read_only=True)
    receiver = UserMinimalSerializer(read_only=True)
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "trajet",
            "text",
            "media",
            "media_url",
            "media_type",
            "is_group_message",
            "is_read",
            "created_at",
            "read_at",
        ]
        read_only_fields = ["sender", "created_at"]

    def get_media_url(self, obj):
        """✅ Construit l'URL complète du média"""
        if not obj.media:
            return None

        try:
            # Récupérer l'URL du fichier
            media_path = obj.media.url

            # Si c'est déjà une URL complète, la retourner telle quelle
            if media_path.startswith("http"):
                return media_path

            # Sinon, construire l'URL complète
            request = self.context.get("request")
            if request:
                # Utiliser build_absolute_uri pour construire l'URL complète
                return request.build_absolute_uri(media_path)
            else:
                # Fallback: construire manuellement avec BACKEND_URL
                backend_url = getattr(settings, "BACKEND_URL", "http://localhost:8000")
                # Retirer le slash final si présent
                backend_url = backend_url.rstrip("/")
                # media_path commence déjà par /media/
                return f"{backend_url}{media_path}"

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"❌ Erreur construction media_url: {e}")
            return None


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer pour les conversations"""

    participants = UserMinimalSerializer(many=True, read_only=True)
    trajet = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "is_group",
            "trajet",
            "participants",
            "last_message",
            "last_activity",
            "unread_count",
            "created_at",
        ]

    def _combine_date_time(self, trajet):
        """Combine les champs date et heure_depart en un datetime ISO"""
        try:
            if trajet.date and trajet.heure_depart:
                combined = datetime.combine(trajet.date, trajet.heure_depart)
                return combined.isoformat()
            elif trajet.date:
                return trajet.date.isoformat()
            return None
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Erreur combinaison date/heure pour trajet {trajet.id}: {e}")
            return None

    def _get_user_photo_url(self, user):
        """Helper pour obtenir l'URL de la photo d'un utilisateur"""
        if user.profile_picture:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(user.profile_picture.url)
            # Fallback
            photo_url = user.profile_picture.url
            if not photo_url.startswith("http"):
                backend_url = getattr(
                    settings, "BACKEND_URL", "http://localhost:8000"
                ).rstrip("/")
                return f"{backend_url}{photo_url}"
            return photo_url
        return None

    def _build_media_url(self, media_file):
        """✅ NOUVEAU: Helper centralisé pour construire les URLs média"""
        if not media_file:
            return None

        try:
            media_path = media_file.url

            # Si déjà une URL complète
            if media_path.startswith("http"):
                return media_path

            # Construire l'URL complète
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(media_path)
            else:
                # Fallback
                backend_url = getattr(
                    settings, "BACKEND_URL", "http://localhost:8000"
                ).rstrip("/")
                return f"{backend_url}{media_path}"
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"❌ Erreur construction media_url: {e}")
            return None

    def get_trajet(self, obj):
        """Retourne les infos du trajet si conversation de groupe"""
        if obj.is_group and obj.trajet:
            try:
                return {
                    "id": obj.trajet.id,
                    "ville_depart": obj.trajet.ville_depart,
                    "ville_arrivee": obj.trajet.ville_arrivee,
                    "date_depart": self._combine_date_time(obj.trajet),
                    "date": str(obj.trajet.date) if obj.trajet.date else None,
                    "heure_depart": (
                        str(obj.trajet.heure_depart)
                        if obj.trajet.heure_depart
                        else None
                    ),
                    "conducteur": {
                        "id": obj.trajet.conducteur.id,
                        "full_name": obj.trajet.conducteur.full_name,
                        "email": obj.trajet.conducteur.email,
                        "photo": self._get_user_photo_url(obj.trajet.conducteur),
                    },
                }
            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.error(f"Erreur sérialisation trajet {obj.trajet.id}: {e}")

                return {
                    "id": obj.trajet.id,
                    "ville_depart": getattr(obj.trajet, "ville_depart", "N/A"),
                    "ville_arrivee": getattr(obj.trajet, "ville_arrivee", "N/A"),
                    "date_depart": None,
                    "conducteur": {
                        "id": obj.trajet.conducteur.id,
                        "full_name": obj.trajet.conducteur.full_name,
                        "email": obj.trajet.conducteur.email,
                        "photo": None,
                    },
                }
        return None

    def get_last_message(self, obj):
        """✅ Retourne le dernier message avec l'URL du média"""
        try:
            if obj.is_group and obj.trajet:
                last_msg = (
                    Message.objects.filter(trajet=obj.trajet, is_group_message=True)
                    .select_related("sender")
                    .order_by("-created_at")
                    .first()
                )
            else:
                participants = obj.participants.all()
                if participants.count() < 2:
                    return None

                last_msg = (
                    Message.objects.filter(
                        sender__in=participants,
                        receiver__in=participants,
                        is_group_message=False,
                    )
                    .select_related("sender")
                    .order_by("-created_at")
                    .first()
                )

            if last_msg:
                message_data = {
                    "text": last_msg.text,
                    "created_at": last_msg.created_at.isoformat(),
                    "sender": {
                        "id": last_msg.sender.id,
                        "full_name": last_msg.sender.full_name,
                    },
                }

                # ✅ Ajouter le média si présent (utiliser la méthode centralisée)
                if last_msg.media:
                    message_data["media_url"] = self._build_media_url(last_msg.media)
                    message_data["media_type"] = last_msg.media_type

                return message_data

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Erreur récupération dernier message: {e}")

        return None

    def get_unread_count(self, obj):
        """Retourne le nombre de messages non lus"""
        try:
            request = self.context.get("request")
            if not request or not request.user.is_authenticated:
                return 0

            return obj.get_unread_count(request.user)
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Erreur calcul messages non lus: {e}")
            return 0
