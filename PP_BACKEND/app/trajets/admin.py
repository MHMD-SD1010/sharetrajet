# ============================================================================
# apps/trajets/admin.py - Administration des trajets
# ============================================================================

from django.contrib import admin
from django.utils.html import format_html

from app.trajets.models import FuelPrice, Trajet, TrajetEtape


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "route",
        "conducteur",
        "date",
        "heure_depart",
        "places_info",
        "price",
        "status_badge",
        "created_at",
    ]
    list_filter = ["status", "is_confort", "pause_required", "date", "created_at"]
    search_fields = [
        "conducteur__email",
        "conducteur__first_name",
        "conducteur__last_name",
        "ville_depart",
        "ville_arrivee",
    ]
    date_hierarchy = "date"
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Informations du trajet",
            {
                "fields": (
                    "conducteur",
                    "ville_depart",
                    "ville_arrivee",
                    "adresse_depart",
                    "adresse_arrivee",
                    "date",
                    "heure_depart",
                )
            },
        ),
        ("Capacité", {"fields": ("nbr_places", "places_disponibles")}),
        (
            "Tarification",
            {"fields": ("price", "price_platform", "price_driver", "suggested_price")},
        ),
        (
            "Options",
            {
                "fields": (
                    "distance",
                    "is_confort",
                    "pause_required",
                    "luggage_allowed",
                    "description",
                )
            },
        ),
        ("Statut", {"fields": ("status",)}),
    )

    readonly_fields = [
        "price_platform",
        "price_driver",
        "places_disponibles",
        "pause_required",
        "suggested_price",
    ]

    def route(self, obj):
        return f"{obj.ville_depart} → {obj.ville_arrivee}"

    route.short_description = "Trajet"

    def places_info(self, obj):
        return f"{obj.places_disponibles}/{obj.nbr_places}"

    places_info.short_description = "Places"

    def status_badge(self, obj):
        colors = {"ACTIVE": "green", "COMPLETED": "blue", "CANCELLED": "red"}
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Statut"

    actions = ["cancel_trajets", "complete_trajets"]

    def cancel_trajets(self, request, queryset):
        updated = queryset.filter(status="ACTIVE").update(status="CANCELLED")
        self.message_user(request, f"{updated} trajet(s) annulé(s)")

    cancel_trajets.short_description = "Annuler les trajets"

    def complete_trajets(self, request, queryset):
        updated = queryset.filter(status="ACTIVE").update(status="COMPLETED")
        self.message_user(request, f"{updated} trajet(s) terminé(s)")

    complete_trajets.short_description = "Marquer comme terminés"


@admin.register(TrajetEtape)
class TrajetEtapeAdmin(admin.ModelAdmin):
    list_display = ["trajet", "ordre", "ville", "heure_arrivee"]
    list_filter = ["trajet__date"]
    search_fields = ["trajet__ville_depart", "trajet__ville_arrivee", "ville"]


@admin.register(FuelPrice)
class FuelPriceAdmin(admin.ModelAdmin):
    # Vérifiez les vrais noms de champs dans votre modèle FuelPrice
    list_display = [
        "fuel_type",
        "price_per_liter",
        "effective_date",
    ]  # Retirez 'wilaya' si n'existe pas
    list_filter = ["fuel_type", "effective_date"]  # Retirez 'wilaya' si n'existe pas
    search_fields = ["fuel_type"]  # Changez selon vos besoins
    date_hierarchy = "effective_date"
