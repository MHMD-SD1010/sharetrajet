import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EmailService:
    """Service pour l'envoi d'emails"""

    @staticmethod
    def _send_email(to_email, subject, text_content, html_content):
        """
        Méthode interne pour envoyer un email
        Retourne True si succès, False sinon
        """
        try:
            if settings.DEBUG:
                logger.info(
                    """
════════════════════════════════════════
📧 EMAIL ENVOYÉ
════════════════════════════════════════
À: %s
Sujet: %s
════════════════════════════════════════
""",
                    to_email,
                    subject,
                )

            send_mail(
                subject=subject,
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                html_message=html_content,
                fail_silently=False,
            )

            logger.info("✅ Email envoyé avec succès à %s", to_email)
            return True

        except Exception as e:
            logger.error("❌ Erreur envoi email à %s: %s", to_email, str(e))
            logger.exception(e)

            if settings.DEBUG:
                raise

            return False

    @staticmethod
    def send_verification_code(user, code):
        """Envoie un email avec le code de vérification"""
        subject = "Vérification de votre email - DZ-CarPool"

        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body
    style="
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
    "
>
    <div
        style="
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        "
    >
        <h1 style="color: #FF5722;">Bienvenue sur DZ-CarPool!</h1>

        <p>Bonjour {user.first_name or user.email},</p>

        <p>
            Merci de vous être inscrit sur DZ-CarPool.
            Voici votre code de vérification :
        </p>

        <div
            style="
                background-color: #f5f5f5;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            "
        >
            <h2
                style="
                    color: #FF5722;
                    font-size: 32px;
                    margin: 0;
                "
            >
                {code}
            </h2>
        </div>

        <p>Ce code est valide pendant 30 minutes.</p>

        <p style="color: #666; font-size: 14px;">
            Si vous n'avez pas créé de compte, ignorez cet email.
        </p>
    </div>
</body>
</html>
"""

        text_message = f"""
Bienvenue sur DZ-CarPool!

Bonjour {user.first_name or user.email},

Voici votre code de vérification : {code}

Ce code est valide pendant 30 minutes.
"""

        return EmailService._send_email(
            user.email,
            subject,
            text_message,
            html_message,
        )

    @staticmethod
    def send_password_reset_email(user, reset_url):
        """Envoie un email avec le lien de réinitialisation"""
        subject = "Réinitialisation de votre mot de passe - DZ-CarPool"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body
    style="
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
    "
>
    <div
        style="
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        "
    >
        <div
            style="
                background-color: white;
                padding: 30px;
                border-radius: 8px;
            "
        >
            <h1 style="color: #FF5722; text-align: center;">
                DZ-CarPool
            </h1>

            <h2 style="color: #333;">
                Réinitialisation de votre mot de passe
            </h2>

            <p>Bonjour {user.first_name or user.email},</p>

            <p>
                Nous avons reçu une demande de réinitialisation
                de mot de passe pour votre compte DZ-CarPool.
            </p>

            <p>
                Cliquez sur le bouton ci-dessous pour créer
                un nouveau mot de passe :
            </p>

            <div style="text-align: center; margin: 30px 0;">
                <a
                    href="{reset_url}"
                    style="
                        display: inline-block;
                        padding: 15px 30px;
                        background-color: #FF5722;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                    "
                >
                    Réinitialiser mon mot de passe
                </a>
            </div>

            <p style="color: #666; font-size: 14px;">
                Ou copiez-collez ce lien dans votre navigateur :
                <br>
                <a
                    href="{reset_url}"
                    style="
                        color: #FF5722;
                        word-break: break-all;
                    "
                >
                    {reset_url}
                </a>
            </p>

            <div
                style="
                    background-color: #fff3e0;
                    padding: 15px;
                    border-left: 4px solid #FF5722;
                    margin: 20px 0;
                "
            >
                <p style="margin: 0; color: #e65100;">
                    <strong>⚠️ Important :</strong>
                    Ce lien est valide pendant 1 heure.
                </p>
            </div>

            <p style="color: #666; font-size: 14px;">
                Si vous n'avez pas demandé cette réinitialisation,
                ignorez cet email. Votre mot de passe restera inchangé.
            </p>

            <hr
                style="
                    border: none;
                    border-top: 1px solid #eee;
                    margin: 30px 0;
                "
            >

            <p
                style="
                    color: #999;
                    font-size: 12px;
                    text-align: center;
                "
            >
                © 2024 DZ-CarPool. Tous droits réservés.
            </p>
        </div>
    </div>
</body>
</html>
"""

        text_content = f"""
Réinitialisation de votre mot de passe - DZ-CarPool

Bonjour {user.first_name or user.email},

Cliquez sur ce lien pour créer un nouveau mot de passe :
{reset_url}

Ce lien est valide pendant 1 heure.

Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
"""

        return EmailService._send_email(
            user.email,
            subject,
            text_content,
            html_content,
        )


class SMSService:
    """Service pour l'envoi de SMS (simulation)"""

    @staticmethod
    def send_verification_code(user, code):
        """
        Envoie un SMS avec le code de vérification
        En mode dev, le code est affiché dans la console
        """
        message = (
            "DZ-CarPool: Votre code de vérification est " f"{code}. Valide 30 minutes."
        )

        try:
            if settings.DEBUG:
                logger.info(
                    """
════════════════════════════════════════
📱 SMS DE VÉRIFICATION
════════════════════════════════════════
À: %s
Nom: %s %s
Code: %s
Message: %s
════════════════════════════════════════
""",
                    user.phone_number,
                    user.first_name,
                    user.last_name,
                    code,
                    message,
                )

            return True

        except Exception as e:
            logger.error("❌ Erreur envoi SMS: %s", str(e))
            return False
