-- ================================================
-- TABLES POUR LA GESTION DES TRAJETS
-- DZ-CarPool - Module Trajets
-- ================================================

-- Table des trajets
CREATE TABLE IF NOT EXISTS trajets (
    id SERIAL PRIMARY KEY,
    conducteur_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    ville_depart VARCHAR(100) NOT NULL,
    ville_arrivee VARCHAR(100) NOT NULL,
    adresse_depart TEXT DEFAULT '',
    adresse_arrivee TEXT DEFAULT '',

    date DATE NOT NULL,
    heure_depart TIME NOT NULL,

    nbr_places INTEGER NOT NULL CHECK (nbr_places >= 1),
    places_disponibles INTEGER NOT NULL CHECK (places_disponibles >= 0),

    price NUMERIC(10,2) NOT NULL CHECK (price >= 0.01),
    price_platform NUMERIC(10,2) DEFAULT 0.00,
    price_driver NUMERIC(10,2) DEFAULT 0.00,
    suggested_price NUMERIC(10,2),

    distance NUMERIC(10,2) NOT NULL CHECK (distance >= 0.01),
    is_confort BOOLEAN DEFAULT FALSE,
    pause_required BOOLEAN DEFAULT FALSE,

    fuel_type VARCHAR(20) NOT NULL DEFAULT 'gasoil'
        CHECK (fuel_type IN ('essence_sans_plomb', 'gasoil', 'gpl', 'electrique')),
    fuel_consumption NUMERIC(4,2) NOT NULL DEFAULT 8.00 CHECK (fuel_consumption >= 0.01),

    wilaya_depart VARCHAR(100) DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
        CHECK (status IN ('ACTIVE', 'COMPLETED', 'CANCELLED')),

    description TEXT DEFAULT '',
    luggage_allowed BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trajets_depart_arrivee_date ON trajets(ville_depart, ville_arrivee, date);
CREATE INDEX idx_trajets_conducteur_status ON trajets(conducteur_id, status);
CREATE INDEX idx_trajets_date_status ON trajets(date, status);
CREATE INDEX idx_trajets_fuel_type ON trajets(fuel_type);
CREATE INDEX idx_trajets_wilaya_depart ON trajets(wilaya_depart);

-- Table intermédiaire trajet-preferences (ManyToMany with through model)
CREATE TABLE IF NOT EXISTS trajets_preferences (
    id SERIAL PRIMARY KEY,
    trajet_id INTEGER NOT NULL REFERENCES trajets(id) ON DELETE CASCADE,
    preference_id INTEGER NOT NULL REFERENCES preferences(id) ON DELETE CASCADE,
    UNIQUE (trajet_id, preference_id)
);

CREATE INDEX idx_trajets_preferences_trajet ON trajets_preferences(trajet_id);
CREATE INDEX idx_trajets_preferences_preference ON trajets_preferences(preference_id);

-- Table des étapes intermédiaires
CREATE TABLE IF NOT EXISTS trajet_etapes (
    id SERIAL PRIMARY KEY,
    trajet_id INTEGER NOT NULL REFERENCES trajets(id) ON DELETE CASCADE,
    ville VARCHAR(100) NOT NULL,
    adresse TEXT DEFAULT '',
    heure_arrivee TIME NOT NULL,
    ordre INTEGER NOT NULL CHECK (ordre >= 1),
    UNIQUE (trajet_id, ordre)
);

CREATE INDEX idx_trajet_etapes_trajet ON trajet_etapes(trajet_id);

-- Table des prix carburants
CREATE TABLE IF NOT EXISTS fuel_prices (
    id SERIAL PRIMARY KEY,
    wilaya_code VARCHAR(2) NOT NULL DEFAULT '',
    wilaya_name VARCHAR(100) NOT NULL DEFAULT '',
    fuel_type VARCHAR(20) NOT NULL
        CHECK (fuel_type IN ('essence_sans_plomb', 'gasoil', 'gpl', 'electrique')),
    price_per_liter NUMERIC(6,2) NOT NULL CHECK (price_per_liter >= 0.01),
    effective_date DATE DEFAULT CURRENT_DATE,
    UNIQUE (wilaya_code, fuel_type, effective_date)
);

CREATE INDEX idx_fuel_prices_wilaya_code ON fuel_prices(wilaya_code);
CREATE INDEX idx_fuel_prices_wilaya_name_fuel_type ON fuel_prices(wilaya_name, fuel_type);

-- Trigger pour maintenir updated_at sur trajets
CREATE TRIGGER update_trajets_updated_at
    BEFORE UPDATE ON trajets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
