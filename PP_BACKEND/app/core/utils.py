from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_email(user, subject, template_name, context):
    """
    Envoie un email de notification à un utilisateur
    """
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def format_distance(distance):
    """
    Formate une distance en km avec unité
    """
    if distance < 1:
        return f"{distance * 1000:.0f} m"
    return f"{distance:.1f} km"


def format_price(price):
    """
    Formate un prix en dinars algériens
    """
    return f"{price:,.2f} DA"


def calculate_trip_duration(distance, average_speed=80):
    """
    Calcule la durée estimée d'un trajet
    """
    from datetime import timedelta

    hours = distance / average_speed
    return timedelta(hours=hours)


def generate_unique_code(length=8):
    """
    Génère un code unique alphanumérique
    """
    import random
    import string

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
