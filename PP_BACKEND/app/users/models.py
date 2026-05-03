"""
Modèles pour la gestion des utilisateurs du projet DZ-CarPool
"""

import random
import secrets
import string
from datetime import timedelta

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class Role(models.Model):
    """Modèle pour les rôles utilisateurs"""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "roles"
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

    def __str__(self):
        return self.name


class Preference(models.Model):
    """Modèle pour les préférences de trajet avec support multilingue"""

    CATEGORY_CHOICES = [
        ("interests", "Centres d'intérêt"),
        ("habits", "Habitudes"),
        ("driving", "Préférences de conduite"),
    ]

    name = models.CharField(
        max_length=100, unique=True
    )  # Garde pour compatibilité (sera name_fr)
    description = models.TextField(blank=True)

    # Nouveaux champs pour le multilingue
    name_fr = models.CharField(max_length=100, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="interests"
    )
    icon = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "preferences"
        verbose_name = "Préférence"
        verbose_name_plural = "Préférences"
        ordering = ["category", "id"]

    def __str__(self):
        return self.name_fr or self.name

    def save(self, *args, **kwargs):
        # Synchroniser name avec name_fr pour compatibilité
        if self.name_fr and not self.name:
            self.name = self.name_fr
        elif not self.name_fr and self.name:
            self.name_fr = self.name
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    """Manager personnalisé pour le modèle User"""

    def create_user(self, email, password=None, **extra_fields):
        """Crée et sauvegarde un utilisateur"""
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crée et sauvegarde un superutilisateur"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé pour DZ-CarPool"""

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    bio = models.TextField(max_length=500, blank=True)

    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    preferences = models.ManyToManyField(Preference, blank=True, related_name="users")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Statistiques
    trips_as_driver = models.IntegerField(default=0)
    trips_as_passenger = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["date_joined"]),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def update_statistics(self):
        """
        ✅ Met à jour les statistiques de l'utilisateur
        Calcule la moyenne des notes reçues
        """
        from app.reservations.models import Rating

        # Calculer la moyenne des notes reçues
        avg_rating = Rating.objects.filter(rated=self).aggregate(Avg("note"))[
            "note__avg"
        ]

        # Mettre à jour le champ rating (si vous avez ce champ)
        if hasattr(self, "rating"):
            self.rating = round(avg_rating, 1) if avg_rating else 5.0
            self.save(update_fields=["rating"])

        return avg_rating


class UserDocument(models.Model):
    """Modèle pour la gestion des documents utilisateurs"""

    DOCUMENT_TYPES = [
        ("CNI", "Carte Nationale d'Identité"),
        ("PERMIS", "Permis de Conduire"),
        ("AUTRE", "Autre Document"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file_path = models.FileField(
        upload_to="documents/",
        validators=[FileExtensionValidator(["pdf", "jpg", "jpeg", "png"])],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = "user_documents"
        verbose_name = "Document Utilisateur"
        verbose_name_plural = "Documents Utilisateurs"
        indexes = [
            models.Index(fields=["user", "verified"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.document_type}"


class RefreshToken(models.Model):
    """Modèle pour la gestion des refresh tokens"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="refresh_tokens"
    )
    token_hash = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = "refresh_tokens"
        verbose_name = "Refresh Token"
        verbose_name_plural = "Refresh Tokens"
        indexes = [
            models.Index(fields=["token_hash"]),
            models.Index(fields=["user", "revoked"]),
        ]

    def __str__(self):
        return f"Token pour {self.user.email}"

    def is_valid(self):
        """Vérifie si le token est toujours valide"""
        from django.utils import timezone

        return not self.revoked and self.expires_at > timezone.now()


class EmailVerification(models.Model):
    """Modèle pour la vérification d'email"""

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="email_verifications"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "email_verifications"
        verbose_name = "Vérification Email"
        verbose_name_plural = "Vérifications Email"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code():
        """Génère un code aléatoire de 6 chiffres"""
        return "".join(random.choices(string.digits, k=6))

    def is_valid(self):
        """Vérifie si le code est encore valide"""
        return (
            not self.is_verified
            and self.expires_at > timezone.now()
            and self.attempts < 3
        )

    def __str__(self):
        return f"Email verification for {self.user.email}"


class PasswordResetToken(models.Model):
    """Modèle pour les tokens de réinitialisation de mot de passe"""

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="password_reset_tokens"
    )
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        db_table = "password_reset_tokens"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        if not self.expires_at:
            # Token valide pendant 1 heure
            self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_valid(self):
        """Vérifie si le token est valide"""
        return not self.used and self.expires_at > timezone.now()

    def __str__(self):
        return f"Password reset token for {self.user.email}"


class PhoneVerification(models.Model):
    """Modèle pour la vérification de téléphone"""

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="phone_verifications"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "phone_verifications"
        verbose_name = "Vérification Téléphone"
        verbose_name_plural = "Vérifications Téléphone"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code():
        """Génère un code aléatoire de 6 chiffres"""
        return "".join(random.choices(string.digits, k=6))

    def is_valid(self):
        """Vérifie si le code est encore valide"""
        return (
            not self.is_verified
            and self.expires_at > timezone.now()
            and self.attempts < 3
        )

    def __str__(self):
        return f"Phone verification for {self.user.phone_number}"
