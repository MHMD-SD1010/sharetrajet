-- ================================================
-- INITIALISATION COMPLÈTE BASE DE DONNÉES
-- DZ-CarPool
-- ================================================
-- Exécution recommandée:
-- psql -U <user> -d <database> -f 00_init_complete_database.sql

\echo '>> 1/5 - Création tables utilisateurs'
\i 01_users_tables.sql

\echo '>> 2/5 - Création tables trajets'
\i 02_trajets_tables.sql

\echo '>> 3/5 - Création tables réservations'
\i 03_reservations_tables.sql

\echo '>> 4/5 - Création tables messaging/notifications'
\i 04_notifications_tables.sql

\echo '>> 5/5 - Seeding données de test'
\i 05_seeding_data.sql

\echo '>> Initialisation terminée.'
