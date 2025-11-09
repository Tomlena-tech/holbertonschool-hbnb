-- ═══════════════════════════════════════════════════════════════════════
-- SCRIPTS SQL - TASK 9 : DATA VALIDATION
-- Projet : HBnB Evolution - Part 3
-- Date : 2025-11-08
-- ═══════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════
-- 1. CRÉATION DE LA BASE DE DONNÉES
-- ═══════════════════════════════════════════════════════════════════════

-- Supprimer la base si elle existe (ATTENTION: supprime toutes les données!)
-- DROP DATABASE IF EXISTS hbnb_prod;

-- Créer la base de données
CREATE DATABASE IF NOT EXISTS hbnb_prod
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Utiliser la base
USE hbnb_prod;

-- ═══════════════════════════════════════════════════════════════════════
-- 2. TABLE USERS
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS users (
    -- Clé primaire (UUID)
    id VARCHAR(36) NOT NULL,

    -- Timestamps automatiques
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attributs user
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,

    -- Contraintes
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_email (email),

    -- Validation avec CHECK constraints (MySQL 8.0.16+)
    CONSTRAINT chk_first_name_length CHECK (CHAR_LENGTH(first_name) <= 50),
    CONSTRAINT chk_last_name_length CHECK (CHAR_LENGTH(last_name) <= 50),
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[^@]+@[^@]+\\.[^@]+$'),
    CONSTRAINT chk_email_length CHECK (CHAR_LENGTH(email) <= 120),
    CONSTRAINT chk_password_hash_length CHECK (CHAR_LENGTH(password_hash) <= 128)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index pour améliorer les performances de recherche par email
CREATE INDEX idx_users_email ON users(email);

-- ═══════════════════════════════════════════════════════════════════════
-- 3. TABLE AMENITIES
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS amenities (
    -- Clé primaire (UUID)
    id VARCHAR(36) NOT NULL,

    -- Timestamps automatiques
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attributs amenity
    name VARCHAR(50) NOT NULL,

    -- Contraintes
    PRIMARY KEY (id),
    UNIQUE KEY uk_amenities_name (name),

    -- Validation
    CONSTRAINT chk_amenity_name_length CHECK (CHAR_LENGTH(name) <= 50),
    CONSTRAINT chk_amenity_name_not_empty CHECK (CHAR_LENGTH(name) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index pour recherche par nom
CREATE INDEX idx_amenities_name ON amenities(name);

-- ═══════════════════════════════════════════════════════════════════════
-- 4. TABLE PLACES
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS places (
    -- Clé primaire (UUID)
    id VARCHAR(36) NOT NULL,

    -- Timestamps automatiques
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attributs place
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,  -- Utiliser DECIMAL pour l'argent (plus précis que FLOAT)
    latitude DECIMAL(10, 8) NOT NULL,  -- Précision GPS
    longitude DECIMAL(11, 8) NOT NULL,
    owner_id VARCHAR(36) NOT NULL,

    -- Contraintes
    PRIMARY KEY (id),

    -- Foreign key vers users
    CONSTRAINT fk_places_owner
        FOREIGN KEY (owner_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Validation
    CONSTRAINT chk_title_length CHECK (CHAR_LENGTH(title) <= 100),
    CONSTRAINT chk_title_not_empty CHECK (CHAR_LENGTH(title) > 0),
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT chk_latitude_range CHECK (latitude >= -90.0 AND latitude <= 90.0),
    CONSTRAINT chk_longitude_range CHECK (longitude >= -180.0 AND longitude <= 180.0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index pour recherche par propriétaire
CREATE INDEX idx_places_owner_id ON places(owner_id);

-- Index pour recherche géographique
CREATE INDEX idx_places_location ON places(latitude, longitude);

-- ═══════════════════════════════════════════════════════════════════════
-- 5. TABLE REVIEWS
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS reviews (
    -- Clé primaire (UUID)
    id VARCHAR(36) NOT NULL,

    -- Timestamps automatiques
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attributs review
    text TEXT NOT NULL,
    rating INT NOT NULL,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,

    -- Contraintes
    PRIMARY KEY (id),

    -- Foreign keys
    CONSTRAINT fk_reviews_place
        FOREIGN KEY (place_id) REFERENCES places(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Validation
    CONSTRAINT chk_text_not_empty CHECK (CHAR_LENGTH(text) > 0),
    CONSTRAINT chk_rating_range CHECK (rating >= 1 AND rating <= 5),

    -- Contrainte unique : un user ne peut reviewer qu'une fois par place
    UNIQUE KEY uk_reviews_user_place (user_id, place_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index pour recherche par place
CREATE INDEX idx_reviews_place_id ON reviews(place_id);

-- Index pour recherche par user
CREATE INDEX idx_reviews_user_id ON reviews(user_id);

-- ═══════════════════════════════════════════════════════════════════════
-- 6. TABLE PLACE_AMENITY (Many-to-Many)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS place_amenity (
    -- Clé primaire composite
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,

    -- Contraintes
    PRIMARY KEY (place_id, amenity_id),

    -- Foreign keys
    CONSTRAINT fk_place_amenity_place
        FOREIGN KEY (place_id) REFERENCES places(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_place_amenity_amenity
        FOREIGN KEY (amenity_id) REFERENCES amenities(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Index pour recherche inverse (amenity → places)
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);

-- ═══════════════════════════════════════════════════════════════════════
-- 7. TRIGGERS POUR VALIDATION SUPPLÉMENTAIRE
-- ═══════════════════════════════════════════════════════════════════════

-- Trigger pour empêcher un user de reviewer son propre place
DELIMITER //

CREATE TRIGGER trg_prevent_self_review
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
    DECLARE place_owner VARCHAR(36);

    -- Récupérer l'owner du place
    SELECT owner_id INTO place_owner
    FROM places
    WHERE id = NEW.place_id;

    -- Vérifier si le user essaie de reviewer son propre place
    IF place_owner = NEW.user_id THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot review your own place';
    END IF;
END//

DELIMITER ;

-- ═══════════════════════════════════════════════════════════════════════
-- 8. VUES UTILES POUR VALIDATION
-- ═══════════════════════════════════════════════════════════════════════

-- Vue pour voir les users avec nombre de places et reviews
CREATE OR REPLACE VIEW v_user_statistics AS
SELECT
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    u.is_admin,
    COUNT(DISTINCT p.id) AS total_places,
    COUNT(DISTINCT r.id) AS total_reviews,
    u.created_at
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
LEFT JOIN reviews r ON u.id = r.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email, u.is_admin, u.created_at;

-- Vue pour voir les places avec leurs statistiques
CREATE OR REPLACE VIEW v_place_statistics AS
SELECT
    p.id,
    p.title,
    p.price,
    p.latitude,
    p.longitude,
    CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
    COUNT(DISTINCT r.id) AS total_reviews,
    COALESCE(AVG(r.rating), 0) AS average_rating,
    COUNT(DISTINCT pa.amenity_id) AS total_amenities,
    p.created_at
FROM places p
LEFT JOIN users u ON p.owner_id = u.id
LEFT JOIN reviews r ON p.id = r.place_id
LEFT JOIN place_amenity pa ON p.id = pa.place_id
GROUP BY p.id, p.title, p.price, p.latitude, p.longitude, u.first_name, u.last_name, p.created_at;

-- ═══════════════════════════════════════════════════════════════════════
-- 9. DONNÉES DE TEST AVEC VALIDATION
-- ═══════════════════════════════════════════════════════════════════════

-- Insertion d'un admin (avec validation email)
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyDvTw7Jxkau',  -- 'admin123'
    TRUE,
    NOW(),
    NOW()
);

-- Insertion d'un user régulier
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at)
VALUES (
    UUID(),
    'John',
    'Doe',
    'john@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyDvTw7Jxkau',
    FALSE,
    NOW(),
    NOW()
);

-- Insertion d'amenities (avec validation name unique)
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    (UUID(), 'WiFi', NOW(), NOW()),
    (UUID(), 'Parking', NOW(), NOW()),
    (UUID(), 'Pool', NOW(), NOW()),
    (UUID(), 'Air Conditioning', NOW(), NOW());

-- ═══════════════════════════════════════════════════════════════════════
-- 10. REQUÊTES DE VÉRIFICATION
-- ═══════════════════════════════════════════════════════════════════════

-- Vérifier les tables créées
SELECT TABLE_NAME, TABLE_ROWS, CREATE_TIME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'hbnb_prod'
ORDER BY TABLE_NAME;

-- Vérifier les contraintes
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'hbnb_prod'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;

-- Vérifier les foreign keys
SELECT
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'hbnb_prod'
    AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Vérifier les CHECK constraints (MySQL 8.0.16+)
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CHECK_CLAUSE
FROM information_schema.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'hbnb_prod';

-- ═══════════════════════════════════════════════════════════════════════
-- 11. TESTS DE VALIDATION
-- ═══════════════════════════════════════════════════════════════════════

-- Test 1 : Email invalide (doit échouer)
-- INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
-- VALUES (UUID(), 'Test', 'User', 'invalid-email', 'hash', FALSE);
-- Erreur attendue : Check constraint 'chk_email_format' is violated

-- Test 2 : Email duplicate (doit échouer)
-- INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
-- VALUES (UUID(), 'Test', 'User', 'admin@hbnb.com', 'hash', FALSE);
-- Erreur attendue : Duplicate entry 'admin@hbnb.com' for key 'uk_users_email'

-- Test 3 : Rating invalide (doit échouer)
-- INSERT INTO reviews (id, text, rating, place_id, user_id)
-- VALUES (UUID(), 'Test', 6, 'place_id', 'user_id');
-- Erreur attendue : Check constraint 'chk_rating_range' is violated

-- Test 4 : Prix négatif (doit échouer)
-- INSERT INTO places (id, title, price, latitude, longitude, owner_id)
-- VALUES (UUID(), 'Test', -10.00, 0.0, 0.0, 'user_id');
-- Erreur attendue : Check constraint 'chk_price_positive' is violated

-- Test 5 : Latitude hors plage (doit échouer)
-- INSERT INTO places (id, title, price, latitude, longitude, owner_id)
-- VALUES (UUID(), 'Test', 100.00, 91.0, 0.0, 'user_id');
-- Erreur attendue : Check constraint 'chk_latitude_range' is violated

-- ═══════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT
-- ═══════════════════════════════════════════════════════════════════════
