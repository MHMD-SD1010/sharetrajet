"""
Script pour peupler les préférences avec traductions
À exécuter avec: python manage.py shell < populate_preferences.py
"""

from app.users.models import Preference

# Données à insérer
preferences_data = [
    # Centres d'intérêt
    {
        "id": 1,
        "name_fr": "Sport",
        "name_en": "Sport",
        "category": "interests",
        "icon": "⚽",
    },
    {
        "id": 2,
        "name_fr": "Musique",
        "name_en": "Music",
        "category": "interests",
        "icon": "🎵",
    },
    {
        "id": 3,
        "name_fr": "Culture",
        "name_en": "Culture",
        "category": "interests",
        "icon": "🎭",
    },
    {
        "id": 4,
        "name_fr": "Philosophie",
        "name_en": "Philosophy",
        "category": "interests",
        "icon": "🤔",
    },
    {
        "id": 5,
        "name_fr": "Lecture",
        "name_en": "Reading",
        "category": "interests",
        "icon": "📚",
    },
    {
        "id": 6,
        "name_fr": "Films et séries",
        "name_en": "Movies & Series",
        "category": "interests",
        "icon": "🎬",
    },
    {
        "id": 7,
        "name_fr": "Science",
        "name_en": "Science",
        "category": "interests",
        "icon": "🔬",
    },
    {
        "id": 8,
        "name_fr": "Technologie",
        "name_en": "Technology",
        "category": "interests",
        "icon": "💻",
    },
    {
        "id": 9,
        "name_fr": "Voyage",
        "name_en": "Travel",
        "category": "interests",
        "icon": "✈️",
    },
    # Habitudes
    {
        "id": 10,
        "name_fr": "Fumeur",
        "name_en": "Smoker",
        "category": "habits",
        "icon": "🚬",
    },
    {
        "id": 11,
        "name_fr": "Non-fumeur",
        "name_en": "Non-Smoker",
        "category": "habits",
        "icon": "🚭",
    },
    {
        "id": 12,
        "name_fr": "Aime les animaux",
        "name_en": "Pets Lover",
        "category": "habits",
        "icon": "🐾",
    },
    {
        "id": 13,
        "name_fr": "Silencieux",
        "name_en": "Quiet",
        "category": "habits",
        "icon": "🤫",
    },
    {
        "id": 14,
        "name_fr": "Bavard",
        "name_en": "Chatty",
        "category": "habits",
        "icon": "💬",
    },
    # Préférences de conduite
    {
        "id": 15,
        "name_fr": "Conducteur rapide",
        "name_en": "Fast Driver",
        "category": "driving",
        "icon": "⚡",
    },
    {
        "id": 16,
        "name_fr": "Conducteur prudent",
        "name_en": "Careful Driver",
        "category": "driving",
        "icon": "🛡️",
    },
    {
        "id": 17,
        "name_fr": "Avec musique",
        "name_en": "Music On",
        "category": "driving",
        "icon": "🎶",
    },
    {
        "id": 18,
        "name_fr": "Silence",
        "name_en": "Silence",
        "category": "driving",
        "icon": "🔇",
    },
]

# Mettre à jour ou créer les préférences
for pref_data in preferences_data:
    Preference.objects.update_or_create(
        id=pref_data["id"],
        defaults={
            "name": pref_data["name_fr"],  # Pour compatibilité
            "name_fr": pref_data["name_fr"],
            "name_en": pref_data["name_en"],
            "category": pref_data["category"],
            "icon": pref_data["icon"],
            "description": "",
        },
    )
    print(f"✓ Préférence {pref_data['id']}: {pref_data['name_fr']}")

print("\n✅ Toutes les préférences ont été importées avec succès!")
