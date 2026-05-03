# app/trajets/urls.py

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import FuelPriceViewSet, TrajetViewSet

router = DefaultRouter()

# ✅ Trajets sur le préfixe racine
router.register(r"", TrajetViewSet, basename="trajet")
router.register(r"fuel-prices", FuelPriceViewSet, basename="fuel-price")

app_name = "trajets"

urlpatterns = [
    path("", include(router.urls)),
]

# URLs générées :
# ========== TRAJETS ==========
# GET    /api/v1/trajets/
# POST   /api/v1/trajets/
# GET    /api/v1/trajets/{id}/
# PUT    /api/v1/trajets/{id}/
# DELETE /api/v1/trajets/{id}/
# POST   /api/v1/trajets/search/              ✅ RECHERCHE SIMPLE
# POST   /api/v1/trajets/intelligent_search/  ✅ RECHERCHE INTELLIGENTE
# GET    /api/v1/trajets/my_trips/
# GET    /api/v1/trajets/upcoming/
# GET    /api/v1/trajets/past/
# POST   /api/v1/trajets/{id}/cancel/
# GET    /api/v1/trajets/{id}/reservations/
# GET    /api/v1/trajets/{id}/statistics/

# ========== FUEL PRICES ==========
# GET    /api/v1/trajets/fuel-prices/
# POST   /api/v1/trajets/fuel-prices/
