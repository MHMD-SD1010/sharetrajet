import json
from decimal import Decimal
from pathlib import Path


def load_fuel_prices():
    """
    Charge le fichier prix_carburants.json
    Conforme au cahier des charges : simulation d'une API externe
    """
    try:
        # Chemin vers le fichier JSON à la racine du projet
        base_dir = Path(__file__).resolve().parent.parent
        json_path = base_dir / "prix_carburants.json"

        if not json_path.exists():
            print(f"⚠️ Fichier prix_carburants.json introuvable à {json_path}")
            return None

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data
    except Exception as e:
        print(f"❌ Erreur lors du chargement de prix_carburants.json: {e}")
        return None


def extract_wilaya_from_location(location_name):
    """
    Extrait le nom de la wilaya depuis une adresse ou un nom de ville

    Args:
        location_name: Nom de la ville/adresse (ex: "Alger", "Oran", "Birkhadem, Algiers")

    Returns:
        str: Nom de la wilaya normalisé ou None
    """
    if not location_name:
        return None

    # Dictionnaire de correspondance ville -> wilaya
    # Pour gérer les cas où la ville n'est pas exactement le nom de la wilaya
    wilaya_mapping = {
        "alger": "Alger",
        "algiers": "Alger",
        "oran": "Oran",
        "constantine": "Constantine",
        "annaba": "Annaba",
        "blida": "Blida",
        "batna": "Batna",
        "setif": "Sétif",
        "sétif": "Sétif",
        "tlemcen": "Tlemcen",
        "bejaia": "Béjaïa",
        "béjaïa": "Béjaïa",
        "biskra": "Biskra",
        "tebessa": "Tébessa",
        "bechar": "Béchar",
        "béchar": "Béchar",
        "tamanrasset": "Tamanrasset",
        "ouargla": "Ouargla",
        "ghardaia": "Ghardaïa",
        "ghardaïa": "Ghardaïa",
        "chlef": "Chlef",
        "mostaganem": "Mostaganem",
        "sidi bel abbes": "Sidi Bel Abbès",
        "jijel": "Jijel",
        "skikda": "Skikda",
        "guelma": "Guelma",
        "tiaret": "Tiaret",
        "birkhadem": "Alger",  # Birkhadem est dans Alger
        "bouira": "Bouira",
        "tizi ouzou": "Tizi Ouzou",
        "bordj bou arreridj": "Bordj Bou Arreridj",
    }

    # Normaliser le nom (minuscules, supprimer les accents pour la recherche)
    normalized = location_name.lower().strip()

    # Enlever les virgules et prendre le premier mot (cas "Birkhadem, Algiers")
    if "," in normalized:
        normalized = normalized.split(",")[0].strip()

    # Chercher dans le mapping
    return wilaya_mapping.get(normalized)


def get_fuel_price_for_wilaya(wilaya_name, fuel_type):
    """
    Récupère le prix du carburant pour une wilaya et un type de carburant

    Args:
        wilaya_name: Nom de la wilaya (ex: "Alger")
        fuel_type: Type de carburant (ex: "gasoil", "essence_sans_plomb")

    Returns:
        Decimal: Prix par litre ou None
    """
    data = load_fuel_prices()
    if not data:
        return None

    # Parcourir les wilayas
    for code, info in data.get("wilayas", {}).items():
        if info.get("name") == wilaya_name:
            prices = info.get("prices", {})
            price = prices.get(fuel_type)
            if price:
                return Decimal(str(price))

    # Wilaya non trouvée, utiliser une moyenne nationale
    print(f"⚠️ Wilaya {wilaya_name} non trouvée, utilisation de la moyenne")
    return get_average_fuel_price(fuel_type)


def get_average_fuel_price(fuel_type):
    """
    Calcule le prix moyen national pour un type de carburant

    Args:
        fuel_type: Type de carburant

    Returns:
        Decimal: Prix moyen par litre
    """
    data = load_fuel_prices()
    if not data:
        # Prix par défaut si le fichier n'est pas disponible
        defaults = {
            "essence_sans_plomb": Decimal("51.00"),
            "gasoil": Decimal("36.00"),
            "gpl": Decimal("10.00"),
            "electrique": Decimal("0.18"),
        }
        return defaults.get(fuel_type, Decimal("40.00"))

    prices = []
    for code, info in data.get("wilayas", {}).items():
        price = info.get("prices", {}).get(fuel_type)
        if price:
            prices.append(Decimal(str(price)))

    if prices:
        return sum(prices) / len(prices)

    # Fallback
    return Decimal("40.00")


def get_default_consumption(fuel_type):
    """
    Récupère la consommation moyenne par défaut selon le cahier des charges

    Args:
        fuel_type: Type de carburant

    Returns:
        Decimal: Consommation moyenne (L/100km ou kWh/100km)
    """
    data = load_fuel_prices()
    if data and "consommation_moyenne" in data:
        consumption = data["consommation_moyenne"].get(fuel_type)
        if consumption:
            return Decimal(str(consumption))

    # Par défaut : 8L/100km comme spécifié dans le cahier des charges
    return Decimal("8.00")


def calculate_suggested_price(
    distance, ville_depart, fuel_type, fuel_consumption=None, nbr_places=1
):
    """
    Calcule le prix conseillé par siège basé sur le coût du carburant
    CONFORME AU CAHIER DES CHARGES

    Processus :
    1. Lire le fichier prix_carburants.json
    2. Calculer le coût total du carburant pour le trajet
    3. Diviser par le nombre de sièges pour obtenir le prix conseillé

    Args:
        distance: Distance du trajet en km
        ville_depart: Ville de départ (pour identifier la wilaya)
        fuel_type: Type de carburant ("gasoil", "essence_sans_plomb", etc.)
        fuel_consumption: Consommation du véhicule (optionnel, utilise la moyenne sinon)
        nbr_places: Nombre de places disponibles

    Returns:
        Decimal: Prix conseillé par siège en DZD
    """
    try:
        # 1. Extraire la wilaya depuis la ville de départ
        wilaya = extract_wilaya_from_location(ville_depart)
        if not wilaya:
            print(f"Impossible d'extraire la wilaya depuis '{ville_depart}'")
            wilaya = "Alger"  # Défaut

        # 2. Récupérer le prix du carburant pour cette wilaya
        fuel_price = get_fuel_price_for_wilaya(wilaya, fuel_type)
        if not fuel_price:
            print(f"⚠️ Prix du carburant non trouvé pour {wilaya}/{fuel_type}")
            fuel_price = get_average_fuel_price(fuel_type)

        # 3. Utiliser la consommation fournie ou la moyenne (8L/100km par défaut)
        if fuel_consumption is None:
            fuel_consumption = get_default_consumption(fuel_type)
        else:
            fuel_consumption = Decimal(str(fuel_consumption))

        # 4. Calculer le coût total du carburant
        # Formule : (distance * consommation * prix) / 100
        distance_decimal = Decimal(str(distance))
        total_fuel_cost = (distance_decimal * fuel_consumption * fuel_price) / Decimal(
            "100"
        )

        # 5. Ajouter un coût d'usure/entretien (environ 50% du carburant)
        total_cost = total_fuel_cost * Decimal("1.5")

        # 6. Diviser par le nombre de sièges pour obtenir le prix conseillé par siège
        nbr_places_decimal = Decimal(str(nbr_places))
        suggested_price_per_seat = total_cost / nbr_places_decimal

        # Arrondir à 10 DZD près (plus lisible)
        suggested_price_per_seat = (suggested_price_per_seat / 10).quantize(
            Decimal("1")
        ) * 10

        print(
            f"""
        ✅ Calcul du prix conseillé :
        - Distance: {distance} km
        - Wilaya: {wilaya}
        - Carburant: {fuel_type}
        - Prix/L: {fuel_price} DZD
        - Consommation: {fuel_consumption} L/100km
        - Coût carburant: {total_fuel_cost:.2f} DZD
        - Coût total (avec usure): {total_cost:.2f} DZD
        - Prix conseillé/siège: {suggested_price_per_seat} DZD
        """
        )

        return suggested_price_per_seat

    except Exception as e:
        print(f"❌ Erreur lors du calcul du prix conseillé: {e}")
        # Prix par défaut en cas d'erreur : ~1500 DZD
        return Decimal("1500.00")


def get_fuel_prices_summary():
    """
    Retourne un résumé des prix du carburant par wilaya
    Utile pour l'API REST

    Returns:
        dict: Données du fichier JSON
    """
    return load_fuel_prices()
