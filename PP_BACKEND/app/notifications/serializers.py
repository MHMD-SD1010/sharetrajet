from rest_framework import serializers

from app.users.serializers import UserSerializer

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications"""

    sender_detail = UserSerializer(source="sender", read_only=True)
    related_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "sender",
            "sender_detail",
            "type",
            "content",
            "related_model",
            "related_id",
            "related_object",
            "is_read",
            "created_at",
            "read_at",
        ]
        read_only_fields = [
            "id",
            "recipient",
            "sender",
            "is_read",
            "created_at",
            "read_at",
        ]

    def get_related_object(self, obj):
        """Récupère l'objet lié à la notification"""
        related = obj.get_related_object()
        if not related:
            return None

        # Retourner une représentation simple de l'objet
        return {
            "type": obj.related_model,
            "id": obj.related_id,
            "summary": str(related),
        }
