# 🧪 GUIDE COMPLET DES TESTS - HBnB Part 3

**Date**: 2025-11-07
**Objectif**: Tester toutes les fonctionnalités Part 3 (JWT, Database, Authorization)

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#prérequis)
2. [Tests JWT Authentication](#tests-jwt-authentication)
3. [Tests Authorization (Role-based)](#tests-authorization)
4. [Tests CRUD avec Database](#tests-crud-database)
5. [Tests Relations Database](#tests-relations)
6. [Tests Business Rules](#tests-business-rules)
7. [Tests Validation](#tests-validation)
8. [Tests Production MySQL](#tests-mysql)
9. [Checklist Complète](#checklist)

---

## 🔧 PRÉREQUIS

### 1. Lancer l'Application

```bash
cd part3/hbnb
python run.py
```

**Vérifier** :
```
* Running on http://127.0.0.1:5000
* Swagger UI: http://127.0.0.1:5000/api/v1/docs
```

### 2. Variables d'Environnement

```bash
# Copier .env.example vers .env
cp .env.example .env

# Éditer si nécessaire
nano .env
```

### 3. Base de Données

```bash
# Vérifier que la DB existe
ls -la instance/hbnb_dev.db

# Si elle n'existe pas, elle sera créée au démarrage
```

---

## 🔐 TESTS JWT AUTHENTICATION

### TEST 1 : Créer un Admin (Premier User)

**Objectif**: Créer le premier utilisateur admin via script

```bash
cd part3/hbnb
python create_admin.py
```

**Résultat attendu**:
```
Admin user created successfully!
Email: admin@hbnb.com
Password: admin123
```

**Vérification**:
```bash
sqlite3 instance/hbnb_dev.db "SELECT email, is_admin FROM users;"
```
Devrait afficher : `admin@hbnb.com|1`

---

### TEST 2 : Login avec Admin

**Endpoint**: `POST /api/v1/auth/login`

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "admin123"
  }'
```

**Résultat attendu**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**✅ Validation**:
- Statut : 200 OK
- Token JWT retourné
- Token contient claim `is_admin: true`

**Sauvegarder le token**:
```bash
export ADMIN_TOKEN="eyJ0eXAiOiJKV1Qi..."
```

---

### TEST 3 : Login avec Mauvais Credentials

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "wrong_password"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Invalid credentials"
}
```

**✅ Validation**:
- Statut : 401 Unauthorized
- Message d'erreur approprié

---

### TEST 4 : Login avec Email Inexistant

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "notexist@hbnb.com",
    "password": "anything"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Invalid credentials"
}
```

**✅ Validation**:
- Statut : 401 Unauthorized
- Pas de leak d'information (même erreur que mot de passe incorrect)

---

## 🛡️ TESTS AUTHORIZATION (ROLE-BASED)

### TEST 5 : Créer User SANS Token (Doit Échouer)

**Endpoint**: `POST /api/v1/users/`

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "msg": "Missing Authorization Header"
}
```

**✅ Validation**:
- Statut : 401 Unauthorized
- Endpoint protégé par JWT

---

### TEST 6 : Créer User AVEC Token Admin (Doit Réussir)

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "password123",
    "is_admin": false
  }'
```

**Résultat attendu**:
```json
{
  "id": "uuid-here",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@test.com",
  "is_admin": false
}
```

**✅ Validation**:
- Statut : 201 Created
- User créé avec succès
- Password haché (pas retourné en réponse)
- `id` UUID généré

**Sauvegarder l'ID**:
```bash
export USER_ID="uuid-here"
```

---

### TEST 7 : Créer User Regular, Login, Tester Restrictions

**Étape 1** : Login avec user regular
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@test.com",
    "password": "password123"
  }'
```

**Sauvegarder token**:
```bash
export USER_TOKEN="token-here"
```

**Étape 2** : Essayer de créer un autre user (DOIT ÉCHOUER)
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@test.com",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Admin privileges required"
}
```

**✅ Validation**:
- Statut : 403 Forbidden
- User regular ne peut pas créer d'autres users

---

### TEST 8 : User Peut Modifier Ses Propres Données

**Requête**:
```bash
curl -X PUT http://localhost:5000/api/v1/users/$USER_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "id": "uuid",
  "first_name": "Johnny",
  "last_name": "Doe",
  "email": "john@test.com"
}
```

**✅ Validation**:
- Statut : 200 OK
- Données mises à jour
- User peut modifier ses propres données

---

### TEST 9 : User NE PEUT PAS Modifier Autres Users

**Créer un 2ème user** (avec admin token):
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "Alice",
    "last_name": "Wonder",
    "email": "alice@test.com",
    "password": "password123"
  }'
```

Sauvegarder : `export USER2_ID="uuid-here"`

**Essayer de modifier avec USER_TOKEN**:
```bash
curl -X PUT http://localhost:5000/api/v1/users/$USER2_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "first_name": "HACKED",
    "last_name": "Wonder",
    "email": "alice@test.com",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Unauthorized action"
}
```

**✅ Validation**:
- Statut : 403 Forbidden
- User ne peut pas modifier d'autres users

---

### TEST 10 : Admin PEUT Modifier N'importe Quel User

**Requête**:
```bash
curl -X PUT http://localhost:5000/api/v1/users/$USER_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "AdminModified",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "id": "uuid",
  "first_name": "AdminModified",
  "last_name": "Doe",
  "email": "john@test.com"
}
```

**✅ Validation**:
- Statut : 200 OK
- Admin peut modifier n'importe quel user

---

## 💾 TESTS CRUD AVEC DATABASE

### TEST 11 : Créer Place

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "title": "Belle maison Paris",
    "description": "Appartement lumineux au coeur de Paris",
    "price": 120.5,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "id": "place-uuid",
  "title": "Belle maison Paris",
  "description": "Appartement lumineux au coeur de Paris",
  "price": 120.5,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "user-uuid"
}
```

**✅ Validation**:
- Statut : 201 Created
- Place créé dans la database
- `owner_id` correctement lié

**Vérifier dans DB**:
```bash
sqlite3 instance/hbnb_dev.db "SELECT title, price, owner_id FROM places;"
```

**Sauvegarder**:
```bash
export PLACE_ID="place-uuid-here"
```

---

### TEST 12 : Lire Place

**Requête**:
```bash
curl -X GET http://localhost:5000/api/v1/places/$PLACE_ID
```

**Résultat attendu**:
```json
{
  "id": "place-uuid",
  "title": "Belle maison Paris",
  "price": 120.5,
  "owner_id": "user-uuid"
}
```

**✅ Validation**:
- Statut : 200 OK
- Données récupérées de la database

---

### TEST 13 : Lister Tous les Places

**Requête**:
```bash
curl -X GET http://localhost:5000/api/v1/places/
```

**Résultat attendu**:
```json
[
  {
    "id": "place-uuid",
    "title": "Belle maison Paris",
    "price": 120.5
  }
]
```

**✅ Validation**:
- Statut : 200 OK
- Array avec tous les places

---

### TEST 14 : Modifier Place

**Requête**:
```bash
curl -X PUT http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "title": "Superbe maison Paris",
    "description": "Appartement rénové",
    "price": 150.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "id": "place-uuid",
  "title": "Superbe maison Paris",
  "price": 150.0
}
```

**✅ Validation**:
- Statut : 200 OK
- Données mises à jour dans DB

**Vérifier**:
```bash
sqlite3 instance/hbnb_dev.db "SELECT title, price FROM places WHERE id='$PLACE_ID';"
```

---

### TEST 15 : Supprimer Place

**Requête**:
```bash
curl -X DELETE http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Résultat attendu**:
```json
{
  "message": "Place deleted successfully"
}
```

**✅ Validation**:
- Statut : 200 OK
- Place supprimé de la DB

**Vérifier**:
```bash
sqlite3 instance/hbnb_dev.db "SELECT COUNT(*) FROM places WHERE id='$PLACE_ID';"
```
Devrait retourner `0`

---

## 🔗 TESTS RELATIONS DATABASE

### TEST 16 : Relation User → Places (One-to-Many)

**Créer plusieurs places pour un user**:
```bash
# Place 1
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"title": "Place 1", "price": 100, "latitude": 48.0, "longitude": 2.0, "owner_id": "'$USER_ID'"}'

# Place 2
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"title": "Place 2", "price": 200, "latitude": 49.0, "longitude": 3.0, "owner_id": "'$USER_ID'"}'
```

**Vérifier relation dans DB**:
```bash
sqlite3 instance/hbnb_dev.db "
SELECT u.email, p.title
FROM users u
JOIN places p ON u.id = p.owner_id
WHERE u.id = '$USER_ID';
"
```

**✅ Validation**:
- 2 places liés au même user
- Foreign key `owner_id` fonctionnelle

---

### TEST 17 : Relation Place → Reviews (One-to-Many)

**Créer une review**:
```bash
export PLACE_ID="place-uuid"  # Utiliser un place existant

curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "text": "Excellent séjour !",
    "rating": 5,
    "place_id": "'$PLACE_ID'",
    "user_id": "'$USER2_ID'"
  }'
```

**Vérifier relation**:
```bash
sqlite3 instance/hbnb_dev.db "
SELECT p.title, r.text, r.rating
FROM places p
JOIN reviews r ON p.id = r.place_id
WHERE p.id = '$PLACE_ID';
"
```

**✅ Validation**:
- Review liée au place
- Foreign key `place_id` fonctionnelle

---

### TEST 18 : Relation Many-to-Many (Place ↔ Amenity)

**Créer amenities**:
```bash
# WiFi
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}'

export AMENITY1_ID="amenity-uuid-1"

# Piscine
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Piscine"}'

export AMENITY2_ID="amenity-uuid-2"
```

**Lier amenities au place**:
```bash
# Ajouter WiFi
curl -X POST http://localhost:5000/api/v1/places/$PLACE_ID/amenities/$AMENITY1_ID \
  -H "Authorization: Bearer $USER_TOKEN"

# Ajouter Piscine
curl -X POST http://localhost:5000/api/v1/places/$PLACE_ID/amenities/$AMENITY2_ID \
  -H "Authorization: Bearer $USER_TOKEN"
```

**Vérifier table de liaison**:
```bash
sqlite3 instance/hbnb_dev.db "
SELECT p.title, a.name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = '$PLACE_ID';
"
```

**✅ Validation**:
- 2 entrées dans `place_amenity`
- Relation many-to-many fonctionnelle

---

## 📏 TESTS BUSINESS RULES

### TEST 19 : User Ne Peut Pas Review Son Propre Place

**Créer un place**:
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "title": "My Place",
    "price": 100,
    "latitude": 48.0,
    "longitude": 2.0,
    "owner_id": "'$USER_ID'"
  }'

export MY_PLACE_ID="uuid"
```

**Essayer de review son propre place**:
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "text": "Mon super appart",
    "rating": 5,
    "place_id": "'$MY_PLACE_ID'",
    "user_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Cannot review your own place",
  "code": "OWNER_REVIEW"
}
```

**✅ Validation**:
- Statut : 400 Bad Request
- Business rule respectée

---

### TEST 20 : User Ne Peut Review Un Place Qu'Une Fois

**Créer 1ère review**:
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "text": "Première review",
    "rating": 4,
    "place_id": "'$PLACE_ID'",
    "user_id": "'$USER_ID'"
  }'
```

**Essayer 2ème review sur même place**:
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "text": "Deuxième review",
    "rating": 5,
    "place_id": "'$PLACE_ID'",
    "user_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "error": "You have already reviewed this place",
  "code": "DUPLICATE_REVIEW"
}
```

**✅ Validation**:
- Statut : 400 Bad Request
- Pas de review dupliquée

---

## ✅ TESTS VALIDATION

### TEST 21 : Email Invalide

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "not-an-email",
    "password": "password123"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Invalid email format"
}
```

**✅ Validation**:
- Email validation fonctionne

---

### TEST 22 : Rating Hors Limites

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "text": "Review",
    "rating": 10,
    "place_id": "'$PLACE_ID'",
    "user_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Rating must be between 1 and 5"
}
```

**✅ Validation**:
- Rating validation (1-5) fonctionne

---

### TEST 23 : Price Négative

**Requête**:
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "title": "Place",
    "price": -50,
    "latitude": 48.0,
    "longitude": 2.0,
    "owner_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Price must be positive"
}
```

---

### TEST 24 : Latitude/Longitude Hors Limites

**Latitude > 90**:
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "title": "Place",
    "price": 100,
    "latitude": 100,
    "longitude": 2.0,
    "owner_id": "'$USER_ID'"
  }'
```

**Résultat attendu**:
```json
{
  "error": "Latitude must be between -90.0 and 90.0"
}
```

---

## 🗄️ TESTS PRODUCTION MYSQL

### TEST 25 : Configuration MySQL

**Créer fichier .env**:
```bash
cat > part3/hbnb/.env << EOF
FLASK_ENV=production
SECRET_KEY=super-secret-production-key
JWT_SECRET_KEY=jwt-secret-production-key
DATABASE_URL=mysql+pymysql://hbnb_user:hbnb_pass@localhost/hbnb_prod
EOF
```

**Lancer avec config production**:
```bash
FLASK_ENV=production python run.py
```

**✅ Validation**:
- App démarre sans erreur
- Se connecte à MySQL (si disponible)
- Sinon, erreur claire de connexion

---

## ✅ CHECKLIST COMPLÈTE

### Authentification JWT
- [ ] TEST 1 : Créer admin
- [ ] TEST 2 : Login admin réussit
- [ ] TEST 3 : Login mauvais password échoue
- [ ] TEST 4 : Login email inexistant échoue

### Authorization
- [ ] TEST 5 : Créer user sans token échoue
- [ ] TEST 6 : Créer user avec admin token réussit
- [ ] TEST 7 : User regular ne peut pas créer users
- [ ] TEST 8 : User peut modifier ses données
- [ ] TEST 9 : User ne peut pas modifier autres users
- [ ] TEST 10 : Admin peut modifier tous users

### CRUD Database
- [ ] TEST 11 : Créer place
- [ ] TEST 12 : Lire place
- [ ] TEST 13 : Lister places
- [ ] TEST 14 : Modifier place
- [ ] TEST 15 : Supprimer place

### Relations
- [ ] TEST 16 : User → Places (1:N)
- [ ] TEST 17 : Place → Reviews (1:N)
- [ ] TEST 18 : Place ↔ Amenity (N:M)

### Business Rules
- [ ] TEST 19 : Pas de self-review
- [ ] TEST 20 : Pas de duplicate review

### Validation
- [ ] TEST 21 : Email invalide
- [ ] TEST 22 : Rating hors limites
- [ ] TEST 23 : Price négative
- [ ] TEST 24 : Lat/Long hors limites

### Production
- [ ] TEST 25 : Configuration MySQL

---

## 🚀 SCRIPT AUTOMATISÉ

Voir `test_part3_automated.sh` pour exécuter tous les tests automatiquement !

---

**Total Tests** : 25
**Temps estimé** : 30-45 minutes (manuel)
**Temps automatisé** : 5-10 minutes

