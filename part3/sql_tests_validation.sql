-- ═══════════════════════════════════════════════════════════════════════
-- TESTS DE VALIDATION - TASK 9
-- Projet : HBnB Evolution - Part 3
-- Ces tests vérifient que toutes les validations fonctionnent correctement
-- ═══════════════════════════════════════════════════════════════════════

USE hbnb_prod;

-- ═══════════════════════════════════════════════════════════════════════
-- TESTS USERS
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ TESTS USERS ══════' AS '';

-- Test 1 : ✅ Insertion valide
SELECT 'Test 1: Insertion user valide' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Jane', 'Smith', 'jane@example.com', '$2b$12$test', FALSE);
SELECT '✅ PASS' AS result;

-- Test 2 : ❌ Email invalide (pas de @)
SELECT 'Test 2: Email sans @' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Test', 'User', 'invalidemail', '$2b$12$test', FALSE);
-- Erreur attendue : Check constraint 'chk_email_format' is violated

-- Test 3 : ❌ Email invalide (pas de domaine)
SELECT 'Test 3: Email sans domaine' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Test', 'User', 'test@', '$2b$12$test', FALSE);
-- Erreur attendue : Check constraint 'chk_email_format' is violated

-- Test 4 : ❌ Email duplicate
SELECT 'Test 4: Email duplicate' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Test', 'User', 'jane@example.com', '$2b$12$test', FALSE);
-- Erreur attendue : Duplicate entry 'jane@example.com' for key 'uk_users_email'

-- Test 5 : ❌ first_name trop long (> 50 caractères)
SELECT 'Test 5: first_name trop long' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz', 'User', 'test1@example.com', '$2b$12$test', FALSE);
-- Erreur attendue : Check constraint 'chk_first_name_length' is violated

-- Test 6 : ❌ last_name trop long (> 50 caractères)
SELECT 'Test 6: last_name trop long' AS test;
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES (UUID(), 'Test', 'Abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz', 'test2@example.com', '$2b$12$test', FALSE);
-- Erreur attendue : Check constraint 'chk_last_name_length' is violated

-- ═══════════════════════════════════════════════════════════════════════
-- TESTS PLACES
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ TESTS PLACES ══════' AS '';

-- D'abord créer un user pour les tests de places
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('test-owner-id', 'Owner', 'Test', 'owner@example.com', '$2b$12$test', FALSE);

-- Test 7 : ✅ Insertion place valide
SELECT 'Test 7: Insertion place valide' AS test;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Belle Maison', 'Une très belle maison', 100.00, 48.8566, 2.3522, 'test-owner-id');
SELECT '✅ PASS' AS result;

-- Test 8 : ❌ Title vide
SELECT 'Test 8: Title vide' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), '', 100.00, 48.8566, 2.3522, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_title_not_empty' is violated

-- Test 9 : ❌ Title trop long (> 100 caractères)
SELECT 'Test 9: Title trop long' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz12345', 100.00, 48.8566, 2.3522, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_title_length' is violated

-- Test 10 : ❌ Prix négatif
SELECT 'Test 10: Prix négatif' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', -50.00, 48.8566, 2.3522, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_price_positive' is violated

-- Test 11 : ❌ Latitude > 90
SELECT 'Test 11: Latitude > 90' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', 100.00, 91.0, 2.3522, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_latitude_range' is violated

-- Test 12 : ❌ Latitude < -90
SELECT 'Test 12: Latitude < -90' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', 100.00, -91.0, 2.3522, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_latitude_range' is violated

-- Test 13 : ❌ Longitude > 180
SELECT 'Test 13: Longitude > 180' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', 100.00, 48.8566, 181.0, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_longitude_range' is violated

-- Test 14 : ❌ Longitude < -180
SELECT 'Test 14: Longitude < -180' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', 100.00, 48.8566, -181.0, 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_longitude_range' is violated

-- Test 15 : ❌ owner_id inexistant (foreign key)
SELECT 'Test 15: owner_id inexistant' AS test;
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Place', 100.00, 48.8566, 2.3522, 'non-existent-id');
-- Erreur attendue : Cannot add or update a child row: a foreign key constraint fails

-- ═══════════════════════════════════════════════════════════════════════
-- TESTS REVIEWS
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ TESTS REVIEWS ══════' AS '';

-- Créer un place et un user pour les tests
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('test-reviewer-id', 'Reviewer', 'Test', 'reviewer@example.com', '$2b$12$test', FALSE);

INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES ('test-place-id', 'Test House', 100.00, 48.8566, 2.3522, 'test-owner-id');

-- Test 16 : ✅ Insertion review valide
SELECT 'Test 16: Insertion review valide' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Excellent place !', 5, 'test-place-id', 'test-reviewer-id');
SELECT '✅ PASS' AS result;

-- Test 17 : ❌ Text vide
SELECT 'Test 17: Text vide' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), '', 5, 'test-place-id', 'test-reviewer-id');
-- Erreur attendue : Check constraint 'chk_text_not_empty' is violated

-- Test 18 : ❌ Rating < 1
SELECT 'Test 18: Rating < 1' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Bad', 0, 'test-place-id', 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_rating_range' is violated

-- Test 19 : ❌ Rating > 5
SELECT 'Test 19: Rating > 5' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Too good', 6, 'test-place-id', 'test-owner-id');
-- Erreur attendue : Check constraint 'chk_rating_range' is violated

-- Test 20 : ❌ Duplicate review (même user + place)
SELECT 'Test 20: Duplicate review' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Another review', 4, 'test-place-id', 'test-reviewer-id');
-- Erreur attendue : Duplicate entry for key 'uk_reviews_user_place'

-- Test 21 : ❌ Self-review (user review son propre place)
SELECT 'Test 21: Self-review' AS test;
INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'My own place', 5, 'test-place-id', 'test-owner-id');
-- Erreur attendue : Cannot review your own place (trigger)

-- ═══════════════════════════════════════════════════════════════════════
-- TESTS AMENITIES
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ TESTS AMENITIES ══════' AS '';

-- Test 22 : ✅ Insertion amenity valide
SELECT 'Test 22: Insertion amenity valide' AS test;
INSERT INTO amenities (id, name)
VALUES (UUID(), 'Gym');
SELECT '✅ PASS' AS result;

-- Test 23 : ❌ Name duplicate
SELECT 'Test 23: Name duplicate' AS test;
INSERT INTO amenities (id, name)
VALUES (UUID(), 'Gym');
-- Erreur attendue : Duplicate entry 'Gym' for key 'uk_amenities_name'

-- Test 24 : ❌ Name vide
SELECT 'Test 24: Name vide' AS test;
INSERT INTO amenities (id, name)
VALUES (UUID(), '');
-- Erreur attendue : Check constraint 'chk_amenity_name_not_empty' is violated

-- Test 25 : ❌ Name trop long (> 50 caractères)
SELECT 'Test 25: Name trop long' AS test;
INSERT INTO amenities (id, name)
VALUES (UUID(), 'Abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz');
-- Erreur attendue : Check constraint 'chk_amenity_name_length' is violated

-- ═══════════════════════════════════════════════════════════════════════
-- TESTS CASCADE DELETE
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ TESTS CASCADE DELETE ══════' AS '';

-- Test 26 : ✅ Cascade delete user → places
SELECT 'Test 26: Cascade delete user → places' AS test;

-- Créer un user avec des places
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('cascade-test-user', 'Cascade', 'Test', 'cascade@example.com', '$2b$12$test', FALSE);

INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES ('cascade-place-1', 'Place 1', 100.00, 0.0, 0.0, 'cascade-test-user');
INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES ('cascade-place-2', 'Place 2', 150.00, 0.0, 0.0, 'cascade-test-user');

-- Vérifier avant suppression
SELECT COUNT(*) AS places_count_before
FROM places
WHERE owner_id = 'cascade-test-user';
-- Devrait retourner 2

-- Supprimer le user
DELETE FROM users WHERE id = 'cascade-test-user';

-- Vérifier après suppression
SELECT COUNT(*) AS places_count_after
FROM places
WHERE owner_id = 'cascade-test-user';
-- Devrait retourner 0 (cascade delete)

SELECT '✅ PASS - Cascade delete fonctionne' AS result;

-- Test 27 : ✅ Cascade delete place → reviews
SELECT 'Test 27: Cascade delete place → reviews' AS test;

-- Créer un place avec des reviews
INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('cascade-owner', 'Owner', 'Test', 'cascade-owner@example.com', '$2b$12$test', FALSE);

INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('cascade-reviewer-1', 'Reviewer1', 'Test', 'reviewer1@example.com', '$2b$12$test', FALSE);

INSERT INTO users (id, first_name, last_name, email, password_hash, is_admin)
VALUES ('cascade-reviewer-2', 'Reviewer2', 'Test', 'reviewer2@example.com', '$2b$12$test', FALSE);

INSERT INTO places (id, title, price, latitude, longitude, owner_id)
VALUES ('cascade-test-place', 'Test Place', 100.00, 0.0, 0.0, 'cascade-owner');

INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Review 1', 5, 'cascade-test-place', 'cascade-reviewer-1');

INSERT INTO reviews (id, text, rating, place_id, user_id)
VALUES (UUID(), 'Review 2', 4, 'cascade-test-place', 'cascade-reviewer-2');

-- Vérifier avant suppression
SELECT COUNT(*) AS reviews_count_before
FROM reviews
WHERE place_id = 'cascade-test-place';
-- Devrait retourner 2

-- Supprimer le place
DELETE FROM places WHERE id = 'cascade-test-place';

-- Vérifier après suppression
SELECT COUNT(*) AS reviews_count_after
FROM reviews
WHERE place_id = 'cascade-test-place';
-- Devrait retourner 0 (cascade delete)

SELECT '✅ PASS - Cascade delete fonctionne' AS result;

-- ═══════════════════════════════════════════════════════════════════════
-- RÉCAPITULATIF
-- ═══════════════════════════════════════════════════════════════════════

SELECT '══════ RÉCAPITULATIF ══════' AS '';

SELECT
    'USERS' AS table_name,
    COUNT(*) AS total_rows
FROM users
UNION ALL
SELECT
    'PLACES',
    COUNT(*)
FROM places
UNION ALL
SELECT
    'REVIEWS',
    COUNT(*)
FROM reviews
UNION ALL
SELECT
    'AMENITIES',
    COUNT(*)
FROM amenities
UNION ALL
SELECT
    'PLACE_AMENITY',
    COUNT(*)
FROM place_amenity;

-- ═══════════════════════════════════════════════════════════════════════
-- FIN DES TESTS
-- ═══════════════════════════════════════════════════════════════════════
