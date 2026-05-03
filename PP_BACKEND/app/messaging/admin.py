# ============================================================================
# apps/messaging/admin.py - Administration de la messagerie
# ============================================================================

from django.contrib import admin

from app.messaging.models import Conversation, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sender",
        "receiver",
        "text_preview",
        "trajet",
        "is_read",
        "created_at",
    ]
    list_filter = ["is_read", "created_at"]
    search_fields = ["sender__email", "receiver__email", "text"]
    date_hierarchy = "created_at"

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    text_preview.short_description = "Message"


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "participants_list", "trajet", "last_activity"]
    list_filter = ["last_activity", "created_at"]
    date_hierarchy = "last_activity"

    def participants_list(self, obj):
        return ", ".join([u.email for u in obj.participants.all()])

    participants_list.short_description = "Participants"
