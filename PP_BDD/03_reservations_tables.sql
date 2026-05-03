-- ================================================
-- TABLES POUR LA GESTION DES RÉSERVATIONS
-- DZ-CarPool - Module Réservations
-- ================================================

-- Table des réservations
CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    trajet_id INTEGER NOT NULL REFERENCES trajets(id) ON DELETE CASCADE,
    passager_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    nbr_places INTEGER NOT NULL CHECK (nbr_places >= 1),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'CONFIRMED', 'REJECTED', 'CANCELLED')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    rejection_reason TEXT DEFAULT '',
    cancellation_reason TEXT DEFAULT '',

    price_per_seat NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(10,2) NOT NULL
);

CREATE INDEX idx_reservations_trajet_status ON reservations(trajet_id, status);
CREATE INDEX idx_reservations_passager_status ON reservations(passager_id, status);
CREATE INDEX idx_reservations_created_at ON reservations(created_at);

-- Contrainte Django:
-- Un même utilisateur ne peut pas avoir 2 réservations actives (PENDING/CONFIRMED) pour un même trajet
CREATE UNIQUE INDEX unique_active_reservation_per_user
    ON reservations(trajet_id, passager_id)
    WHERE status IN ('PENDING', 'CONFIRMED');

-- Table des évaluations mutuelles
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER NOT NULL UNIQUE REFERENCES reservations(id) ON DELETE CASCADE,
    rater_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rated_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    note INTEGER NOT NULL CHECK (note BETWEEN 1 AND 5),
    comment TEXT DEFAULT '',

    ponctualite INTEGER CHECK (ponctualite BETWEEN 1 AND 5),
    convivialite INTEGER CHECK (convivialite BETWEEN 1 AND 5),
    conduite INTEGER CHECK (conduite BETWEEN 1 AND 5),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_rating_per_user UNIQUE (reservation_id, rater_id)
);

CREATE INDEX idx_ratings_rated_note ON ratings(rated_id, note);
CREATE INDEX idx_ratings_created_at ON ratings(created_at);
