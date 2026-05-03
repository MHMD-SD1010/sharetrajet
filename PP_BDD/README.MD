# 🚗 DZ-CarPool - Documentation Base de Données

## 📋 Vue d'ensemble

Cette documentation décrit la structure de la base de données PostgreSQL pour l'application DZ-CarPool et fournit les scripts SQL d'initialisation et de seeding.

## 📁 Structure des fichiers SQL

```
database/
├── 00_init_complete_database.sql  # Script principal d'initialisation
├── 01_users_tables.sql            # Tables module utilisateurs
├── 02_trajets_tables.sql          # Tables module trajets
├── 03_reservations_tables.sql     # Tables module réservations
├── 04_notifications_tables.sql    # Tables module notifications
├── 05_seeding_data.sql            # Données de test
└── README_DATABASE.md             # Cette documentation
```

## 🚀 Installation rapide

### Option 1: Script complet (recommandé)

```bash
# Créer la base de données
createdb dzcarpool

# Exécuter le script complet
psql -U postgres -d dzcarpool -f 00_init_complete_database.sql
```

### Option 2: Étape par étape

```bash
# Créer la base de données
createdb dzcarpool

# Exécuter les scripts dans l'ordre
psql -U postgres -d dzcarpool -f 01_users_tables.sql
psql -U postgres -d dzcarpool -f 02_trajets_tables.sql
psql -U postgres -d dzcarpool -f 03_reservations_tables.sql
psql -U postgres -d dzcarpool -f 04_notifications_tables.sql
psql -U postgres -d dzcarpool -f 05_seeding_data.sql
```

### Option 3: Avec Docker

```bash
# Démarrer PostgreSQL
docker run --name dzcarpool-db \
  -e POSTGRES_DB=dzcarpool \
  -e POSTGRES_USER=dzcarpool \
  -e POSTGRES_PASSWORD=dzcarpool123 \
  -p 5432:5432 \
  -d postgres:15

# Attendre que PostgreSQL soit prêt
sleep 5

# Exécuter les scripts
docker exec -i dzcarpool-db psql -U dzcarpool -d dzcarpool < 00_init_complete_database.sql
```

## 📊 Structure de la base de données

### Module Users (01_users_tables.sql)

#### Tables principales:
- **users**: Utilisateurs de la plateforme
- **roles**: Rôles (Passager, Conducteur, Admin)
- **preferences**: Préférences utilisateurs (musique, non-fumeur, etc.)
- **user_documents**: Documents d'identité et permis
- **refresh_tokens**: Tokens d'authentification
- **email_verifications**: Codes de vérification email
- **phone_verifications**: Codes de vérification téléphone

#### Relations:
- users ↔ preferences (many-to-many)
- users → roles (many-to-one)
- users → user_documents (one-to-many)

### Module Trajets (02_trajets_tables.sql)

#### Tables principales:
- **trajets**: Trajets de covoiturage
- **trajet_etapes**: Étapes intermédiaires des trajets
- **trajets_preferences**: Préférences par trajet
- **fuel_prices**: Prix du carburant par wilaya

#### Caractéristiques:
- Calcul automatique commission plateforme (15%)
- Supplément confort (+30%)
- Pause obligatoire pour trajets > 300km
- Support multi-carburant (essence, gasoil, GPL, électrique)

### Module Réservations (03_reservations_tables.sql)

#### Tables principales:
- **reservations**: Réservations de places
- **ratings**: Évaluations mutuelles (1-5 étoiles)

#### Statuts de réservation:
- `PENDING`: En attente d'approbation
- `CONFIRMED`: Confirmée par le conducteur
- `REJECTED`: Refusée
- `CANCELLED`: Annulée

#### Triggers automatiques:
- Mise à jour des places disponibles
- Calcul de la moyenne des ratings
- Mise à jour des statistiques utilisateur

### Module Notifications (04_notifications_tables.sql)

#### Tables principales:
- **messagerie**: Messages entre utilisateurs
- **conversations**: Conversations privées et de groupe
- **notifications**: Notifications système

#### Types de notifications:
- Demandes de réservation
- Approbations/Rejets
- Messages reçus
- Modifications de trajet
- Évaluations reçues
- Vérifications de documents

## 🎲 Données de test (05_seeding_data.sql)

### Utilisateurs créés:

| Email | Rôle | Password | Description |
|-------|------|----------|-------------|
| admin@dzcarpool.dz | Admin | password123 | Administrateur principal |
| karim.mohamed@email.dz | Conducteur | password123 | Trajets Alger-Oran réguliers |
| fatima.zahir@email.dz | Conducteur | password123 | Trajets Alger-Constantine |
| yacine.hamdi@email.dz | Conducteur | password123 | Commercial, nombreux trajets |
| sarah.djebar@email.dz | Conducteur | password123 | Trajets quotidiens Alger-Blida |
| mehdi.brahimi@email.dz | Conducteur | password123 | Conduite écologique (électrique) |
| amina.kaci@email.dz | Passager | password123 | Étudiante en médecine |
| riad.mansouri@email.dz | Passager | password123 | Développeur freelance |
| leila.cherif@email.dz | Passager | password123 | Journaliste |
| nassim.bouaziz@email.dz | Passager | password123 | Chef de projet |
| samia.lakhal@email.dz | Passager | password123 | Architecte |

### Données de test:

✅ **11 utilisateurs** (1 admin, 5 conducteurs, 5 passagers)  
✅ **4 rôles** système  
✅ **15 préférences** (catégorisées: intérêts, habitudes, conduite)  
✅ **10 trajets** (7 actifs futurs, 3 complétés)  
✅ **5 wilayas** avec prix carburant réels  
✅ **10 réservations** (6 pour trajets futurs, 4 complétés)  
✅ **6 évaluations** (notes de 4 à 5 étoiles)  
✅ **3 conversations** (2 groupes, 1 privée)  
✅ **6 messages** échangés  
✅ **8 notifications** diverses  
✅ **14 documents** (12 vérifiés, 2 en attente)

### Trajets de test disponibles:

1. **Alger → Oran** (Karim) - Dans 2 jours - 1500 DA - 3 places
2. **Alger → Constantine** (Fatima) - Dans 3 jours - 2000 DA - 3 places
3. **Alger → Blida** (Sarah) - Demain - 300 DA - 2 places (quotidien)
4. **Oran → Alger** (Yacine) - Dans 4 jours - 1600 DA - 3 places
5. **Constantine → Annaba** (Mehdi) - Dans 5 jours - 800 DA - Électrique
6. **Alger → Oran CONFORT** (Karim) - Dans 6 jours - 2000 DA - Luxe
7. **Blida → Alger** (Sarah) - Demain soir - 300 DA - Retour travail

## 🔍 Requêtes utiles pour tester

### Statistiques globales
```sql
-- Nombre total d'utilisateurs par rôle
SELECT r.name, COUNT(u.id) as count
FROM users u
JOIN roles r ON u.role_id = r.id
GROUP BY r.name;

-- Trajets actifs avec places disponibles
SELECT 
    ville_depart || ' → ' || ville_arrivee as trajet,
    date,
    heure_depart,
    places_disponibles,
    price
FROM trajets
WHERE status = 'ACTIVE' AND places_disponibles > 0
ORDER BY date;
```

### Recherche de trajets
```sql
-- Rechercher trajets Alger → Oran
SELECT 
    t.id,
    u.first_name || ' ' || u.last_name as conducteur,
    t.date,
    t.heure_depart,
    t.places_disponibles,
    t.price,
    u.average_rating
FROM trajets t
JOIN users u ON t.conducteur_id = u.id
WHERE t.ville_depart = 'Alger'
  AND t.ville_arrivee = 'Oran'
  AND t.status = 'ACTIVE'
  AND t.places_disponibles > 0
ORDER BY t.date, t.heure_depart;
```

### Réservations utilisateur
```sql
-- Voir toutes les réservations d'un utilisateur
SELECT 
    r.id,
    t.ville_depart || ' → ' || t.ville_arrivee as trajet,
    t.date,
    r.nbr_places,
    r.total_price,
    r.status,
    u.first_name || ' ' || u.last_name as conducteur
FROM reservations r
JOIN trajets t ON r.trajet_id = t.id
JOIN users u ON t.conducteur_id = u.id
WHERE r.passager_id = 7 -- Amina
ORDER BY t.date DESC;
```

### Évaluations et statistiques
```sql
-- Top conducteurs par note
SELECT 
    u.first_name || ' ' || u.last_name as conducteur,
    u.average_rating,
    u.trips_as_driver,
    COUNT(DISTINCT r.id) as total_ratings
FROM users u
LEFT JOIN ratings r ON r.rated_id = u.id
WHERE u.role_id = 2 -- Conducteurs
GROUP BY u.id, u.first_name, u.last_name, u.average_rating, u.trips_as_driver
ORDER BY u.average_rating DESC;
```

### Messages et notifications
```sql
-- Messages non lus pour un utilisateur
SELECT 
    sender.first_name || ' ' || sender.last_name as expediteur,
    m.text,
    m.created_at
FROM messagerie m
JOIN users sender ON m.sender_id = sender.id
WHERE m.receiver_id = 2 -- Karim
  AND m.is_read = false
ORDER BY m.created_at DESC;

-- Notifications non lues
SELECT type, content, created_at
FROM notifications
WHERE recipient_id = 2
  AND is_read = false
ORDER BY created_at DESC;
```

## 🛠️ Maintenance

### Réinitialiser les données
```sql
-- Supprimer toutes les données mais garder la structure
TRUNCATE TABLE ratings, reservations, notifications, messagerie, 
                conversations_participants, conversations, trajet_etapes, 
                trajets_preferences, trajets, fuel_prices, users_preferences, 
                user_documents, refresh_tokens, email_verifications, 
                phone_verifications, users, preferences, roles 
RESTART IDENTITY CASCADE;

-- Puis réexécuter le seeding
\i 05_seeding_data.sql
```

### Backup
```bash
# Sauvegarder la base
pg_dump -U postgres dzcarpool > backup_dzcarpool_$(date +%Y%m%d).sql

# Restaurer depuis un backup
psql -U postgres dzcarpool < backup_dzcarpool_20250101.sql
```

## 📱 Intégration avec Django

Ces scripts SQL créent les mêmes tables que les models Django fournis. Pour synchroniser:

```bash
# Si vous utilisez Django, pas besoin d'exécuter les scripts SQL
python manage.py makemigrations
python manage.py migrate

# Pour charger uniquement les données de test
python manage.py shell
# Puis copier le contenu de 05_seeding_data.sql adapté en Python
```

## 🔐 Sécurité

⚠️ **IMPORTANT**: Les mots de passe dans le seeding sont des exemples!

- Mot de passe par défaut: `password123`
- Hash bcrypt utilisé: `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7DSQNZ6ppe`
- En production, utilisez des mots de passe forts et uniques

## 📞 Support

Pour toute question sur la structure de la base de données:
- Consultez les commentaires dans chaque fichier SQL
- Vérifiez les contraintes et indexes pour comprendre les relations
- Utilisez `\d+ nom_table` dans psql pour voir les détails d'une table

## 📄 License

Ce schéma de base de données est conçu pour le projet DZ-CarPool.