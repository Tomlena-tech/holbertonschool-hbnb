# 📊 Scripts SQL - Task 9 : Data Validation

Ce dossier contient les scripts SQL pour créer et tester la base de données MySQL avec toutes les validations de la Task 9.

---

## 📁 Fichiers

1. **`sql_scripts_task9.sql`** - Script principal de création de la base de données
2. **`sql_tests_validation.sql`** - Tests de validation (27 tests)

---

## 🚀 Utilisation

### **Étape 1 : Créer la Base de Données**

```bash
# Se connecter à MySQL
mysql -u root -p

# Exécuter le script de création
mysql -u root -p < sql_scripts_task9.sql

# Ou dans MySQL :
SOURCE /chemin/vers/sql_scripts_task9.sql;
```

**Ce que fait ce script** :
- ✅ Crée la base de données `hbnb_prod`
- ✅ Crée les 5 tables (users, places, reviews, amenities, place_amenity)
- ✅ Ajoute toutes les contraintes (PK, FK, UK, CHECK)
- ✅ Crée les index pour les performances
- ✅ Crée un trigger pour empêcher les self-reviews
- ✅ Crée des vues utiles
- ✅ Insère des données de test

---

### **Étape 2 : Tester les Validations**

```bash
# Exécuter les tests de validation
mysql -u root -p hbnb_prod < sql_tests_validation.sql
```

**Ce que fait ce script** :
- ✅ Teste toutes les validations
- ✅ Teste les erreurs attendues
- ✅ Teste les cascade deletes
- ✅ Affiche un récapitulatif

---

## 📋 Validations Implémentées

### **1. TABLE USERS**

| Validation | Contrainte | Description |
|-----------|-----------|-------------|
| Email format | `chk_email_format` | Regex : `^[^@]+@[^@]+\.[^@]+$` |
| Email unique | `uk_users_email` | Pas de doublons |
| Email longueur | `chk_email_length` | Max 120 caractères |
| first_name longueur | `chk_first_name_length` | Max 50 caractères |
| last_name longueur | `chk_last_name_length` | Max 50 caractères |
| password_hash longueur | `chk_password_hash_length` | Max 128 caractères |

---

### **2. TABLE PLACES**

| Validation | Contrainte | Description |
|-----------|-----------|-------------|
| Title non-vide | `chk_title_not_empty` | CHAR_LENGTH > 0 |
| Title longueur | `chk_title_length` | Max 100 caractères |
| Prix positif | `chk_price_positive` | price >= 0 |
| Latitude plage | `chk_latitude_range` | -90.0 à 90.0 |
| Longitude plage | `chk_longitude_range` | -180.0 à 180.0 |
| Owner existe | `fk_places_owner` | Foreign key vers users |

---

### **3. TABLE REVIEWS**

| Validation | Contrainte | Description |
|-----------|-----------|-------------|
| Text non-vide | `chk_text_not_empty` | CHAR_LENGTH > 0 |
| Rating plage | `chk_rating_range` | 1 à 5 |
| No duplicate review | `uk_reviews_user_place` | Un seul review par user/place |
| No self-review | `trg_prevent_self_review` | Trigger (user ≠ owner) |
| Place existe | `fk_reviews_place` | Foreign key vers places |
| User existe | `fk_reviews_user` | Foreign key vers users |

---

### **4. TABLE AMENITIES**

| Validation | Contrainte | Description |
|-----------|-----------|-------------|
| Name non-vide | `chk_amenity_name_not_empty` | CHAR_LENGTH > 0 |
| Name longueur | `chk_amenity_name_length` | Max 50 caractères |
| Name unique | `uk_amenities_name` | Pas de doublons |

---

## 🧪 Tests Inclus (27 tests)

### **Tests USERS (6 tests)**
1. ✅ Insertion valide
2. ❌ Email sans @
3. ❌ Email sans domaine
4. ❌ Email duplicate
5. ❌ first_name trop long
6. ❌ last_name trop long

### **Tests PLACES (9 tests)**
7. ✅ Insertion valide
8. ❌ Title vide
9. ❌ Title trop long
10. ❌ Prix négatif
11. ❌ Latitude > 90
12. ❌ Latitude < -90
13. ❌ Longitude > 180
14. ❌ Longitude < -180
15. ❌ owner_id inexistant

### **Tests REVIEWS (6 tests)**
16. ✅ Insertion valide
17. ❌ Text vide
18. ❌ Rating < 1
19. ❌ Rating > 5
20. ❌ Duplicate review
21. ❌ Self-review

### **Tests AMENITIES (4 tests)**
22. ✅ Insertion valide
23. ❌ Name duplicate
24. ❌ Name vide
25. ❌ Name trop long

### **Tests CASCADE DELETE (2 tests)**
26. ✅ User supprimé → Places supprimés
27. ✅ Place supprimé → Reviews supprimés

---

## 📊 Vues Créées

### **v_user_statistics**
Vue qui montre chaque user avec :
- Nombre de places possédés
- Nombre de reviews écrits
- Informations du user

**Utilisation** :
```sql
SELECT * FROM v_user_statistics;
```

---

### **v_place_statistics**
Vue qui montre chaque place avec :
- Nom du propriétaire
- Nombre de reviews
- Note moyenne
- Nombre d'amenities

**Utilisation** :
```sql
SELECT * FROM v_place_statistics;
```

---

## 🔧 Requêtes Utiles

### **Vérifier les contraintes**
```sql
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'hbnb_prod'
ORDER BY TABLE_NAME;
```

---

### **Vérifier les foreign keys**
```sql
SELECT
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'hbnb_prod'
    AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

### **Vérifier les CHECK constraints**
```sql
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CHECK_CLAUSE
FROM information_schema.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'hbnb_prod';
```

---

## ⚠️ Notes Importantes

### **Versions MySQL**

**CHECK Constraints** :
- ✅ MySQL 8.0.16+ : Supporté
- ❌ MySQL < 8.0.16 : Pas supporté (ignorés silencieusement)

**Vérifier votre version** :
```bash
mysql --version
```

Si version < 8.0.16, les validations de plage (rating, latitude, etc.) ne seront PAS appliquées au niveau database (seulement au niveau application).

---

### **Trigger pour Self-Review**

Le trigger `trg_prevent_self_review` empêche un user de reviewer son propre place **au niveau database**.

**Test** :
```sql
-- Créer un user
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('owner-123', 'Owner', 'Test', 'owner@test.com', 'hash', FALSE);

-- Créer son place
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES ('place-123', 'My Place', 100, 0, 0, 'owner-123');

-- Essayer de reviewer son propre place
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Great!', 5, 'place-123', 'owner-123');

-- ❌ Erreur : Cannot review your own place
```

---

### **Cascade Delete**

**Configuration** :
```sql
FOREIGN KEY (owner_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```

**Comportement** :
- Si user supprimé → Tous ses places supprimés
- Si place supprimé → Tous ses reviews supprimés
- Si user supprimé → Tous ses reviews supprimés

---

## 🎯 Données de Test Incluses

### **Admin User**
```
Email: admin@hbnb.com
Password: admin123 (hash bcrypt)
is_admin: TRUE
```

### **User Régulier**
```
Email: john@example.com
Password: admin123 (hash bcrypt)
is_admin: FALSE
```

### **Amenities**
- WiFi
- Parking
- Pool
- Air Conditioning

---

## 🔍 Debugging

### **Vérifier si une contrainte existe**
```sql
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'hbnb_prod'
    AND TABLE_NAME = 'users';
```

---

### **Vérifier les triggers**
```sql
SHOW TRIGGERS FROM hbnb_prod;
```

---

### **Activer les logs d'erreurs**
```sql
-- Voir les warnings
SHOW WARNINGS;

-- Voir les erreurs
SHOW ERRORS;
```

---

## 📚 Ressources

- [MySQL CHECK Constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
- [MySQL Foreign Keys](https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html)
- [MySQL Triggers](https://dev.mysql.com/doc/refman/8.0/en/triggers.html)
- [MySQL UNIQUE Constraints](https://dev.mysql.com/doc/refman/8.0/en/constraint-unique.html)

---

## ✅ Checklist de Vérification

Après avoir exécuté les scripts :

- [ ] Base de données `hbnb_prod` créée
- [ ] 5 tables créées (users, places, reviews, amenities, place_amenity)
- [ ] Toutes les contraintes actives (CHECK, FK, UK)
- [ ] Trigger `trg_prevent_self_review` créé
- [ ] 2 vues créées (v_user_statistics, v_place_statistics)
- [ ] Admin user créé
- [ ] 4 amenities créés
- [ ] Tous les tests passent

**Vérification finale** :
```sql
SELECT TABLE_NAME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'hbnb_prod';

SELECT * FROM users WHERE is_admin = TRUE;

SELECT * FROM amenities;
```

---

**Créé le** : 2025-11-08
**Par** : Thomas
**Projet** : HBnB Evolution - Part 3
