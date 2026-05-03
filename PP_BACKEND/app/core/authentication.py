from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    ✅ CORRECTION : Ne pas forcer l'authentification
    """

    def authenticate(self, request):
        """
        Override pour permettre les requêtes sans token
        """
        # ✅ Si pas de header Authorization, retourner None (pas d'erreur)
        header = self.get_header(request)

        if header is None:
            # ✅ IMPORTANT : Retourner None au lieu de lever une exception
            return None

        # Si un header existe, valider le token
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validation normale du token
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
