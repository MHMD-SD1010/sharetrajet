-- ================================================
-- TABLES POUR LA GESTION DES UTILISATEURS
-- DZ-CarPool - Module Users
-- ================================================

-- Table des rôles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT DEFAULT ''
);

-- Table des préférences
CREATE TABLE IF NOT EXISTS preferences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    name_fr VARCHAR(100) DEFAULT '',
    name_en VARCHAR(100) DEFAULT '',
    category VARCHAR(20) DEFAULT 'interests' CHECK (category IN ('interests', 'habits', 'driving')),
    icon VARCHAR(10) DEFAULT ''
);

CREATE INDEX idx_preferences_category ON preferences(category, id);

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) DEFAULT '',
    last_name VARCHAR(100) DEFAULT '',
    phone_number VARCHAR(20) DEFAULT '',
    phone_verified BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    phone_verified_at TIMESTAMP,
    profile_picture VARCHAR(255),
    bio TEXT,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trips_as_driver INTEGER DEFAULT 0,
    trips_as_passenger INTEGER DEFAULT 0,
    average_rating NUMERIC(3, 2) DEFAULT 0.0,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_date_joined ON users(date_joined);

-- Table de liaison users-preferences
CREATE TABLE IF NOT EXISTS users_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    preference_id INTEGER NOT NULL REFERENCES preferences(id) ON DELETE CASCADE,
    UNIQUE(user_id, preference_id)
);

CREATE INDEX idx_users_preferences_user ON users_preferences(user_id);
CREATE INDEX idx_users_preferences_preference ON users_preferences(preference_id);

-- Table des documents utilisateurs
CREATE TABLE IF NOT EXISTS user_documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_type VARCHAR(20) NOT NULL CHECK (document_type IN ('CNI', 'PERMIS', 'AUTRE')),
    file_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    verified_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP,
    rejection_reason TEXT DEFAULT ''
);

CREATE INDEX idx_user_documents_user_verified ON user_documents(user_id, verified);

-- Table des refresh tokens
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_user_revoked ON refresh_tokens(user_id, revoked);

-- Table de vérification email
CREATE TABLE IF NOT EXISTS email_verifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0
);

CREATE INDEX idx_email_verifications_user ON email_verifications(user_id);

-- Table de vérification téléphone
CREATE TABLE IF NOT EXISTS phone_verifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0
);

CREATE INDEX idx_phone_verifications_user ON phone_verifications(user_id);

-- Trigger pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();