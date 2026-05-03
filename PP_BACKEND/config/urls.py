from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

admin.site.site_header = "DZ-CarPool Administration"
admin.site.site_title = "DZ-CarPool Admin"
admin.site.index_title = "Bienvenue sur le panneau d'administration DZ-CarPool"

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Health check endpoint
    path("health/", lambda request: JsonResponse({"status": "healthy"})),
    # API v1 - Toutes vos apps
    path("api/v1/users/", include("app.users.urls")),
    path("api/v1/trajets/", include("app.trajets.urls")),
    path("api/v1/reservations/", include("app.reservations.urls")),
    path("api/v1/messaging/", include("app.messaging.urls")),
    path("api/v1/notifications/", include("app.notifications.urls")),
    # Allauth URLs (pour Google Auth)
    path("accounts/", include("allauth.urls")),
]
# ✅ SUPPRIMÉ : la ligne en doublon qui était ici

# ✅ Servir les fichiers média et statiques uniquement en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
