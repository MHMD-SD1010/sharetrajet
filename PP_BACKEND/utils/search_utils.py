from difflib import SequenceMatcher
from typing import Dict, Tuple

# Villes principales d'Algérie avec leurs régions
WILAYAS_DATA = {
    "alger": {
        "region": "centre",
        "alternatives": ["alger", "algiers", "bab ezzouar", "kouba"],
    },
    "oran": {"region": "ouest", "alternatives": ["oran", "wahran", "es senia"]},
    "constantine": {
        "region": "est",
        "alternatives": ["constantine", "cirta", "el khroub"],
    },
    "annaba": {"region": "est", "alternatives": ["annaba", "bone", "seraidi"]},
    "tlemcen": {"region": "ouest", "alternatives": ["tlemcen", "tilimsen", "maghnia"]},
    "sétif": {"region": "est", "alternatives": ["sétif", "setif", "ain oulmene"]},
    "batna": {"region": "est", "alternatives": ["batna", "batnah"]},
    "béjaïa": {"region": "est", "alternatives": ["béjaïa", "bejaia", "bgayet"]},
    "tizi ouzou": {
        "region": "centre",
        "alternatives": ["tizi ouzou", "tizi", "azazga"],
    },
    "blida": {"region": "centre", "alternatives": ["blida", "boufarik", "mouzaia"]},
    "béchar": {"region": "sud-ouest", "alternatives": ["béchar", "bechar"]},
    "biskra": {"region": "sud-est", "alternatives": ["biskra", "sidi okba"]},
    "ouargla": {"region": "sud", "alternatives": ["ouargla", "warqla"]},
    "ghardaïa": {"region": "sud", "alternatives": ["ghardaïa", "ghardaia"]},
    "mostaganem": {"region": "ouest", "alternatives": ["mostaganem", "must"]},
    "skikda": {"region": "est", "alternatives": ["skikda", "philippeville"]},
    "tipaza": {"region": "centre", "alternatives": ["tipaza", "cherchell"]},
    "sidi bel abbès": {"region": "ouest", "alternatives": ["sidi bel abbès", "sba"]},
    "chlef": {"region": "centre", "alternatives": ["chlef", "ech cheliff"]},
    "jijel": {"region": "est", "alternatives": ["jijel", "el aouana"]},
}


def normalize_city_name(city: str) -> str:
    """Normalise le nom de la ville"""
    city = city.lower().strip()
    # Retirer les accents et caractères spéciaux
    replacements = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "à": "a",
        "â": "a",
        "î": "i",
        "ï": "i",
        "ô": "o",
        "ö": "o",
        "û": "u",
        "ü": "u",
        "ç": "c",
    }
    for old, new in replacements.items():
        city = city.replace(old, new)
    return city


def get_city_similarity(city1: str, city2: str) -> float:
    """
    Calcule la similarité entre deux villes (0.0 à 1.0)
    """
    city1_norm = normalize_city_name(city1)
    city2_norm = normalize_city_name(city2)

    # Correspondance exacte
    if city1_norm == city2_norm:
        return 1.0

    # Vérifier si c'est une ville alternative
    for wilaya, data in WILAYAS_DATA.items():
        if city1_norm in data["alternatives"] and city2_norm in data["alternatives"]:
            return 0.95

    # Similarité de chaîne (SequenceMatcher)
    return SequenceMatcher(None, city1_norm, city2_norm).ratio()


def get_regional_proximity(city1: str, city2: str) -> float:
    """
    Retourne un score de proximité régionale (0.0 à 0.7)
    """
    city1_norm = normalize_city_name(city1)
    city2_norm = normalize_city_name(city2)

    region1 = None
    region2 = None

    # Trouver les régions
    for wilaya, data in WILAYAS_DATA.items():
        if any(alt in city1_norm for alt in data["alternatives"]):
            region1 = data["region"]
        if any(alt in city2_norm for alt in data["alternatives"]):
            region2 = data["region"]

    if not region1 or not region2:
        return 0.3  # Score par défaut

    if region1 == region2:
        return 0.7  # Même région

    # Régions adjacentes
    adjacent_regions = {
        "centre": ["est", "ouest"],
        "est": ["centre", "sud-est"],
        "ouest": ["centre", "sud-ouest"],
        "sud": ["sud-est", "sud-ouest"],
    }

    if region2 in adjacent_regions.get(region1, []):
        return 0.5

    return 0.3


def calculate_date_proximity(target_date, trajet_date) -> float:
    """
    Calcule la proximité de date (1.0 = même date, décroît avec la distance)
    """
    diff = abs((trajet_date - target_date).days)

    if diff == 0:
        return 1.0
    elif diff <= 1:
        return 0.9
    elif diff <= 3:
        return 0.7
    elif diff <= 7:
        return 0.5
    elif diff <= 14:
        return 0.3
    else:
        return 0.1


def calculate_match_score(
    search_depart: str,
    search_arrivee: str,
    search_date,
    trajet_depart: str,
    trajet_arrivee: str,
    trajet_date,
) -> Tuple[float, Dict[str, float]]:
    """
    Calcule un score de correspondance global pour un trajet

    Returns:
        (score_total, détails) où score_total est entre 0 et 1
    """
    # Scores individuels
    depart_score = get_city_similarity(search_depart, trajet_depart)
    depart_regional = get_regional_proximity(search_depart, trajet_depart)

    arrivee_score = get_city_similarity(search_arrivee, trajet_arrivee)
    arrivee_regional = get_regional_proximity(search_arrivee, trajet_arrivee)

    date_score = calculate_date_proximity(search_date, trajet_date)

    # Pondérations
    weights = {
        "depart_exact": 0.35,
        "depart_regional": 0.10,
        "arrivee_exact": 0.35,
        "arrivee_regional": 0.10,
        "date": 0.10,
    }

    # Score total
    total_score = (
        depart_score * weights["depart_exact"]
        + depart_regional * weights["depart_regional"]
        + arrivee_score * weights["arrivee_exact"]
        + arrivee_regional * weights["arrivee_regional"]
        + date_score * weights["date"]
    )

    details = {
        "depart_score": depart_score,
        "depart_regional": depart_regional,
        "arrivee_score": arrivee_score,
        "arrivee_regional": arrivee_regional,
        "date_score": date_score,
        "total_score": total_score,
    }

    return total_score, details


def get_time_period(heure: str) -> str:
    try:
        hour = int(heure.split(":")[0])
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "evening"
    except (ValueError, IndexError):
        return "morning"
