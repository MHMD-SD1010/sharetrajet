import django_filters

from app.trajets.models import Trajet


class TrajetFilter(django_filters.FilterSet):
    """Filtre pour le modèle Trajet"""

    class Meta:
        model = Trajet
        fields = ["ville_depart", "ville_arrivee", "date", "conducteur", "status"]
