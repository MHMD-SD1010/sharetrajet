#!/usr/bin/env bash
set -o errexit

# Utiliser les settings de build
export DJANGO_SETTINGS_MODULE=config.build_settings

pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --no-input --noinput

echo "✅ Build terminé avec succès"