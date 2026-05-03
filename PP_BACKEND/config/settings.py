"""
Configuration Django pour le projet DZ-CarPool
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,dz-carpool-backend-1.onrender.com"
).split(",")

# Application definition
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Requis pour allauth
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "corsheaders",  # ✅ CORS
    "channels",
    # Allauth pour social authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",  # Provider Google
    # Local apps
    "app.core.apps.CoreConfig",
    "app.users",
    "app.trajets",
    "app.messaging",
    "django_extensions",
    "app",
    "app.reservations.apps.ReservationsConfig",
    "app.notifications.apps.NotificationsConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ✅ DOIT ÊTRE EN PREMIER
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.core.middleware.RequestLoggingMiddleware",
    "app.core.middleware.UserActivityMiddleware",
    "app.core.middleware.RateLimitMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# ============================================
# ✅ CONFIGURATION REDIS & CHANNELS LAYER
# ============================================
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

# Si l'URL Redis utilise SSL (rediss://)
if REDIS_URL.startswith("rediss://"):
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [{
                    "address": REDIS_URL,
                    "ssl_cert_reqs": None,  # ✅ Désactive la vérification SSL stricte
                }],
            },
        },
    }
    # Cache avec SSL
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {
                    "ssl_cert_reqs": None,
                },
            },
            "KEY_PREFIX": "dzcarpool",
            "TIMEOUT": 300,
        }
    }
else:
    # Redis sans SSL (développement local)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        },
    }
    # Cache sans SSL
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "dzcarpool",
            "TIMEOUT": 300,
        }
    }

# URL WebSocket (pour le frontend)
WEBSOCKET_URL = config("WEBSOCKET_URL", default="ws://localhost:8000")

# ============================================
# DATABASE CONFIGURATION
# ============================================
import dj_database_url

if 'DATABASE_URL' in os.environ:
    # En production sur Render
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # En développement local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Algiers"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# URL du backend (pour construire les URLs complètes)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000").rstrip("/")

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "users.User"

# ============================================
# REST FRAMEWORK CONFIGURATION
# ============================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "app.core.authentication.CustomJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_PAGINATION_CLASS": "app.core.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "app.core.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "app.core.throttling.BurstRateThrottle",
        "app.core.throttling.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "burst": "60/min",
        "sustained": "1000/day",
        "anon_burst": "20/min",
    },
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",
}

# ============================================
# JWT SETTINGS
# ============================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME_MINUTES", default=60, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": config("JWT_ALGORITHM", default="HS256"),
    "SIGNING_KEY": config("JWT_SECRET_KEY", default=SECRET_KEY),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

# ============================================
# ✅ CORS SETTINGS - CONFIGURATION CORRIGÉE
# ============================================
if DEBUG:
    # Mode développement - Permissif
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    # Mode production - Stricte
    CORS_ALLOWED_ORIGINS = [
        "https://dz-car-pool-frontend.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF - URLs de confiance
CSRF_TRUSTED_ORIGINS = [
    "https://dz-car-pool-frontend.vercel.app",
    "https://dz-carpool-backend-1.onrender.com",
]

# ✅ Méthodes HTTP autorisées
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# ✅ Headers autorisés
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ============================================
# DRF SPECTACULAR SETTINGS
# ============================================
SPECTACULAR_SETTINGS = {
    "TITLE": "DZ-CarPool API",
    "DESCRIPTION": "API pour la plateforme de covoiturage DZ-CarPool",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ============================================
# BUSINESS LOGIC CONFIGURATION
# ============================================
PLATFORM_COMMISSION_RATE = config("PLATFORM_COMMISSION_RATE", default=0.15, cast=float)
CONFORT_SUPPLEMENT_RATE = config("CONFORT_SUPPLEMENT_RATE", default=0.30, cast=float)
LONG_DISTANCE_THRESHOLD_KM = 300
PAUSE_DURATION_MINUTES = 15
FUEL_CONSUMPTION_L_PER_100KM = config(
    "FUEL_CONSUMPTION_L_PER_100KM", default=8.0, cast=float
)

# ============================================
# ✅ LOGGING CONFIGURATION
# ============================================
if os.environ.get('RENDER'):
    # Sur Render : logs console avec détails WebSocket
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            # ✅ Logs détaillés pour WebSocket
            "daphne": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "channels": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "app.messaging": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "app.notifications": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }
else:
    # En développement local : console + fichier
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": logs_dir / "django.log",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "daphne": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
            "channels": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
            },
        },
    }

# Cache pour les sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ============================================
# EMAIL CONFIGURATION
# ============================================
DJANGO_ENV = config("DJANGO_ENV", default="development")

if DJANGO_ENV == "production":
    # MODE PRODUCTION - Envoi SMTP réel
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@dzcarpool.com")
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    print("=" * 60)
    print("✅ MODE PRODUCTION : Envoi d'emails SMTP activé")
    print(f"📧 Serveur SMTP : {EMAIL_HOST}:{EMAIL_PORT}")
    print(f"👤 Utilisateur : {EMAIL_HOST_USER}")
    print("=" * 60)
else:
    # MODE DÉVELOPPEMENT - Console uniquement
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "noreply@dzcarpool.com"
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    print("=" * 60)
    print("🔧 MODE DÉVELOPPEMENT : Emails affichés dans la console")
    print("💡 Pour envoyer de vrais emails, définissez DJANGO_ENV=production")
    print("=" * 60)

# Templates d'emails
EMAIL_TEMPLATES = {
    "welcome": "emails/welcome.html",
    "reservation_confirmed": "emails/reservation_confirmed.html",
    "trajet_cancelled": "emails/trajet_cancelled.html",
    "password_reset": "emails/password_reset.html",
}

# ============================================
# ALLAUTH CONFIGURATION - GOOGLE AUTH
# ============================================
SITE_ID = 1

# Backends d'authentification
AUTHENTICATION_BACKENDS = [
    # Backend Django par défaut (email/password)
    "django.contrib.auth.backends.ModelBackend",
    # Backend allauth (pour Google, Facebook, etc.)
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Configuration allauth
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]

# Configuration Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID", default=""),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET", default=""),
            "key": "",
        },
    }
}

# Redirection après login social
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"