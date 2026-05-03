-- ================================================
-- TABLES POUR MESSAGERIE ET NOTIFICATIONS
-- DZ-CarPool - Modules Messaging/Notifications
-- ================================================

-- Table des conversations
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    trajet_id INTEGER REFERENCES trajets(id) ON DELETE CASCADE,
    is_group BOOLEAN DEFAULT FALSE,
    last_message_id INTEGER,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_is_group_trajet ON conversations(is_group, trajet_id);

-- Table de liaison participants de conversation (ManyToMany)
CREATE TABLE IF NOT EXISTS conversations_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (conversation_id, user_id)
);

CREATE INDEX idx_conversations_participants_conversation ON conversations_participants(conversation_id);
CREATE INDEX idx_conversations_participants_user ON conversations_participants(user_id);

-- Table des messages
CREATE TABLE IF NOT EXISTS messagerie (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    trajet_id INTEGER REFERENCES trajets(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    media VARCHAR(255),
    media_type VARCHAR(50) DEFAULT '',
    is_group_message BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_sender_receiver ON messagerie(sender_id, receiver_id);
CREATE INDEX idx_messages_trajet_created_at ON messagerie(trajet_id, created_at);
CREATE INDEX idx_messages_is_read_receiver ON messagerie(is_read, receiver_id);
CREATE INDEX idx_messages_is_group_trajet ON messagerie(is_group_message, trajet_id);

-- Ajouter la FK last_message_id après création de messagerie (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_conversations_last_message'
    ) THEN
        ALTER TABLE conversations
            ADD CONSTRAINT fk_conversations_last_message
            FOREIGN KEY (last_message_id)
            REFERENCES messagerie(id)
            ON DELETE SET NULL;
    END IF;
END $$;

-- Table des notifications
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (
        type IN (
            'RESERVATION_REQUEST',
            'RESERVATION_APPROVED',
            'RESERVATION_REJECTED',
            'RESERVATION_CANCELLED',
            'MESSAGE_RECEIVED',
            'TRAJET_CANCELLED',
            'TRAJET_MODIFIED',
            'RATING_RECEIVED',
            'DOCUMENT_VERIFIED',
            'DOCUMENT_REJECTED',
            'WELCOME'
        )
    ),
    content TEXT NOT NULL,
    related_model VARCHAR(50),
    related_id INTEGER,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

CREATE INDEX idx_notifications_recipient_is_read ON notifications(recipient_id, is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
CREATE INDEX idx_notifications_related ON notifications(related_model, related_id);
