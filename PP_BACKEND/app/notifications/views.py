from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour la gestion des notifications"""

    queryset = Notification.objects.select_related("recipient", "sender").all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtre les notifications de l'utilisateur"""
        return self.queryset.filter(recipient=self.request.user).order_by("-created_at")

    @action(detail=False, methods=["get"])
    def unread(self, request):
        """Liste les notifications non lues"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Compte les notifications non lues"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        """Marque une notification comme lue"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({"message": "Notification marquée comme lue"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Marque toutes les notifications comme lues"""
        count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"message": f"{count} notifications marquées comme lues"})

    @action(detail=False, methods=["delete"])
    def clear_all(self, request):
        """Supprime toutes les notifications lues"""
        count = self.get_queryset().filter(is_read=True).delete()[0]
        return Response({"message": f"{count} notifications supprimées"})

    @action(detail=False, methods=["get"])
    def by_type(self, request):
        """Filtre les notifications par type"""
        notif_type = request.query_params.get("type")

        if not notif_type:
            return Response(
                {"error": "Type de notification requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notifications = self.get_queryset().filter(type=notif_type)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
