"""
apps/users/admin.py - Administration des utilisateurs
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Preference, RefreshToken, Role, User, UserDocument


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration personnalisée pour les utilisateurs"""

    list_display = [
        "email",
        "full_name",
        "phone_number",
        "role",
        "is_active",
        "average_rating",
        "total_trips",
        "date_joined",
    ]
    list_filter = ["is_active", "is_staff", "role", "date_joined"]
    search_fields = ["email", "first_name", "last_name", "phone_number"]
    ordering = ["-date_joined"]

    fieldsets = (
        ("Informations de connexion", {"fields": ("email", "password")}),
        (
            "Informations personnelles",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "phone_verified",
                    "profile_picture",
                    "bio",
                )
            },
        ),
        ("Rôle et préférences", {"fields": ("role", "preferences")}),
        (
            "Statistiques",
            {"fields": ("trips_as_driver", "trips_as_passenger", "average_rating")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates importantes", {"fields": ("date_joined", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    readonly_fields = [
        "date_joined",
        "updated_at",
        "trips_as_driver",
        "trips_as_passenger",
        "average_rating",
    ]

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = "Nom complet"

    def total_trips(self, obj):
        return obj.trips_as_driver + obj.trips_as_passenger

    total_trips.short_description = "Trajets totaux"

    actions = ["activate_users", "deactivate_users", "verify_phone"]

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s)")

    activate_users.short_description = "Activer les utilisateurs sélectionnés"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s)")

    deactivate_users.short_description = "Désactiver les utilisateurs sélectionnés"

    def verify_phone(self, request, queryset):
        updated = queryset.update(phone_verified=True)
        self.message_user(request, f"{updated} téléphone(s) vérifié(s)")

    verify_phone.short_description = "Vérifier les téléphones"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "user_count"]
    search_fields = ["name"]

    def user_count(self, obj):
        return obj.users.count()

    user_count.short_description = "Nombre d'utilisateurs"


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "user_count"]
    search_fields = ["name"]

    def user_count(self, obj):
        return obj.users.count()

    user_count.short_description = "Nombre d'utilisateurs"


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "document_type",
        "uploaded_at",
        "verified_status",
        "verified_by",
        "verified_at",
    ]
    list_filter = ["document_type", "verified", "uploaded_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    date_hierarchy = "uploaded_at"

    def verified_status(self, obj):
        if obj.verified:
            return format_html('<span style="color: green;">✓ Vérifié</span>')
        return format_html('<span style="color: red;">✗ Non vérifié</span>')

    verified_status.short_description = "Statut"

    actions = ["verify_documents", "reject_documents"]

    def verify_documents(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(
            verified=True, verified_by=request.user, verified_at=timezone.now()
        )
        self.message_user(request, f"{updated} document(s) vérifié(s)")

    verify_documents.short_description = "Vérifier les documents"

    def reject_documents(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f"{updated} document(s) rejeté(s)")

    reject_documents.short_description = "Rejeter les documents"


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "expires_at", "revoked", "is_valid_display"]
    list_filter = ["revoked", "created_at", "expires_at"]
    search_fields = ["user__email"]
    date_hierarchy = "created_at"

    def is_valid_display(self, obj):
        if obj.is_valid():
            return format_html('<span style="color: green;">✓ Valide</span>')
        return format_html('<span style="color: red;">✗ Expiré/Révoqué</span>')

    is_valid_display.short_description = "Validité"
