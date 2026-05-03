"""
Configuration Django pour le build sur Render
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger le fichier .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Importer les settings de base
from .settings import *  # noqa: F403, F401, E402

# ==================== BASE DE DONNÉES TEMPORAIRE POUR LE BUILD ====================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/build_db.sqlite3",
    }
}

# ==================== CONFIGURATION CACHE ====================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "build-cache",
    }
}

# ==================== CONFIGURATION EMAIL ====================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ==================== DÉSACTIVER DEBUG ====================
DEBUG = False

# ==================== LOGGING SIMPLIFIÉ (CONSOLE UNIQUEMENT) ====================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
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
    },
}

print("=" * 80)
print("🏗️  BUILD SETTINGS LOADED")
print("📊 Database: SQLite (temporaire pour le build)")
print("🗄️  Cache: In-Memory")
print("📝 Logging: Console uniquement")
print("=" * 80)