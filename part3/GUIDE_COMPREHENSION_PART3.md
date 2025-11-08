# 📚 GUIDE DE COMPRÉHENSION - PART 3 HBnB
## Ce que vous DEVEZ comprendre par cœur

**Date de création** : 2025-11-08
**Pour** : Thomas - Soumission Part 3
**But** : Révision avant soutenance et compréhension approfondie

---

## 📖 TABLE DES MATIÈRES

1. [Architecture Globale](#1-architecture-globale)
2. [Authentification JWT](#2-authentification-jwt)
3. [Sécurité avec Bcrypt](#3-sécurité-avec-bcrypt)
4. [SQLAlchemy ORM](#4-sqlalchemy-orm)
5. [Authorization (RBAC)](#5-authorization-rbac)
6. [Relations entre Tables](#6-relations-entre-tables)
7. [Configuration Dev vs Production](#7-configuration-dev-vs-production)
8. [Questions Fréquentes](#8-questions-fréquentes)

---

## 1. ARCHITECTURE GLOBALE

### Les 3 Couches de l'Application

```
┌─────────────────────────────────────────┐
│   COUCHE 1 : API (Presentation Layer)  │
│   Fichiers : app/api/v1/*.py            │
│   Rôle : Gérer les requêtes HTTP        │
└─────────────────┬───────────────────────┘
                  │ appelle
                  ▼
┌─────────────────────────────────────────┐
│   COUCHE 2 : Facade (Business Logic)   │
│   Fichier : app/services/facade.py      │
│   Rôle : Logique métier et validation   │
└─────────────────┬───────────────────────┘
                  │ appelle
                  ▼
┌─────────────────────────────────────────┐
│   COUCHE 3 : Repository (Persistence)   │
│   Fichiers : app/persistence/*.py       │
│   Rôle : Accès à la base de données     │
└─────────────────┬───────────────────────┘
                  │ SQL
                  ▼
┌─────────────────────────────────────────┐
│   DATABASE (SQLite ou MySQL)            │
│   Tables : users, places, reviews, etc. │
└─────────────────────────────────────────┘
```

### Pourquoi cette architecture ?

**✅ Séparation des responsabilités**
- Si je change la base de données → Je modifie seulement la couche Repository
- Si je change l'API (REST → GraphQL) → Je modifie seulement la couche API
- La logique métier reste indépendante

**✅ Testabilité**
- Je peux tester chaque couche séparément
- Facile de mocker (simuler) une couche pour tester une autre

**✅ Réutilisabilité**
- La même logique métier peut servir pour une API, une CLI, ou une interface web

---

## 2. AUTHENTIFICATION JWT

### Qu'est-ce qu'un JWT ?

**JWT = JSON Web Token**

C'est un token (jeton) qui contient des informations encodées en 3 parties :

```
eyJhbGci...    .    eyJmcmVz...    .    vPwP6W8...
    ↑                   ↑                   ↑
  HEADER             PAYLOAD            SIGNATURE
```

### Contenu d'un JWT

**HEADER (en-tête)**
```json
{
  "alg": "HS256",    // Algorithme de signature (HMAC-SHA256)
  "typ": "JWT"       // Type de token
}
```

**PAYLOAD (données)**
```json
{
  "sub": "13fc6363-4110-4de7-acda-558f1d834444",  // ID de l'utilisateur
  "is_admin": true,                                // Claim personnalisé
  "iat": 1762615283,                               // Issued At (date création)
  "exp": 1762616183                                // Expiration (15 min après)
}
```

**SIGNATURE**
```
HMAC-SHA256(
  base64(header) + "." + base64(payload),
  JWT_SECRET_KEY
)
```

### Comment ça fonctionne dans votre code ?

**ÉTAPE 1 : Login (app/api/v1/auth.py)**

```python
@api.route('/login')
def post(self):
    # 1. Récupérer email et password
    creds = api.payload

    # 2. Chercher le user dans la base
    user = facade.get_user_by_email(creds['email'])

    # 3. Vérifier le password (avec bcrypt)
    if not user or not user.verify_password(creds['password']):
        return {'error': 'Invalid credentials'}, 401

    # 4. Créer le token JWT
    token = create_access_token(
        identity=str(user.id),              # Le "sub" du payload
        additional_claims={'is_admin': user.is_admin}  # Claim perso
    )

    # 5. Retourner le token au client
    return {'access_token': token}, 200
```

**ÉTAPE 2 : Utilisation du token (app/api/v1/places.py)**

```python
@jwt_required()  # Ce décorateur vérifie automatiquement le token
def post(self):
    # Récupérer l'ID du user depuis le token
    current_user = get_jwt_identity()
    # → Retourne "13fc6363-4110-4de7-acda-558f1d834444"

    # Créer un place avec cet owner
    place_data['owner_id'] = current_user
    new_place = facade.create_place(place_data)
```

### Pourquoi JWT et pas des sessions ?

| Sessions (ancienne méthode) | JWT (méthode moderne) |
|----------------------------|----------------------|
| Stocke les sessions sur le serveur | Rien stocké côté serveur (stateless) |
| Difficulté avec plusieurs serveurs | Fonctionne avec plusieurs serveurs |
| Chaque requête = accès base de données | Pas besoin de base pour vérifier |
| Ne scale pas bien | Scale très bien |

### Points clés à retenir

✅ **Le token contient l'identité** : Pas besoin de chercher dans la base à chaque requête
✅ **Signature cryptographique** : Impossible de modifier le token sans la clé secrète
✅ **Expiration automatique** : Le token expire après 15 minutes (configurable)
✅ **Stateless** : Le serveur ne stocke rien, tout est dans le token

---

## 3. SÉCURITÉ AVEC BCRYPT

### Pourquoi NE JAMAIS stocker les passwords en clair ?

Imaginez cette table si on stocke en clair :

| Email | Password |
|-------|----------|
| admin@hbnb.com | admin123 |
| user@test.com | password123 |

**Problème** : Si quelqu'un accède à votre base (hack, backup volé, employé malveillant), TOUS les passwords sont exposés !

### Solution : Hachage avec Bcrypt

**Hachage = Fonction à sens unique**

```
password → [fonction bcrypt] → hash
```

**Impossible de revenir en arrière** :
```
hash → [???] → password  ❌ IMPOSSIBLE
```

### Comment bcrypt fonctionne ?

**1. Lors de la création d'un user (app/models/user.py:66-68)**

```python
def set_password(self, password):
    # Bcrypt fait 3 choses :
    # 1. Génère un "salt" (sel) aléatoire
    # 2. Combine password + salt
    # 3. Hash le résultat avec bcrypt (12 rounds par défaut)

    self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # Résultat : $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyDvTw7Jxkau
```

**Décomposition du hash** :
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyDvTw7Jxkau
 │   │   │                        │
 │   │   │                        └─ Hash + Salt fusionnés
 │   │   └─ Le salt (aléatoire)
 │   └─ Cost factor (12 = 2^12 = 4096 itérations)
 └─ Version de bcrypt (2b)
```

**2. Lors du login (app/models/user.py:70-72)**

```python
def check_password(self, password):
    # Bcrypt :
    # 1. Extrait le salt du hash stocké
    # 2. Hash le password fourni avec ce même salt
    # 3. Compare les deux hash

    return bcrypt.check_password_hash(self.password_hash, password)
    # True si match, False sinon
```

### Exemple concret

```python
# User 1 crée son compte avec password "admin123"
user1.set_password("admin123")
# Hash : $2b$12$ABC...XYZ

# User 2 crée son compte AUSSI avec "admin123"
user2.set_password("admin123")
# Hash : $2b$12$DEF...UVW  ← DIFFÉRENT grâce au salt aléatoire !

# Lors du login
user1.check_password("admin123")  # True
user1.check_password("wrong")     # False
```

### Qu'est-ce que le "salt" ?

**Salt = Valeur aléatoire ajoutée au password avant le hachage**

**Sans salt** :
```
password "admin123" → hash toujours identique
→ Tables rainbow possibles (pré-calculer tous les hash)
```

**Avec salt** :
```
password "admin123" + salt "ABC" → hash1
password "admin123" + salt "XYZ" → hash2
→ Même password = hash différents
→ Tables rainbow inutiles
```

### Points clés à retenir

✅ **Bcrypt est LENT par design** : 4096 itérations rendent le brute-force très difficile
✅ **Salt automatique** : Bcrypt génère un salt aléatoire à chaque fois
✅ **Adaptive** : On peut augmenter le cost factor avec le temps
✅ **Industrie standard** : Recommandé par l'OWASP et tous les experts sécurité

---

## 4. SQLALCHEMY ORM

### Qu'est-ce qu'un ORM ?

**ORM = Object-Relational Mapping**

C'est un pont entre le monde des objets Python et le monde des tables SQL.

```
SANS ORM (SQL brut)                AVEC ORM (SQLAlchemy)
──────────────────                 ────────────────────

cursor.execute(                    user = User.query.get(user_id)
  "SELECT * FROM users
   WHERE id = ?",
  (user_id,)
)
row = cursor.fetchone()
user = {
  'id': row[0],
  'email': row[1],
  ...
}
```

### Définition d'un modèle (app/models/user.py)

```python
class User(BaseModel):
    __tablename__ = 'users'  # Nom de la table SQL

    # Colonnes de la table
    first_name = db.Column(db.String(50), nullable=False)
    #              ↑           ↑              ↑
    #         Type Python   Max length    NOT NULL

    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #                                                   ↑
    #                                         UNIQUE constraint

    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    #                                  ↑
    #                            Valeur par défaut
```

**Ce code crée cette table SQL** :

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT 0 NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Opérations CRUD avec SQLAlchemy

**CREATE (app/persistence/repository.py:17-21)**

```python
def add(self, obj):
    from app import db
    db.session.add(obj)      # Ajoute à la session
    db.session.commit()      # Écrit dans la base

    # Équivalent SQL :
    # INSERT INTO users (id, email, ...) VALUES (?, ?, ...)
```

**READ**

```python
# Récupérer par ID
user = User.query.get(user_id)
# SQL : SELECT * FROM users WHERE id = ?

# Récupérer tous
users = User.query.all()
# SQL : SELECT * FROM users

# Recherche avec filtre
user = User.query.filter_by(email='admin@hbnb.com').first()
# SQL : SELECT * FROM users WHERE email = 'admin@hbnb.com' LIMIT 1
```

**UPDATE (app/persistence/repository.py:29-35)**

```python
def update(self, obj_id, data):
    obj = self.get(obj_id)
    if obj:
        for key, value in data.items():
            setattr(obj, key, value)  # Modifie l'objet Python
        db.session.commit()           # Persiste en base

    # SQL : UPDATE users SET first_name=?, ... WHERE id=?
```

**DELETE (app/persistence/repository.py:37-42)**

```python
def delete(self, obj_id):
    obj = self.get(obj_id)
    if obj:
        db.session.delete(obj)
        db.session.commit()

    # SQL : DELETE FROM users WHERE id = ?
```

### Avantages de SQLAlchemy

✅ **Protection contre SQL Injection**
```python
# DANGEREUX (SQL brut) :
query = f"SELECT * FROM users WHERE email = '{email}'"
# Si email = "'; DROP TABLE users; --" → CATASTROPHE

# SÉCURISÉ (SQLAlchemy) :
user = User.query.filter_by(email=email).first()
# SQLAlchemy échappe automatiquement les caractères spéciaux
```

✅ **Code plus lisible**
```python
# AVANT : 10 lignes de SQL
# APRÈS : 1 ligne Python
user = User.query.filter_by(email=email).first()
```

✅ **Portabilité**
```python
# Le même code Python fonctionne avec :
# - SQLite
# - MySQL
# - PostgreSQL
# - Oracle
# Seule la connection string change !
```

### Points clés à retenir

✅ **db.Column** définit les colonnes de la table
✅ **db.session** gère les transactions
✅ **query** permet de faire des SELECT
✅ **Protection SQL Injection** automatique
✅ **Même code = plusieurs bases** (SQLite, MySQL, etc.)

---

## 5. AUTHORIZATION (RBAC)

### Qu'est-ce que RBAC ?

**RBAC = Role-Based Access Control**

Système de permissions basé sur les rôles :
- **Admin** : Peut tout faire
- **User** : Peut seulement modifier ses propres données

### Les 2 niveaux de contrôle

**NIVEAU 1 : Authentication (Qui êtes-vous ?)**

```python
@jwt_required()  # Es-tu connecté ?
def post(self):
    current_user = get_jwt_identity()  # Qui es-tu ?
```

**NIVEAU 2 : Authorization (Avez-vous le droit ?)**

```python
@jwt_required()
def post(self):
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    if not is_admin:
        return {'error': 'Admin privileges required'}, 403
    # Tu es connecté, mais pas admin → INTERDIT
```

### Exemples concrets dans votre code

**EXEMPLE 1 : Admin seulement (app/api/v1/users.py:23-29)**

```python
@jwt_required()
def post(self):
    """Créer un user - Admin seulement"""
    claims = get_jwt()  # Récupère TOUTES les infos du token

    if not claims.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403

    # Si on arrive ici, l'utilisateur est admin ✅
    new_user = facade.create_user(api.payload)
```

**EXEMPLE 2 : Propriétaire OU Admin (app/api/v1/places.py)**

```python
@jwt_required()
def put(self, place_id):
    """Modifier un place - Propriétaire OU Admin"""
    current_user = get_jwt_identity()  # ID du user connecté
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    place = facade.get_place(place_id)

    # Vérification : Admin OU Propriétaire
    if not is_admin and place.owner_id != current_user:
        return {'error': 'Unauthorized action'}, 403

    # Si on arrive ici, l'utilisateur a le droit ✅
    facade.update_place(place_id, api.payload)
```

### Matrice des permissions

| Action | Public | User connecté | Propriétaire | Admin |
|--------|--------|---------------|--------------|-------|
| Voir liste users | ✅ | ✅ | ✅ | ✅ |
| Voir un user | ✅ | ✅ | ✅ | ✅ |
| Créer un user | ❌ | ❌ | ❌ | ✅ |
| Modifier un user | ❌ | ❌ | ✅ | ✅ |
| Créer un place | ❌ | ✅ | ✅ | ✅ |
| Modifier un place | ❌ | ❌ | ✅ | ✅ |
| Supprimer un place | ❌ | ❌ | ✅ | ✅ |
| Créer amenity | ❌ | ❌ | ❌ | ✅ |
| Modifier amenity | ❌ | ❌ | ❌ | ✅ |

### Les codes HTTP d'erreur

```python
401 Unauthorized : "Tu n'es pas connecté"
# Pas de token JWT OU token invalide/expiré

403 Forbidden : "Tu es connecté mais tu n'as pas le droit"
# Token valide MAIS pas les permissions

404 Not Found : "La ressource n'existe pas"
# L'objet demandé n'existe pas dans la base
```

### Points clés à retenir

✅ **Authentication ≠ Authorization**
   - Authentication = Vérifier l'identité
   - Authorization = Vérifier les permissions

✅ **2 types de vérifications**
   - Admin check : `claims.get('is_admin')`
   - Owner check : `object.owner_id == current_user`

✅ **Fail secure**
   - Par défaut, on refuse l'accès
   - On autorise seulement si les conditions sont remplies

---

## 6. RELATIONS ENTRE TABLES

### Les 4 types de relations

**1. One-to-Many : User → Place**

```python
# Dans User (app/models/user.py:36)
places = db.relationship('Place', backref='owner', lazy=True,
                        cascade='all, delete-orphan')

# Dans Place (app/models/place.py)
owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
```

**Signification** :
- Un User peut avoir PLUSIEURS Places
- Un Place a UN SEUL owner
- `backref='owner'` → On peut faire `place.owner` pour obtenir le User
- `cascade='all, delete-orphan'` → Si on supprime le User, ses Places sont supprimés aussi

**SQL équivalent** :
```sql
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Utilisation** :
```python
# Récupérer tous les places d'un user
user = User.query.get(user_id)
places = user.places  # Liste de tous ses places

# Récupérer le owner d'un place
place = Place.query.get(place_id)
owner = place.owner  # L'objet User propriétaire
```

**2. One-to-Many : Place → Review**

```python
# Dans Place
reviews = db.relationship('Review', backref='place', lazy=True,
                         cascade='all, delete-orphan')

# Dans Review
place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
```

**Signification** :
- Un Place peut avoir PLUSIEURS Reviews
- Une Review concerne UN SEUL Place
- Si on supprime un Place, toutes ses Reviews sont supprimées

**3. One-to-Many : User → Review**

```python
# Dans User
reviews = db.relationship('Review', backref='user', lazy=True,
                         cascade='all, delete-orphan')

# Dans Review
user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
```

**Signification** :
- Un User peut écrire PLUSIEURS Reviews
- Une Review est écrite par UN SEUL User
- Si on supprime un User, toutes ses Reviews sont supprimées

**4. Many-to-Many : Place ↔ Amenity**

```python
# Table d'association (app/models/place_amenity.py)
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

# Dans Place
amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                           backref=db.backref('places', lazy=True))
```

**Signification** :
- Un Place peut avoir PLUSIEURS Amenities
- Une Amenity peut être dans PLUSIEURS Places
- Table intermédiaire `place_amenity` pour stocker les associations

**SQL équivalent** :
```sql
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
```

**Utilisation** :
```python
# Ajouter une amenity à un place
place = Place.query.get(place_id)
wifi = Amenity.query.filter_by(name='Wi-Fi').first()
place.amenities.append(wifi)
db.session.commit()

# Récupérer toutes les amenities d'un place
amenities = place.amenities  # Liste d'objets Amenity

# Récupérer tous les places ayant une amenity
wifi = Amenity.query.filter_by(name='Wi-Fi').first()
places_with_wifi = wifi.places  # Liste de tous les places avec Wi-Fi
```

### Cascade : Qu'est-ce qui se passe lors d'une suppression ?

**Avec `cascade='all, delete-orphan'`** :

```python
# Supprimer un user
user = User.query.get(user_id)
db.session.delete(user)
db.session.commit()

# Automatiquement supprimé aussi :
# - Tous les Places du user
# - Toutes les Reviews du user
# - Toutes les associations place_amenity des places du user
```

**Schéma de cascade** :
```
DELETE User
    ↓
DELETE tous ses Places
    ↓
DELETE toutes les Reviews de ces Places
    ↓
DELETE toutes les associations place_amenity
```

### Points clés à retenir

✅ **Foreign Key** = Colonne qui référence la Primary Key d'une autre table
✅ **backref** = Permet la navigation inverse (place.owner, review.user, etc.)
✅ **cascade** = Définit le comportement lors de suppressions
✅ **Many-to-Many** = Nécessite une table intermédiaire

---

## 7. CONFIGURATION DEV VS PRODUCTION

### Pourquoi 2 configurations ?

**Développement** :
- On veut debugger facilement
- Performances secondaires
- Base de données simple (SQLite)

**Production** :
- Sécurité maximale
- Performances critiques
- Base de données robuste (MySQL)

### Configuration Development (config.py:13-16)

```python
class DevelopmentConfig(Config):
    DEBUG = True  # Active le debugger Flask
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
    # SQLite = fichier local, pas de serveur nécessaire
```

**Caractéristiques** :
- ✅ Debug mode activé → Erreurs détaillées affichées
- ✅ SQLite → Pas besoin d'installer MySQL
- ✅ Secrets par défaut OK (pas de sécurité critique)
- ✅ Auto-reload quand on modifie le code

### Configuration Production (config.py:19-28)

```python
class ProductionConfig(Config):
    DEBUG = False  # JAMAIS de debug en production !
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://hbnb_user:hbnb_password@localhost/hbnb_prod'
    )
    SECRET_KEY = os.getenv('SECRET_KEY')  # DOIT être défini
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # DOIT être défini
```

**Caractéristiques** :
- ❌ Debug désactivé → Pas de fuite d'informations sensibles
- ✅ MySQL → Base de données robuste et performante
- ✅ Secrets en variables d'environnement → Sécurisé
- ✅ Logs en production

### Variables d'environnement (.env)

**Développement (.env)** :
```bash
FLASK_ENV=development
DATABASE_URL=sqlite:///hbnb_dev.db
SECRET_KEY=dev-secret-key-not-for-production
JWT_SECRET_KEY=dev-jwt-secret
```

**Production (.env)** :
```bash
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://hbnb_user:SuperSecurePass123!@localhost/hbnb_prod
SECRET_KEY=VotreSuperSecretKeyTresLongueEtAleatoire123456789ABCDEF
JWT_SECRET_KEY=UnAutreSecretDifferentPourLesJWT987654321ZYXWVU
```

### Générer des secrets forts

```bash
# Générer un secret sécurisé
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Résultat : XYZ123abc-DEF456ghi_JKL789mno
```

### Migration SQLite → MySQL

**ÉTAPE 1 : Installer MySQL**
```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# Démarrer MySQL
sudo systemctl start mysql
```

**ÉTAPE 2 : Créer la base de données**
```bash
mysql -u root -p

# Dans MySQL
CREATE DATABASE hbnb_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hbnb_user'@'localhost' IDENTIFIED BY 'VotreMotDePasseSecurise';
GRANT ALL PRIVILEGES ON hbnb_prod.* TO 'hbnb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**ÉTAPE 3 : Configurer l'application**
```bash
# Dans .env
export DATABASE_URL=mysql+pymysql://hbnb_user:VotreMotDePasseSecurise@localhost/hbnb_prod
export FLASK_ENV=production
export SECRET_KEY=VotreSecretGeneré
export JWT_SECRET_KEY=UnAutreSecret
```

**ÉTAPE 4 : Lancer l'application**
```bash
python3 run.py
# SQLAlchemy va automatiquement créer les tables dans MySQL !
```

### Différences SQLite vs MySQL

| Aspect | SQLite | MySQL |
|--------|--------|-------|
| Installation | Aucune (inclus Python) | Serveur à installer |
| Fichier | Un fichier .db local | Base sur serveur |
| Concurrence | Faible (1 writer à la fois) | Excellente (multiples writers) |
| Taille max | ~140 TB | ~64 TB par table |
| Usage | Dev, tests, petites apps | Production, apps à fort trafic |
| Backup | Copier le fichier .db | mysqldump, réplication |

### Points clés à retenir

✅ **DEV : SQLite + Debug ON** pour faciliter le développement
✅ **PROD : MySQL + Debug OFF** pour performance et sécurité
✅ **Secrets = Variables d'environnement** JAMAIS dans le code
✅ **SQLAlchemy** permet de changer de base facilement

---

## 8. QUESTIONS FRÉQUENTES

### Q1 : Pourquoi utiliser JWT et pas des sessions ?

**Réponse** :

Les sessions traditionnelles stockent l'état côté serveur :
```
User se connecte → Session stockée en RAM/Redis
Chaque requête → Lookup dans le stockage de sessions
```

Problèmes :
- Nécessite un stockage partagé entre serveurs
- Lookup à chaque requête = performance
- Difficile à scaler horizontalement

JWT est **stateless** :
```
User se connecte → Token généré avec toutes les infos
Chaque requête → Token validé cryptographiquement
```

Avantages :
- ✅ Aucun stockage serveur nécessaire
- ✅ Fonctionne avec load balancing
- ✅ Pas de lookup en base
- ✅ Microservices-friendly

### Q2 : Le JWT ne peut-il pas être volé ?

**Réponse** :

Oui, comme tout token. Protections :

1. **HTTPS obligatoire** : Chiffre la communication
2. **httpOnly cookies** : Empêche JavaScript d'y accéder
3. **Expiration courte** : Token expire après 15-30 min
4. **Refresh tokens** : Pour renouveler sans re-login
5. **Pas de données sensibles** : Pas de password dans le token

Dans votre code :
```python
token = create_access_token(
    identity=str(user.id),  # Seulement l'ID
    additional_claims={'is_admin': user.is_admin}  # Pas sensible
)
```

### Q3 : Pourquoi bcrypt et pas SHA256 ?

**Réponse** :

SHA256 est **trop rapide** pour les passwords :
```
SHA256 : ~1 milliard de hash/seconde
→ Brute force facile avec GPU
```

Bcrypt est **volontairement lent** :
```
Bcrypt (cost=12) : ~4000 hash/seconde
→ Brute force quasi impossible
```

De plus :
- ✅ Bcrypt inclut un salt automatique
- ✅ Bcrypt est adaptive (on peut augmenter le cost)
- ✅ SHA256 n'est PAS conçu pour les passwords

### Q4 : Que se passe-t-il si je supprime un User ?

**Réponse** :

Grâce au `cascade='all, delete-orphan'` :

```python
user = User.query.get(user_id)
db.session.delete(user)
db.session.commit()
```

**Automatiquement supprimé** :
1. ✅ Tous les Places du user (owner_id = user.id)
2. ✅ Toutes les Reviews du user (user_id = user.id)
3. ✅ Toutes les Reviews des places du user
4. ✅ Toutes les associations place_amenity des places

**C'est voulu** : On ne veut pas de places "orphelins" sans propriétaire.

### Q5 : Puis-je changer de SQLite à MySQL sans modifier le code ?

**Réponse** :

**OUI !** C'est l'avantage de SQLAlchemy.

Seule modification nécessaire :
```python
# Avant (SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'

# Après (MySQL)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:pass@localhost/hbnb_prod'
```

**Tout le reste du code reste identique** :
- ✅ Modèles (User, Place, etc.)
- ✅ Repositories
- ✅ Queries
- ✅ Relations

### Q6 : Que signifie @jwt_required() exactement ?

**Réponse** :

C'est un **décorateur** Flask qui :

1. Vérifie que le header `Authorization` existe
2. Extrait le token : `Bearer eyJhbGci...`
3. Vérifie la signature avec `JWT_SECRET_KEY`
4. Vérifie que le token n'est pas expiré
5. Si OK → Continue vers la fonction
6. Si KO → Retourne 401 Unauthorized

Sans @jwt_required() :
```python
def post(self):
    # N'importe qui peut appeler
```

Avec @jwt_required() :
```python
@jwt_required()
def post(self):
    # Seulement les users avec token valide
    current_user = get_jwt_identity()
```

### Q7 : Pourquoi 3 couches (API, Facade, Repository) ?

**Réponse** :

**Séparation des responsabilités** :

**API Layer** : "Comment présenter ?"
- Gère HTTP (GET, POST, etc.)
- Validation input
- Formatage JSON

**Facade Layer** : "Quelle est la logique métier ?"
- Règles métier (pas de self-review)
- Coordination (créer user + place + review)
- Validation métier

**Repository Layer** : "Comment stocker ?"
- Accès base de données
- CRUD operations
- Transactions

**Avantage** : Si je veux ajouter une interface GraphQL, je réutilise Facade + Repository sans les toucher !

### Q8 : Le token JWT contient-il le password ?

**Réponse** :

**NON ! JAMAIS !**

Le token contient :
```json
{
  "sub": "user-id-uuid",      // ✅ ID seulement
  "is_admin": true,           // ✅ Info non sensible
  "exp": 1762616183           // ✅ Expiration
}
```

**Pas dedans** :
- ❌ Password (ni en clair ni hashé)
- ❌ Numéro de carte bancaire
- ❌ Adresse
- ❌ Toute info personnelle sensible

**Règle** : JWT visible par le client → Seulement infos non sensibles

### Q9 : C'est quoi exactement db.session ?

**Réponse** :

`db.session` = **Gestionnaire de transactions** SQLAlchemy

**Transaction** = Ensemble d'opérations qui doivent toutes réussir ou toutes échouer.

```python
# Début transaction (implicite)
user = User(...)
db.session.add(user)

place = Place(owner=user, ...)
db.session.add(place)

# Si TOUT est OK → Commit (valide)
db.session.commit()

# Si une erreur → Rollback (annule tout)
db.session.rollback()
```

**Exemple** :
```python
try:
    user = User(email='test@test.com', ...)
    db.session.add(user)

    place = Place(owner=user, ...)
    db.session.add(place)  # Erreur ici !

    db.session.commit()  # Jamais atteint
except:
    db.session.rollback()  # Annule TOUT (user + place)
```

### Q10 : Comment débugger si ça ne marche pas ?

**Réponse** :

**1. Vérifier les logs Flask** :
```bash
python3 run.py
# Regarder les erreurs affichées
```

**2. Vérifier la base de données** :
```bash
# SQLite
sqlite3 instance/hbnb_dev.db
.tables  # Voir les tables
SELECT * FROM users;  # Voir les données

# MySQL
mysql -u hbnb_user -p hbnb_prod
SHOW TABLES;
SELECT * FROM users;
```

**3. Tester l'authentification** :
```bash
# Test login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@hbnb.com","password":"admin123"}'

# Doit retourner un access_token
```

**4. Tester un endpoint protégé** :
```bash
# Sans token → 401
curl http://localhost:5000/api/v1/users/

# Avec token → 200
curl http://localhost:5000/api/v1/users/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

**5. Vérifier les imports** :
```python
# Si erreur "No module named 'flask_bcrypt'"
pip3 install -r requirements.txt
```

---

## 🎯 CHECKLIST FINALE AVANT SOUTENANCE

### Points à vérifier (2 minutes)

```bash
# 1. Application démarre
cd part3/hbnb
python3 run.py
# ✅ Doit afficher "Admin user auto-created" ou "already exists"

# 2. Base de données existe
ls -lh instance/hbnb_dev.db
# ✅ Doit afficher ~60K

# 3. Login fonctionne
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@hbnb.com","password":"admin123"}'
# ✅ Doit retourner un access_token

# 4. Dépendances installées
pip3 list | grep -i flask
# ✅ Doit afficher Flask, Flask-JWT-Extended, Flask-SQLAlchemy
```

### Questions à maîtriser

✅ **Architecture** : Expliquer les 3 couches
✅ **JWT** : Expliquer comment fonctionne l'authentification
✅ **Bcrypt** : Pourquoi on l'utilise et comment ça marche
✅ **SQLAlchemy** : Avantages d'un ORM vs SQL brut
✅ **Relations** : Expliquer les foreign keys et cascade
✅ **RBAC** : Différence entre admin et user
✅ **Configuration** : Différences dev vs production

---

## 📚 POUR ALLER PLUS LOIN

### Documentation officielle

- **Flask** : https://flask.palletsprojects.com/
- **Flask-JWT-Extended** : https://flask-jwt-extended.readthedocs.io/
- **SQLAlchemy** : https://docs.sqlalchemy.org/
- **Bcrypt** : https://github.com/pyca/bcrypt/

### Concepts avancés (pas obligatoires pour Part 3)

- **Refresh tokens** : Pour prolonger la session sans re-login
- **Token blacklist** : Pour invalider des tokens (logout)
- **OAuth 2.0** : Authentification via Google, Facebook, etc.
- **2FA** : Two-Factor Authentication
- **Rate limiting** : Limiter le nombre de requêtes par IP
- **CORS** : Cross-Origin Resource Sharing pour APIs publiques

---

## ✅ CONCLUSION

Vous maîtrisez maintenant :

✅ **L'architecture** 3-tiers de votre application
✅ **L'authentification JWT** et son fonctionnement
✅ **La sécurité** avec bcrypt et validation
✅ **SQLAlchemy ORM** et les relations entre tables
✅ **RBAC** et la gestion des permissions
✅ **Configuration** dev/prod

**Vous êtes prêt pour la soutenance !** 🎉

---

**Généré le** : 2025-11-08
**Pour** : Thomas - Holberton School
**Projet** : HBnB Evolution - Part 3
**Par** : Claude Code
