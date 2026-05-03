"""
Serializers pour la gestion des utilisateurs
"""

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from app.users.models import UserDocument as Document

from .models import Preference, Role, User


class RoleSerializer(serializers.ModelSerializer):
    """Serializer pour les rôles"""

    class Meta:
        db_table = "roles"
        model = Role
        fields = ["id", "name", "description"]


# Dans users/serializers.py - Ajouter à la fin du fichier


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer pour demander la réinitialisation du mot de passe"""

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Valide le format de l'email (ne révèle pas si l'email existe)"""
        return value.lower().strip()


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer pour réinitialiser le mot de passe"""

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    new_password_confirm = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        """Valide que les mots de passe correspondent"""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password": "Les mots de passe ne correspondent pas."}
            )
        return attrs


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializer pour les préférences avec support multilingue"""

    class Meta:
        model = Preference
        fields = ["id", "name_fr", "name_en", "category", "icon", "description"]
        read_only_fields = ["id"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour du profil utilisateur"""

    # Accepter une liste d'IDs de préférences
    preferences = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Preference.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
            "bio",
            "preferences",
        ]

    def update(self, instance, validated_data):
        # Gérer les préférences séparément
        preferences = validated_data.pop("preferences", None)

        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour les préférences si fournies
        if preferences is not None:
            instance.preferences.set(preferences)

        return instance


class UserDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour les documents utilisateurs"""

    class Meta:
        model = Document
        fields = [
            "id",
            "document_type",
            "file_path",
            "uploaded_at",
            "verified",
            "verified_by",
            "verified_at",
            "rejection_reason",
        ]
        read_only_fields = ["uploaded_at", "verified", "verified_by", "verified_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""

    role_detail = RoleSerializer(source="role", read_only=True)
    preferences_detail = PreferenceSerializer(
        source="preferences", many=True, read_only=True
    )
    documents = UserDocumentSerializer(many=True, read_only=True)

    # ✅ AJOUT : Retourner l'URL complète de la photo
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "phone_verified",
            "profile_picture",
            "bio",
            "role",
            "role_detail",
            "preferences",
            "preferences_detail",
            "documents",
            "trips_as_driver",
            "trips_as_passenger",
            "average_rating",
            "date_joined",
            "is_active",
            "is_staff",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "trips_as_driver",
            "trips_as_passenger",
            "average_rating",
            "is_active",
        ]
        extra_kwargs = {
            "email": {"required": True},
        }

    def get_profile_picture(self, obj):
        """Retourne l'URL complète de la photo de profil"""
        if obj.profile_picture:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False, allow_null=True
    )
    documents = UserDocumentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "documents",
        ]

    def validate(self, attrs):
        """Valide que les mots de passe correspondent"""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        """Crée un nouvel utilisateur"""
        validated_data.pop("password_confirm")

        # Obtenir le rôle ou créer USER par défaut
        role = validated_data.pop("role", None)
        if role is None:
            role, _ = Role.objects.get_or_create(
                name="USER", defaults={"description": "Utilisateur standard"}
            )

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            role=role,
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Valide que les nouveaux mots de passe correspondent"""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password": "Les nouveaux mots de passe ne correspondent pas."}
            )
        return attrs

    def validate_old_password(self, value):
        """Valide que l'ancien mot de passe est correct"""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le profil utilisateur"""

    role_detail = RoleSerializer(source="role", read_only=True)
    preferences_detail = PreferenceSerializer(
        source="preferences", many=True, read_only=True
    )
    documents = UserDocumentSerializer(many=True, read_only=True)

    # ✅ MODIFICATION : Retourner l'URL complète de la photo
    profile_picture = serializers.SerializerMethodField()

    # Statistiques supplémentaires
    total_trips = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "phone_verified",
            "profile_picture",
            "bio",
            "role",
            "role_detail",
            "preferences",
            "preferences_detail",
            "documents",
            "trips_as_driver",
            "trips_as_passenger",
            "average_rating",
            "total_trips",
            "date_joined",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["id", "email", "date_joined"]

    def get_profile_picture(self, obj):
        """Retourne l'URL complète de la photo de profil"""
        if obj.profile_picture:
            request = self.context.get("request")
            if request:
                # Retourne l'URL absolue (http://localhost:8000/media/profiles/...)
                return request.build_absolute_uri(obj.profile_picture.url)
            # Fallback : retourne juste le chemin relatif
            return obj.profile_picture.url
        return None

    def get_total_trips(self, obj):
        """Calcule le nombre total de trajets"""
        return obj.trips_as_driver + obj.trips_as_passenger


class SendEmailVerificationSerializer(serializers.Serializer):
    """Serializer pour l'envoi du code de vérification d'email"""

    pass  # Utilise l'utilisateur authentifié


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer pour la vérification d'email"""

    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        """Valide que le code contient uniquement des chiffres"""
        if not value.isdigit():
            raise serializers.ValidationError(
                "Le code doit contenir uniquement des chiffres"
            )
        return value


class SendPhoneVerificationSerializer(serializers.Serializer):
    """Serializer pour l'envoi du code de vérification de téléphone"""

    pass  # Utilise l'utilisateur authentifié


class VerifyPhoneSerializer(serializers.Serializer):
    """Serializer pour la vérification de téléphone"""

    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        """Valide que le code contient uniquement des chiffres"""
        if not value.isdigit():
            raise serializers.ValidationError(
                "Le code doit contenir uniquement des chiffres"
            )
        return value


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer pour renvoyer un code de vérification"""

    verification_type = serializers.ChoiceField(
        choices=["email", "phone"], required=True
    )
