import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_algerian_phone(value):
    """
    Valide un numéro de téléphone algérien
    Format: 0XXXXXXXXX ou +213XXXXXXXXX
    """
    pattern = r"^(0|\+213)[5-7][0-9]{8}$"
    if not re.match(pattern, value):
        raise ValidationError(
            _(
                "Numéro de téléphone algérien invalide. Format: 0XXXXXXXXX ou +213XXXXXXXXX"
            ),
            code="invalid_phone",
        )


def validate_wilaya_name(value):
    """
    Valide un nom de wilaya algérienne
    """
    wilayas = [
        "Adrar",
        "Chlef",
        "Laghouat",
        "Oum El Bouaghi",
        "Batna",
        "Béjaïa",
        "Biskra",
        "Béchar",
        "Blida",
        "Bouira",
        "Tamanrasset",
        "Tébessa",
        "Tlemcen",
        "Tiaret",
        "Tizi Ouzou",
        "Alger",
        "Djelfa",
        "Jijel",
        "Sétif",
        "Saïda",
        "Skikda",
        "Sidi Bel Abbès",
        "Annaba",
        "Guelma",
        "Constantine",
        "Médéa",
        "Mostaganem",
        "M'Sila",
        "Mascara",
        "Ouargla",
        "Oran",
        "El Bayadh",
        "Illizi",
        "Bordj Bou Arréridj",
        "Boumerdès",
        "El Tarf",
        "Tindouf",
        "Tissemsilt",
        "El Oued",
        "Khenchela",
        "Souk Ahras",
        "Tipaza",
        "Mila",
        "Aïn Defla",
        "Naâma",
        "Aïn Témouchent",
        "Ghardaïa",
        "Relizane",
    ]

    if value not in wilayas:
        raise ValidationError(
            _("Wilaya invalide. Veuillez choisir une wilaya algérienne valide."),
            code="invalid_wilaya",
        )


def validate_future_date(value):
    """
    Valide que la date est dans le futur
    """
    from django.utils import timezone

    if value < timezone.now().date():
        raise ValidationError(_("La date doit être dans le futur."), code="past_date")


def validate_price_range(value):
    """
    Valide que le prix est dans une fourchette raisonnable
    """
    from decimal import Decimal

    min_price = Decimal("100.00")
    max_price = Decimal("50000.00")

    if value < min_price or value > max_price:
        raise ValidationError(
            _(f"Le prix doit être entre {min_price} DA et {max_price} DA."),
            code="invalid_price_range",
        )


def validate_seats_count(value):
    """
    Valide le nombre de places
    """
    if value < 1 or value > 8:
        raise ValidationError(
            _("Le nombre de places doit être entre 1 et 8."), code="invalid_seats"
        )
