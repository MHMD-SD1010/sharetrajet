-- ================================================
-- SCRIPT DE SEEDING - DZ-CarPool
-- Jeu de données de test cohérent et complet
-- ================================================

-- ========================================
-- 1. RÔLES
-- ========================================
INSERT INTO roles (name, description) VALUES
('Passager', 'Utilisateur standard qui peut réserver des trajets'),
('Conducteur', 'Utilisateur qui peut proposer et conduire des trajets'),
('Admin', 'Administrateur de la plateforme'),
('Super Admin', 'Super administrateur avec tous les droits');

-- ========================================
-- 2. PRÉFÉRENCES
-- ========================================
INSERT INTO preferences (name, name_fr, name_en, category, icon) VALUES
-- Centres d'intérêt
('Musique', 'Musique', 'Music', 'interests', '🎵'),
('Sports', 'Sports', 'Sports', 'interests', '⚽'),
('Lecture', 'Lecture', 'Reading', 'interests', '📚'),
('Technologie', 'Technologie', 'Technology', 'interests', '💻'),
('Voyage', 'Voyage', 'Travel', 'interests', '✈️'),
('Cuisine', 'Cuisine', 'Cooking', 'interests', '🍳'),

-- Habitudes
('Non-fumeur', 'Non-fumeur', 'Non-smoker', 'habits', '🚭'),
('Animaux acceptés', 'Animaux acceptés', 'Pets allowed', 'habits', '🐕'),
('Bavard', 'Bavard', 'Chatty', 'habits', '💬'),
('Silencieux', 'Silencieux', 'Quiet', 'habits', '🤫'),
('Ponctuel', 'Ponctuel', 'Punctual', 'habits', '⏰'),

-- Préférences de conduite
('Conduite souple', 'Conduite souple', 'Smooth driving', 'driving', '🚗'),
('Climatisation', 'Climatisation', 'Air conditioning', 'driving', '❄️'),
('Pauses fréquentes', 'Pauses fréquentes', 'Frequent breaks', 'driving', '☕'),
('Musique en voiture', 'Musique en voiture', 'Music in car', 'driving', '🎶');

-- ========================================
-- 3. UTILISATEURS (Mot de passe: "password123" hashé en bcrypt)
-- ========================================
INSERT INTO users (email, password, first_name, last_name, phone_number, phone_verified, email_verified, email_verified_at, bio, role_id, is_active, average_rating) VALUES
-- Administrateurs
('admin@dzcarpool.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Ahmed', 'Benali', '+213550123456', true, true, CURRENT_TIMESTAMP, 'Administrateur principal de DZ-CarPool', 3, true, 5.0),

-- Conducteurs actifs
('karim.mohamed@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Karim', 'Mohamed', '+213551234567', true, true, CURRENT_TIMESTAMP, 'Conducteur expérimenté depuis 3 ans, trajets Alger-Oran réguliers', 2, true, 4.8),
('fatima.zahir@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Fatima', 'Zahir', '+213552345678', true, true, CURRENT_TIMESTAMP, 'Enseignante, trajets hebdomadaires Alger-Constantine', 2, true, 4.9),
('yacine.hamdi@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Yacine', 'Hamdi', '+213553456789', true, true, CURRENT_TIMESTAMP, 'Commercial, nombreux déplacements professionnels', 2, true, 4.7),
('sarah.djebar@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Sarah', 'Djebar', '+213554567890', true, true, CURRENT_TIMESTAMP, 'Infirmière, trajet Alger-Blida quotidien', 2, true, 5.0),
('mehdi.brahimi@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Mehdi', 'Brahimi', '+213555678901', true, true, CURRENT_TIMESTAMP, 'Ingénieur, conduite écologique privilégiée', 2, true, 4.6),

-- Passagers
('amina.kaci@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Amina', 'Kaci', '+213556789012', true, true, CURRENT_TIMESTAMP, 'Étudiante en médecine', 1, true, 4.9),
('riad.mansouri@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Riad', 'Mansouri', '+213557890123', true, true, CURRENT_TIMESTAMP, 'Développeur freelance', 1, true, 4.8),
('leila.cherif@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Leila', 'Cherif', '+213558901234', true, true, CURRENT_TIMESTAMP, 'Journaliste', 1, true, 4.7),
('nassim.bouaziz@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Nassim', 'Bouaziz', '+213559012345', true, true, CURRENT_TIMESTAMP, 'Chef de projet', 1, true, 4.9),
('samia.lakhal@email.dz', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe', 'Samia', 'Lakhal', '+213550987654', true, true, CURRENT_TIMESTAMP, 'Architecte', 1, true, 5.0);

-- ========================================
-- 4. PRÉFÉRENCES DES UTILISATEURS
-- ========================================
-- Karim (Conducteur)
INSERT INTO users_preferences (user_id, preference_id) VALUES
(2, 1), (2, 7), (2, 11), (2, 12), (2, 13);

-- Fatima (Conducteur)
INSERT INTO users_preferences (user_id, preference_id) VALUES
(3, 3), (3, 7), (3, 10), (3, 11), (3, 13);

-- Yacine (Conducteur)
INSERT INTO users_preferences (user_id, preference_id) VALUES
(4, 1), (4, 4), (4, 7), (4, 9), (4, 12);

-- Sarah (Conducteur)
INSERT INTO users_preferences (user_id, preference_id) VALUES
(5, 2), (5, 7), (5, 10), (5, 11), (5, 13);

-- Mehdi (Conducteur)
INSERT INTO users_preferences (user_id, preference_id) VALUES
(6, 4), (6, 5), (6, 7), (6, 12), (6, 14);

-- Passagers
INSERT INTO users_preferences (user_id, preference_id) VALUES
(7, 1), (7, 3), (7, 7), (7, 10),
(8, 4), (8, 7), (8, 9),
(9, 1), (9, 3), (9, 5), (9, 7),
(10, 2), (10, 4), (10, 7), (10, 11),
(11, 3), (11, 5), (11, 7), (11, 10);

-- ========================================
-- 5. PRIX DU CARBURANT PAR WILAYA
-- ========================================
INSERT INTO fuel_prices (wilaya_code, wilaya_name, fuel_type, price_per_liter) VALUES
-- Wilaya d'Alger (16)
('16', 'Alger', 'essence_sans_plomb', 47.52),
('16', 'Alger', 'gasoil', 29.76),
('16', 'Alger', 'gpl', 9.96),

-- Wilaya d'Oran (31)
('31', 'Oran', 'essence_sans_plomb', 47.52),
('31', 'Oran', 'gasoil', 29.76),
('31', 'Oran', 'gpl', 9.96),

-- Wilaya de Constantine (25)
('25', 'Constantine', 'essence_sans_plomb', 47.52),
('25', 'Constantine', 'gasoil', 29.76),
('25', 'Constantine', 'gpl', 9.96),

-- Wilaya de Blida (09)
('09', 'Blida', 'essence_sans_plomb', 47.52),
('09', 'Blida', 'gasoil', 29.76),
('09', 'Blida', 'gpl', 9.96),

-- Wilaya d'Annaba (23)
('23', 'Annaba', 'essence_sans_plomb', 47.52),
('23', 'Annaba', 'gasoil', 29.76),
('23', 'Annaba', 'gpl', 9.96);

-- ========================================
-- 6. TRAJETS
-- ========================================
-- Trajets actifs (futurs)
INSERT INTO trajets (conducteur_id, ville_depart, ville_arrivee, adresse_depart, adresse_arrivee, date, heure_depart, nbr_places, places_disponibles, price, price_platform, price_driver, distance, fuel_type, fuel_consumption, wilaya_depart, status, description, is_confort) VALUES
-- Trajet 1: Alger → Oran (Karim)
(2, 'Alger', 'Oran', 'Place des Martyrs, Alger Centre', 'Place du 1er Novembre, Oran', CURRENT_DATE + INTERVAL '2 days', '08:00:00', 3, 3, 1500.00, 225.00, 1275.00, 432, 'gasoil', 7.5, 'Alger', 'ACTIVE', 'Trajet direct sans arrêt intermédiaire, véhicule confortable climatisé', false),

-- Trajet 2: Alger → Constantine (Fatima)
(3, 'Alger', 'Constantine', 'Bab Ezzouar, Alger', 'Centre-ville Constantine', CURRENT_DATE + INTERVAL '3 days', '06:30:00', 3, 3, 2000.00, 300.00, 1700.00, 431, 'gasoil', 8.0, 'Alger', 'ACTIVE', 'Départ tôt le matin, possibilité d\'arrêt café', false),

-- Trajet 3: Alger → Blida (Sarah - quotidien)
(5, 'Alger', 'Blida', 'Kouba, Alger', 'Centre-ville Blida', CURRENT_DATE + INTERVAL '1 days', '07:30:00', 2, 2, 300.00, 45.00, 255.00, 50, 'essence_sans_plomb', 6.5, 'Alger', 'ACTIVE', 'Trajet quotidien pour travail, ponctualité garantie', false),

-- Trajet 4: Oran → Alger (Yacine)
(4, 'Oran', 'Alger', 'Sidi El Houari, Oran', 'Hydra, Alger', CURRENT_DATE + INTERVAL '4 days', '14:00:00', 3, 3, 1600.00, 240.00, 1360.00, 432, 'gasoil', 7.8, 'Oran', 'ACTIVE', 'Retour d\'un déplacement professionnel', false),

-- Trajet 5: Constantine → Annaba (Mehdi)
(6, 'Constantine', 'Annaba', 'Université Mentouri', 'Port d\'Annaba', CURRENT_DATE + INTERVAL '5 days', '09:00:00', 3, 3, 800.00, 120.00, 680.00, 110, 'electrique', 15.0, 'Constantine', 'ACTIVE', 'Véhicule électrique, trajet écologique', false),

-- Trajet 6: Alger → Oran CONFORT (Karim)
(2, 'Alger', 'Oran', 'Cheraga, Alger', 'Es Senia, Oran', CURRENT_DATE + INTERVAL '6 days', '10:00:00', 2, 2, 2000.00, 300.00, 1700.00, 432, 'gasoil', 7.5, 'Alger', 'ACTIVE', 'Trajet confort avec véhicule haut de gamme, sièges en cuir, WiFi à bord', true),

-- Trajet 7: Blida → Alger (Sarah - retour)
(5, 'Blida', 'Alger', 'Hopital Frantz Fanon, Blida', 'Bab Ezzouar, Alger', CURRENT_DATE + INTERVAL '1 days', '17:00:00', 2, 2, 300.00, 45.00, 255.00, 50, 'essence_sans_plomb', 6.5, 'Blida', 'ACTIVE', 'Retour du travail en fin d\'après-midi', false);

-- Trajets complétés (passés)
INSERT INTO trajets (conducteur_id, ville_depart, ville_arrivee, adresse_depart, adresse_arrivee, date, heure_depart, nbr_places, places_disponibles, price, price_platform, price_driver, distance, fuel_type, fuel_consumption, wilaya_depart, status, description) VALUES
(2, 'Alger', 'Oran', 'Bab Ezzouar', 'Centre-ville Oran', CURRENT_DATE - INTERVAL '10 days', '08:00:00', 3, 0, 1500.00, 225.00, 1275.00, 432, 'gasoil', 7.5, 'Alger', 'COMPLETED', 'Trajet terminé avec succès'),
(3, 'Alger', 'Constantine', 'Hydra', 'Université Constantine', CURRENT_DATE - INTERVAL '15 days', '07:00:00', 3, 0, 2000.00, 300.00, 1700.00, 431, 'gasoil', 8.0, 'Alger', 'COMPLETED', 'Trajet terminé'),
(4, 'Oran', 'Alger', 'Es Senia', 'Alger Centre', CURRENT_DATE - INTERVAL '8 days', '15:00:00', 3, 0, 1600.00, 240.00, 1360.00, 432, 'gasoil', 7.8, 'Oran', 'COMPLETED', 'Retour professionnel');

-- ========================================
-- 7. PRÉFÉRENCES DES TRAJETS
-- ========================================
-- Trajet 1 (Karim: Alger → Oran)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(1, 1), (1, 7), (1, 11), (1, 13);

-- Trajet 2 (Fatima: Alger → Constantine)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(2, 3), (2, 7), (2, 10), (2, 11);

-- Trajet 3 (Sarah: Alger → Blida)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(3, 7), (3, 10), (3, 11);

-- Trajet 4 (Yacine: Oran → Alger)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(4, 1), (4, 4), (4, 7), (4, 9);

-- Trajet 5 (Mehdi: Constantine → Annaba)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(5, 4), (5, 7), (5, 12);

-- Trajet 6 (Karim CONFORT: Alger → Oran)
INSERT INTO trajets_preferences (trajet_id, preference_id) VALUES
(6, 1), (6, 7), (6, 11), (6, 12), (6, 13), (6, 14);

-- ========================================
-- 8. ÉTAPES DE TRAJETS
-- ========================================
-- Trajet 1: Alger → Oran (avec étape à Chlef)
INSERT INTO trajet_etapes (trajet_id, ville, adresse, heure_arrivee, ordre) VALUES
(1, 'Chlef', 'Centre-ville Chlef', '10:30:00', 1);

-- Trajet 2: Alger → Constantine (avec étapes)
INSERT INTO trajet_etapes (trajet_id, ville, adresse, heure_arrivee, ordre) VALUES
(2, 'Bouira', 'Gare routière Bouira', '08:30:00', 1),
(2, 'Sétif', 'Place de l\'indépendance', '10:00:00', 2);

-- ========================================
-- 9. RÉSERVATIONS
-- ========================================
-- Réservations pour trajets futurs (PENDING et CONFIRMED)
INSERT INTO reservations (trajet_id, passager_id, nbr_places, status, price_per_seat, total_price, created_at) VALUES
-- Trajet 1 (Alger → Oran): 1 réservation confirmée
(1, 7, 2, 'CONFIRMED', 1500.00, 3000.00, CURRENT_TIMESTAMP - INTERVAL '1 day'),

-- Trajet 2 (Alger → Constantine): 2 réservations (1 pending, 1 confirmed)
(2, 8, 1, 'CONFIRMED', 2000.00, 2000.00, CURRENT_TIMESTAMP - INTERVAL '2 days'),
(2, 9, 1, 'PENDING', 2000.00, 2000.00, CURRENT_TIMESTAMP - INTERVAL '6 hours'),

-- Trajet 3 (Alger → Blida): 1 réservation confirmée
(3, 10, 1, 'CONFIRMED', 300.00, 300.00, CURRENT_TIMESTAMP - INTERVAL '12 hours'),

-- Trajet 4 (Oran → Alger): 1 réservation pending
(4, 11, 2, 'PENDING', 1600.00, 3200.00, CURRENT_TIMESTAMP - INTERVAL '3 hours'),

-- Trajet 6 (CONFORT): 1 réservation confirmée
(6, 7, 1, 'CONFIRMED', 2000.00, 2000.00, CURRENT_TIMESTAMP - INTERVAL '5 hours');

-- Réservations pour trajets complétés
INSERT INTO reservations (trajet_id, passager_id, nbr_places, status, price_per_seat, total_price, created_at, approved_at) VALUES
(8, 7, 2, 'CONFIRMED', 1500.00, 3000.00, CURRENT_DATE - INTERVAL '12 days', CURRENT_DATE - INTERVAL '11 days'),
(8, 8, 1, 'CONFIRMED', 1500.00, 1500.00, CURRENT_DATE - INTERVAL '12 days', CURRENT_DATE - INTERVAL '11 days'),
(9, 9, 2, 'CONFIRMED', 2000.00, 4000.00, CURRENT_DATE - INTERVAL '16 days', CURRENT_DATE - INTERVAL '16 days'),
(10, 10, 1, 'CONFIRMED', 1600.00, 1600.00, CURRENT_DATE - INTERVAL '9 days', CURRENT_DATE - INTERVAL '9 days');

-- Mettre à jour places_disponibles
UPDATE trajets SET places_disponibles = 1 WHERE id = 1;
UPDATE trajets SET places_disponibles = 1 WHERE id = 2;
UPDATE trajets SET places_disponibles = 1 WHERE id = 3;
UPDATE trajets SET places_disponibles = 1 WHERE id = 6;

-- ========================================
-- 10. ÉVALUATIONS (RATINGS)
-- ========================================
-- Évaluations pour le trajet 8 (complété)
INSERT INTO ratings (reservation_id, rater_id, rated_id, note, comment, ponctualite, convivialite, conduite, created_at) VALUES
-- Amina note Karim (conducteur)
(7, 7, 2, 5, 'Excellent conducteur, très ponctuel et agréable. Trajet très confortable!', 5, 5, 5, CURRENT_DATE - INTERVAL '9 days'),
-- Karim note Amina (passagère)
(7, 2, 7, 5, 'Passagère très sympathique et ponctuelle. Recommandé!', 5, 5, NULL, CURRENT_DATE - INTERVAL '9 days'),
-- Riad note Karim
(8, 8, 2, 5, 'Conduite sécurisée, bonne ambiance!', 5, 4, 5, CURRENT_DATE - INTERVAL '9 days'),
-- Karim note Riad
(8, 2, 8, 5, 'Passager agréable, à recommander', 5, 5, NULL, CURRENT_DATE - INTERVAL '9 days');

-- Évaluations pour le trajet 9
INSERT INTO ratings (reservation_id, rater_id, rated_id, note, comment, ponctualite, convivialite, conduite) VALUES
-- Leila note Fatima
(9, 9, 3, 5, 'Excellente conductrice, très professionnelle', 5, 5, 5),
-- Fatima note Leila
(9, 3, 9, 5, 'Passagère parfaite!', 5, 5, NULL);

-- Évaluations pour le trajet 10
INSERT INTO ratings (reservation_id, rater_id, rated_id, note, comment, ponctualite, convivialite, conduite) VALUES
-- Nassim note Yacine
(10, 10, 4, 4, 'Bon trajet, quelques retards mineurs', 4, 5, 5),
-- Yacine note Nassim
(10, 4, 10, 5, 'Excellent passager', 5, 5, NULL);

-- ========================================
-- 11. CONVERSATIONS
-- ========================================
INSERT INTO conversations (trajet_id, is_group, created_at) VALUES
-- Conversation de groupe pour trajet 1
(1, true, CURRENT_TIMESTAMP - INTERVAL '1 day'),
-- Conversation de groupe pour trajet 2
(2, true, CURRENT_TIMESTAMP - INTERVAL '2 days'),
-- Conversation privée Karim-Amina
(NULL, false, CURRENT_TIMESTAMP - INTERVAL '3 days');

-- Participants aux conversations
INSERT INTO conversations_participants (conversation_id, user_id) VALUES
-- Conversation groupe trajet 1
(1, 2), (1, 7),
-- Conversation groupe trajet 2
(2, 3), (2, 8), (2, 9),
-- Conversation privée
(3, 2), (3, 7);

-- ========================================
-- 12. MESSAGES
-- ========================================
INSERT INTO messagerie (sender_id, receiver_id, trajet_id, conversation_id, text, is_group_message, is_read, created_at) VALUES
-- Messages du groupe trajet 1
(2, NULL, 1, 1, 'Bonjour à tous! Rendez-vous à 8h précises Place des Martyrs.', true, true, CURRENT_TIMESTAMP - INTERVAL '1 day'),
(7, NULL, 1, 1, 'Parfait, je serai là! Merci', true, true, CURRENT_TIMESTAMP - INTERVAL '23 hours'),

-- Messages du groupe trajet 2
(3, NULL, 2, 2, 'Bonjour, départ prévu à 6h30. N\'oubliez pas vos pièces d\'identité.', true, true, CURRENT_TIMESTAMP - INTERVAL '2 days'),
(8, NULL, 2, 2, 'Merci pour l\'info!', true, true, CURRENT_TIMESTAMP - INTERVAL '47 hours'),
(9, NULL, 2, 2, 'Est-ce qu\'on peut faire un arrêt café à Bouira?', true, false, CURRENT_TIMESTAMP - INTERVAL '5 hours'),

-- Messages privés
(7, 2, NULL, 3, 'Bonjour, est-ce que vous avez de la place pour des bagages?', false, true, CURRENT_TIMESTAMP - INTERVAL '3 days'),
(2, 7, NULL, 3, 'Oui bien sûr, pas de problème pour les bagages!', false, true, CURRENT_TIMESTAMP - INTERVAL '3 days');

-- ========================================
-- 13. NOTIFICATIONS
-- ========================================
INSERT INTO notifications (recipient_id, sender_id, type, content, related_model, related_id, is_read, created_at) VALUES
-- Notifications pour Karim (conducteur)
(2, 7, 'RESERVATION_REQUEST', 'Amina Kaci a demandé à réserver 2 places pour votre trajet Alger → Oran', 'Reservation', 1, true, CURRENT_TIMESTAMP - INTERVAL '1 day'),
(2, 11, 'RESERVATION_REQUEST', 'Samia Lakhal a demandé à réserver 2 places pour votre trajet Oran → Alger', 'Reservation', 5, false, CURRENT_TIMESTAMP - INTERVAL '3 hours'),

-- Notifications pour Fatima
(3, 8, 'RESERVATION_REQUEST', 'Riad Mansouri a demandé à réserver 1 place pour votre trajet Alger → Constantine', 'Reservation', 2, true, CURRENT_TIMESTAMP - INTERVAL '2 days'),
(3, 9, 'RESERVATION_REQUEST', 'Leila Cherif a demandé à réserver 1 place pour votre trajet Alger → Constantine', 'Reservation', 3, false, CURRENT_TIMESTAMP - INTERVAL '6 hours'),

-- Notifications pour passagers
(7, 2, 'RESERVATION_APPROVED', 'Votre réservation pour le trajet Alger → Oran a été approuvée', 'Reservation', 1, true, CURRENT_TIMESTAMP - INTERVAL '23 hours'),
(8, 3, 'RESERVATION_APPROVED', 'Votre réservation pour le trajet Alger → Constantine a été approuvée', 'Reservation', 2, true, CURRENT_TIMESTAMP - INTERVAL '47 hours'),
(10, 5, 'RESERVATION_APPROVED', 'Votre réservation pour le trajet Alger → Blida a été approuvée', 'Reservation', 4, true, CURRENT_TIMESTAMP - INTERVAL '11 hours'),

-- Notifications de bienvenue
(7, NULL, 'WELCOME', 'Bienvenue sur DZ-CarPool! Commencez à rechercher des trajets.', NULL, NULL, true, CURRENT_TIMESTAMP - INTERVAL '30 days'),
(8, NULL, 'WELCOME', 'Bienvenue sur DZ-CarPool! Commencez à rechercher des trajets.', NULL, NULL, true, CURRENT_TIMESTAMP - INTERVAL '25 days');

-- ========================================
-- 14. DOCUMENTS UTILISATEURS
-- ========================================
INSERT INTO user_documents (user_id, document_type, file_path, verified, verified_by_id, verified_at) VALUES
-- Documents vérifiés des conducteurs
(2, 'PERMIS', 'documents/karim_permis.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '20 days'),
(2, 'CNI', 'documents/karim_cni.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '20 days'),
(3, 'PERMIS', 'documents/fatima_permis.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '18 days'),
(3, 'CNI', 'documents/fatima_cni.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '18 days'),
(4, 'PERMIS', 'documents/yacine_permis.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '15 days'),
(4, 'CNI', 'documents/yacine_cni.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '15 days'),
(5, 'PERMIS', 'documents/sarah_permis.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '22 days'),
(5, 'CNI', 'documents/sarah_cni.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '22 days'),
(6, 'PERMIS', 'documents/mehdi_permis.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '10 days'),
(6, 'CNI', 'documents/mehdi_cni.pdf', true, 1, CURRENT_TIMESTAMP - INTERVAL '10 days'),

-- Documents en attente de vérification
(7, 'CNI', 'documents/amina_cni.pdf', false, NULL, NULL),
(8, 'CNI', 'documents/riad_cni.pdf', false, NULL, NULL);

-- ========================================
-- RÉSUMÉ DU JEU DE DONNÉES
-- ========================================
-- 
-- ✅ 11 utilisateurs (1 admin, 5 conducteurs, 5 passagers)
-- ✅ 4 rôles
-- ✅ 15 préférences (catégorisées)
-- ✅ 10 trajets (7 actifs, 3 complétés)
-- ✅ 5 wilayas avec prix carburant
-- ✅ 10 réservations (6 pour trajets futurs, 4 pour trajets passés)
-- ✅ 6 évaluations (notes de 4 à 5 étoiles)
-- ✅ 3 conversations (2 groupes, 1 privée)
-- ✅ 6 messages
-- ✅ 8 notifications
-- ✅ 14 documents (12 vérifiés, 2 en attente)
--
-- Scénarios testables:
-- 1. Recherche de trajets actifs
-- 2. Réservation de places (pending/confirmed)
-- 3. Système d'évaluation après trajet
-- 4. Messagerie individuelle et de groupe
-- 5. Notifications multi-types
-- 6. Vérification de documents
-- 7. Calcul des prix avec commission
-- 8. Gestion des préférences utilisateurs/trajets
-- 9. Historique des trajets complétés
-- 10. Statistiques utilisateurs (ratings, nombre de trajets)
-- ========================================

