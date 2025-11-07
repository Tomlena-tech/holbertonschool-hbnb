# ✅ CHECKLIST TESTS MANUELS - HBnB Part 3

## 🚀 Démarrage Rapide

### 1. Lancer l'Application
```bash
cd part3/hbnb
python run.py
```

### 2. Ouvrir Swagger UI
Naviguer vers : `http://localhost:5000/api/v1/docs`

### 3. Créer un Admin
```bash
cd part3/hbnb
python create_admin.py
```

**Credentials** :
- Email: `admin@hbnb.com`
- Password: `admin123`

---

## 📝 TESTS À FAIRE MANUELLEMENT

### ✅ SECTION 1 : Authentication

#### Test 1.1 : Login Admin
- [ ] Aller sur `/api/v1/auth/login`
- [ ] POST avec email: `admin@hbnb.com`, password: `admin123`
- [ ] **Vérifier** : Token JWT retourné
- [ ] **Copier le token** pour tests suivants

#### Test 1.2 : Login avec Mauvais Password
- [ ] Essayer avec password incorrect
- [ ] **Vérifier** : Erreur 401 "Invalid credentials"

#### Test 1.3 : Login avec Email Inexistant
- [ ] Essayer avec email qui n'existe pas
- [ ] **Vérifier** : Erreur 401 "Invalid credentials"

---

### ✅ SECTION 2 : Authorization (Admin vs User)

#### Test 2.1 : Créer User SANS Token
- [ ] Aller sur `/api/v1/users/`
- [ ] POST SANS header Authorization
- [ ] **Vérifier** : Erreur 401 "Missing Authorization Header"

#### Test 2.2 : Créer User AVEC Token Admin
- [ ] POST sur `/api/v1/users/`
- [ ] Ajouter header : `Authorization: Bearer <TOKEN_ADMIN>`
- [ ] Body :
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@test.com",
  "password": "password123",
  "is_admin": false
}
```
- [ ] **Vérifier** : User créé (201), password PAS retourné
- [ ] **Noter l'ID du user** : `_________________`

#### Test 2.3 : Login avec User Regular
- [ ] POST sur `/api/v1/auth/login`
- [ ] Email: `john@test.com`, Password: `password123`
- [ ] **Vérifier** : Token retourné
- [ ] **Copier le token USER** : `_________________`

#### Test 2.4 : User Regular Essaie de Créer User
- [ ] POST sur `/api/v1/users/`
- [ ] Avec token USER (pas admin)
- [ ] **Vérifier** : Erreur 403 "Admin privileges required"

#### Test 2.5 : User Modifie Ses Propres Données
- [ ] PUT sur `/api/v1/users/<ID_USER>`
- [ ] Avec token USER
- [ ] **Vérifier** : Modification réussit (200)

#### Test 2.6 : User Essaie de Modifier Autre User
- [ ] Créer un 2ème user (avec admin)
- [ ] Essayer de modifier ce 2ème user avec token du 1er user
- [ ] **Vérifier** : Erreur 403 "Unauthorized action"

#### Test 2.7 : Admin Peut Modifier N'importe Quel User
- [ ] PUT sur `/api/v1/users/<ID_USER>` avec token ADMIN
- [ ] **Vérifier** : Modification réussit

---

### ✅ SECTION 3 : CRUD - Places

#### Test 3.1 : Créer un Place
- [ ] POST sur `/api/v1/places/`
- [ ] Avec token USER
- [ ] Body :
```json
{
  "title": "Appartement Paris",
  "description": "Bel appartement",
  "price": 120.5,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "<ID_USER>"
}
```
- [ ] **Vérifier** : Place créé (201)
- [ ] **Noter l'ID** : `_________________`

#### Test 3.2 : Lire un Place
- [ ] GET sur `/api/v1/places/<ID_PLACE>`
- [ ] **Vérifier** : Données retournées (200)

#### Test 3.3 : Lister Tous les Places
- [ ] GET sur `/api/v1/places/`
- [ ] **Vérifier** : Array avec au moins 1 place

#### Test 3.4 : Modifier un Place
- [ ] PUT sur `/api/v1/places/<ID_PLACE>`
- [ ] Changer le prix à 150.0
- [ ] **Vérifier** : Prix mis à jour

#### Test 3.5 : Supprimer un Place
- [ ] DELETE sur `/api/v1/places/<ID_PLACE>`
- [ ] **Vérifier** : Message "deleted successfully" (200)
- [ ] GET sur ce place → Erreur 404

---

### ✅ SECTION 4 : CRUD - Amenities

#### Test 4.1 : Créer Amenity
- [ ] POST sur `/api/v1/amenities/`
- [ ] Body : `{"name": "WiFi"}`
- [ ] **Vérifier** : Amenity créé
- [ ] **Noter l'ID** : `_________________`

#### Test 4.2 : Lister Amenities
- [ ] GET sur `/api/v1/amenities/`
- [ ] **Vérifier** : Liste retournée

#### Test 4.3 : Modifier Amenity
- [ ] PUT sur `/api/v1/amenities/<ID>`
- [ ] Changer name à "WiFi Haut Débit"
- [ ] **Vérifier** : Mis à jour

#### Test 4.4 : Supprimer Amenity
- [ ] DELETE sur `/api/v1/amenities/<ID>`
- [ ] **Vérifier** : Supprimé

---

### ✅ SECTION 5 : CRUD - Reviews

#### Test 5.1 : Créer Review
- [ ] Créer 2 users (A et B) et 1 place (propriétaire = A)
- [ ] POST sur `/api/v1/reviews/` avec token de B
- [ ] Body :
```json
{
  "text": "Super appart !",
  "rating": 5,
  "place_id": "<ID_PLACE>",
  "user_id": "<ID_USER_B>"
}
```
- [ ] **Vérifier** : Review créé (201)
- [ ] **Noter l'ID** : `_________________`

#### Test 5.2 : Lister Reviews d'un Place
- [ ] GET sur `/api/v1/places/<ID_PLACE>/reviews`
- [ ] **Vérifier** : Au moins 1 review

#### Test 5.3 : Modifier Review
- [ ] PUT sur `/api/v1/reviews/<ID>`
- [ ] Changer rating à 4
- [ ] **Vérifier** : Mis à jour

#### Test 5.4 : Supprimer Review
- [ ] DELETE sur `/api/v1/reviews/<ID>`
- [ ] **Vérifier** : Supprimé

---

### ✅ SECTION 6 : Business Rules

#### Test 6.1 : Owner Ne Peut Pas Review Son Place
- [ ] User A crée un place
- [ ] User A essaie de review ce place
- [ ] **Vérifier** : Erreur 400 "Cannot review your own place"
- [ ] **Vérifier** : Code erreur "OWNER_REVIEW"

#### Test 6.2 : Pas de Review Dupliquée
- [ ] User B review place de A
- [ ] User B essaie de review encore le même place
- [ ] **Vérifier** : Erreur 400 "Already reviewed"
- [ ] **Vérifier** : Code erreur "DUPLICATE_REVIEW"

---

### ✅ SECTION 7 : Validation

#### Test 7.1 : Email Invalide
- [ ] Créer user avec email "not-an-email"
- [ ] **Vérifier** : Erreur 400 "Invalid email format"

#### Test 7.2 : Rating Hors Limites
- [ ] Créer review avec rating = 10
- [ ] **Vérifier** : Erreur 400 "Rating must be between 1 and 5"

#### Test 7.3 : Rating = 0
- [ ] Créer review avec rating = 0
- [ ] **Vérifier** : Erreur 400 "Rating must be between 1 and 5"

#### Test 7.4 : Price Négative
- [ ] Créer place avec price = -50
- [ ] **Vérifier** : Erreur 400 "Price must be positive"

#### Test 7.5 : Latitude Hors Limites
- [ ] Créer place avec latitude = 100
- [ ] **Vérifier** : Erreur 400 "Latitude must be between -90 and 90"

#### Test 7.6 : Longitude Hors Limites
- [ ] Créer place avec longitude = 200
- [ ] **Vérifier** : Erreur 400 "Longitude must be between -180 and 180"

#### Test 7.7 : Champ Obligatoire Manquant
- [ ] Créer user SANS email
- [ ] **Vérifier** : Erreur de validation

---

### ✅ SECTION 8 : Relations Database

#### Test 8.1 : Relation User → Places (1:N)
- [ ] Créer user
- [ ] Créer 3 places pour ce user
- [ ] Vérifier dans SQLite :
```bash
sqlite3 instance/hbnb_dev.db "
SELECT u.email, COUNT(p.id) as nb_places
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
GROUP BY u.id;
"
```
- [ ] **Vérifier** : 3 places liés au user

#### Test 8.2 : Relation Place → Reviews (1:N)
- [ ] Créer 1 place
- [ ] Créer 3 reviews pour ce place (par différents users)
- [ ] GET `/api/v1/places/<ID>/reviews`
- [ ] **Vérifier** : 3 reviews retournés

#### Test 8.3 : Relation Place ↔ Amenity (N:M)
- [ ] Créer 2 amenities
- [ ] Lier les 2 au même place
- [ ] Vérifier table de liaison :
```bash
sqlite3 instance/hbnb_dev.db "
SELECT * FROM place_amenity;
"
```
- [ ] **Vérifier** : 2 lignes dans place_amenity

---

### ✅ SECTION 9 : Database Persistence

#### Test 9.1 : Données Persistent Après Redémarrage
- [ ] Créer user, place, review
- [ ] **Stopper** l'application (Ctrl+C)
- [ ] **Redémarrer** : `python run.py`
- [ ] GET sur les ressources créées
- [ ] **Vérifier** : Données toujours présentes

#### Test 9.2 : Cascade Delete - User
- [ ] User A a 2 places et 3 reviews
- [ ] DELETE user A
- [ ] **Vérifier** : Ses places sont supprimés (cascade)
- [ ] **Vérifier** : Ses reviews sont supprimés

#### Test 9.3 : Cascade Delete - Place
- [ ] Place a 5 reviews
- [ ] DELETE place
- [ ] **Vérifier** : Reviews du place sont supprimés

---

### ✅ SECTION 10 : Password Security

#### Test 10.1 : Password Jamais Retourné
- [ ] Créer user
- [ ] GET `/api/v1/users/<ID>`
- [ ] **Vérifier** : Réponse NE contient PAS "password" ou "password_hash"

#### Test 10.2 : Password Hashé en DB
- [ ] Créer user avec password "test123"
- [ ] Vérifier en DB :
```bash
sqlite3 instance/hbnb_dev.db "SELECT password_hash FROM users LIMIT 1;"
```
- [ ] **Vérifier** : Hash bcrypt (commence par $2b$)
- [ ] **Vérifier** : PAS le password en clair

#### Test 10.3 : Login Vérifie Hash
- [ ] Créer user avec password "secret"
- [ ] Login avec "secret" → Réussit
- [ ] Login avec "wrong" → Échoue

---

## 📊 RÉSUMÉ

**Total Sections** : 10
**Total Tests Manuels** : ~45

### Score :
- Tests Passés : _____ / 45
- Tests Échoués : _____ / 45

### Statut :
- [ ] ✅ Tous les tests passent (100%)
- [ ] ⚠️ Quelques tests échouent (> 90%)
- [ ] ❌ Beaucoup de tests échouent (< 90%)

---

## 🎯 VALIDATION FINALE

**Pour soumettre Part 3, TOUS les tests doivent passer !**

- [ ] Authentication JWT fonctionne
- [ ] Authorization (admin/user) fonctionne
- [ ] CRUD complet sur toutes les entités
- [ ] Business rules respectées
- [ ] Validation des données
- [ ] Relations database correctes
- [ ] Persistence après redémarrage
- [ ] Passwords sécurisés (bcrypt)
- [ ] Pas de password en clair retourné

**Prêt pour Holberton** : ☐ OUI  ☐ NON

---

**Date de test** : _______________
**Testé par** : _______________
**Environnement** : ☐ SQLite  ☐ MySQL
