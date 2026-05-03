import logging

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour DRF
    """
    # Appeler le gestionnaire par défaut
    response = exception_handler(exc, context)

    if response is not None:
        # Personnaliser la réponse d'erreur
        custom_response_data = {
            "error": True,
            "status_code": response.status_code,
            "message": "Une erreur est survenue",
            "details": response.data,
        }

        # Logger l'erreur
        logger.error(
            f"API Error: {exc.__class__.__name__} - {str(exc)}",
            extra={
                "status_code": response.status_code,
                "path": context["request"].path,
                "method": context["request"].method,
            },
        )

        response.data = custom_response_data
    else:
        # Erreur non gérée par DRF
        logger.exception(f"Unhandled exception: {exc}")

        response = Response(
            {
                "error": True,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Erreur serveur interne",
                "details": str(exc) if settings.DEBUG else "Une erreur est survenue",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
