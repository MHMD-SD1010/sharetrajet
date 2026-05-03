from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PreferenceViewSet, RoleViewSet, UserViewSet

# ✅ Créer des routeurs SÉPARÉS pour éviter les conflits
user_router = DefaultRouter()
user_router.register(r"", UserViewSet, basename="user")

role_router = DefaultRouter()
role_router.register(r"", RoleViewSet, basename="role")

preference_router = DefaultRouter()
preference_router.register(r"", PreferenceViewSet, basename="preference")

app_name = "users"

urlpatterns = [
    # JWT Token refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ✅ Routes spécifiques AVANT les routes génériques
    path("roles/", include(role_router.urls)),
    path("preferences/", include(preference_router.urls)),
    # Routes utilisateurs (en dernier pour éviter les conflits)
    path("", include(user_router.urls)),
]

# URLs générées :
# ========== AUTHENTIFICATION ==========
# POST   /api/v1/users/register/
# POST   /api/v1/users/login/
# POST   /api/v1/users/google_auth/
# GET    /api/v1/users/me/

# ========== PRÉFÉRENCES ==========
# GET    /api/v1/users/preferences/           ✅ Liste toutes les préférences (PUBLIC)
# GET    /api/v1/users/preferences/{id}/      ✅ Détail d'une préférence (PUBLIC)
# GET    /api/v1/users/my_preferences/        ✅ Préférences de l'utilisateur connecté
# POST   /api/v1/users/preferences/           ✅ Mettre à jour les préférences
# ========== VÉRIFICATIONS ==========
# POST   /api/v1/users/send_email_verification/
# POST   /api/v1/users/verify_email/
# POST   /api/v1/users/send_phone_verification/
# POST   /api/v1/users/verify_phone/
# GET    /api/v1/users/verification_status/
# ========== DOCUMENTS ==========
# POST   /api/v1/users/upload_document/
# GET    /api/v1/users/documents/
# GET    /api/v1/users/check-document-status/

# ========== RÔLES ==========
# GET    /api/v1/users/roles/
# GET    /api/v1/users/roles/{id}/
