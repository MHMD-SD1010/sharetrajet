# ============================================================================
# apps/notifications/admin.py - Administration des notifications
# ============================================================================

from django.contrib import admin

from app.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "recipient",
        "type",
        "content_preview",
        "is_read",
        "created_at",
    ]
    list_filter = ["type", "is_read", "created_at"]
    search_fields = ["recipient__email", "content"]
    date_hierarchy = "created_at"

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Contenu"

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marquée(s) comme lue(s)")

    mark_as_read.short_description = "Marquer comme lues"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(
            request, f"{updated} notification(s) marquée(s) comme non lues"
        )

    mark_as_unread.short_description = "Marquer comme non lues"
