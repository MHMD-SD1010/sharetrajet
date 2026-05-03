from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination standard pour les résultats.

    Utilise la pagination par numéro de page de Django REST Framework.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
