# ============================================================================
# apps/reservations/admin.py - Administration des réservations
# ============================================================================

from django.contrib import admin
from django.utils.html import format_html

from app.reservations.models import Rating, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "trajet_info",
        "passager",
        "nbr_places",
        "status_badge",
        "total_price",
        "created_at",
    ]
    list_filter = ["status", "created_at", "approved_at"]
    search_fields = [
        "passager__email",
        "trajet__ville_depart",
        "trajet__ville_arrivee",
        "trajet__conducteur__email",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        ("Réservation", {"fields": ("trajet", "passager", "nbr_places")}),
        ("Tarification", {"fields": ("price_per_seat", "total_price")}),
        ("Statut", {"fields": ("status", "rejection_reason", "cancellation_reason")}),
        ("Dates", {"fields": ("created_at", "approved_at", "cancelled_at")}),
    )

    readonly_fields = [
        "created_at",
        "approved_at",
        "cancelled_at",
        "price_per_seat",
        "total_price",
    ]

    def trajet_info(self, obj):
        return f"{obj.trajet.ville_depart} → {obj.trajet.ville_arrivee} ({obj.trajet.date})"

    trajet_info.short_description = "Trajet"

    def status_badge(self, obj):
        colors = {
            "PENDING": "orange",
            "CONFIRMED": "green",
            "REJECTED": "red",
            "CANCELLED": "gray",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Statut"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["rater", "rated", "note", "stars_display", "created_at"]
    list_filter = ["note", "created_at"]
    search_fields = ["rater__email", "rated__email", "comment"]
    date_hierarchy = "created_at"

    def stars_display(self, obj):
        stars = "⭐" * obj.note
        return format_html('<span style="font-size: 16px;">{}</span>', stars)

    stars_display.short_description = "Étoiles"
