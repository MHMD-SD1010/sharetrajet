from rest_framework import permissions


class IsMessageParticipant(permissions.BasePermission):
    """
    Permission pour les messages: expéditeur ou destinataire
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission pour les conversations: doit être participant
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
