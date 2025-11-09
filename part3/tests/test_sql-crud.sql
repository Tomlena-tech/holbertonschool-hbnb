-- ========================================
-- SQL CRUD Operations Test Script
-- ========================================
-- This script tests CREATE, READ, UPDATE, and DELETE operations
-- for Users, Places, Reviews, and Amenities tables.
-- Tests data integrity and verifies admin user creation.

-- ========================================
-- 1. USERS TABLE - CRUD OPERATIONS
-- ========================================

-- CREATE: Insert test users including an admin
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES
    ('user-001', 'Admin', 'User', 'admin@hbnb.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oel4UYvZxAEm', TRUE, datetime('now'), datetime('now')),
    ('user-002', 'John', 'Doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oel4UYvZxAEm', FALSE, datetime('now'), datetime('now')),
    ('user-003', 'Jane', 'Smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oel4UYvZxAEm', FALSE, datetime('now'), datetime('now'));

-- READ: Select all users
SELECT '=== ALL USERS ===' AS test_section;
SELECT id, first_name, last_name, email, is_admin, created_at FROM users;

-- READ: Verify admin user was created correctly
SELECT '=== ADMIN USER VERIFICATION ===' AS test_section;
SELECT id, first_name, last_name, email, is_admin FROM users WHERE is_admin = TRUE;

-- READ: Select specific user by email
SELECT '=== USER BY EMAIL ===' AS test_section;
SELECT id, first_name, last_name, email FROM users WHERE email = 'john.doe@example.com';

-- UPDATE: Modify user information
UPDATE users SET last_name = 'Doe-Updated', updated_at = datetime('now') WHERE email = 'john.doe@example.com';

-- READ: Verify update
SELECT '=== USER AFTER UPDATE ===' AS test_section;
SELECT id, first_name, last_name, email, updated_at FROM users WHERE email = 'john.doe@example.com';

-- ========================================
-- 2. AMENITIES TABLE - CRUD OPERATIONS
-- ========================================

-- CREATE: Insert test amenities
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    ('amenity-001', 'WiFi', datetime('now'), datetime('now')),
    ('amenity-002', 'Pool', datetime('now'), datetime('now')),
    ('amenity-003', 'Parking', datetime('now'), datetime('now')),
    ('amenity-004', 'Air Conditioning', datetime('now'), datetime('now')),
    ('amenity-005', 'Kitchen', datetime('now'), datetime('now'));

-- READ: Select all amenities
SELECT '=== ALL AMENITIES ===' AS test_section;
SELECT id, name, created_at FROM amenities;

-- READ: Verify specific amenities were inserted correctly
SELECT '=== VERIFY AMENITIES ===' AS test_section;
SELECT name FROM amenities WHERE name IN ('WiFi', 'Pool', 'Parking', 'Air Conditioning', 'Kitchen');

-- UPDATE: Modify an amenity
UPDATE amenities SET name = 'High-Speed WiFi', updated_at = datetime('now') WHERE name = 'WiFi';

-- READ: Verify amenity update
SELECT '=== AMENITY AFTER UPDATE ===' AS test_section;
SELECT id, name, updated_at FROM amenities WHERE id = 'amenity-001';

-- ========================================
-- 3. PLACES TABLE - CRUD OPERATIONS
-- ========================================

-- CREATE: Insert test places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES
    ('place-001', 'Cozy Beach House', 'A beautiful beach house with ocean views', 150.00, 34.0522, -118.2437, 'user-002', datetime('now'), datetime('now')),
    ('place-002', 'Mountain Cabin', 'Peaceful cabin in the mountains', 120.00, 39.7392, -104.9903, 'user-002', datetime('now'), datetime('now')),
    ('place-003', 'Downtown Apartment', 'Modern apartment in city center', 200.00, 40.7128, -74.0060, 'user-003', datetime('now'), datetime('now'));

-- READ: Select all places
SELECT '=== ALL PLACES ===' AS test_section;
SELECT id, title, description, price, latitude, longitude, owner_id FROM places;

-- READ: Select places by owner
SELECT '=== PLACES BY OWNER (user-002) ===' AS test_section;
SELECT id, title, price, owner_id FROM places WHERE owner_id = 'user-002';

-- READ: Select places within price range
SELECT '=== PLACES UNDER $160/NIGHT ===' AS test_section;
SELECT id, title, price FROM places WHERE price < 160.00 ORDER BY price ASC;

-- UPDATE: Modify place information
UPDATE places SET price = 175.00, description = 'A stunning beach house with panoramic ocean views', updated_at = datetime('now') WHERE id = 'place-001';

-- READ: Verify place update
SELECT '=== PLACE AFTER UPDATE ===' AS test_section;
SELECT id, title, description, price, updated_at FROM places WHERE id = 'place-001';

-- ========================================
-- 4. PLACE_AMENITY TABLE - MANY-TO-MANY RELATIONSHIP
-- ========================================

-- CREATE: Associate amenities with places
INSERT INTO place_amenity (place_id, amenity_id)
VALUES
    ('place-001', 'amenity-001'),
    ('place-001', 'amenity-002'),
    ('place-001', 'amenity-005'),
    ('place-002', 'amenity-003'),
    ('place-002', 'amenity-004'),
    ('place-003', 'amenity-001'),
    ('place-003', 'amenity-004');

-- READ: Select places with their amenities
SELECT '=== PLACES WITH AMENITIES ===' AS test_section;
SELECT p.title, a.name AS amenity
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
ORDER BY p.title, a.name;

-- READ: Count amenities per place
SELECT '=== AMENITY COUNT BY PLACE ===' AS test_section;
SELECT p.title, COUNT(pa.amenity_id) AS amenity_count
FROM places p
LEFT JOIN place_amenity pa ON p.id = pa.place_id
GROUP BY p.id, p.title
ORDER BY amenity_count DESC;

-- DELETE: Remove an amenity association
DELETE FROM place_amenity WHERE place_id = 'place-001' AND amenity_id = 'amenity-002';

-- READ: Verify deletion
SELECT '=== PLACE-001 AMENITIES AFTER DELETION ===' AS test_section;
SELECT a.name
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'place-001';

-- ========================================
-- 5. REVIEWS TABLE - CRUD OPERATIONS
-- ========================================

-- CREATE: Insert test reviews
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES
    ('review-001', 'Amazing place! The beach view was spectacular.', 5, 'place-001', 'user-003', datetime('now'), datetime('now')),
    ('review-002', 'Great cabin, very peaceful and relaxing.', 5, 'place-002', 'user-003', datetime('now'), datetime('now')),
    ('review-003', 'Nice apartment but a bit noisy at night.', 3, 'place-003', 'user-002', datetime('now'), datetime('now'));

-- READ: Select all reviews
SELECT '=== ALL REVIEWS ===' AS test_section;
SELECT id, text, rating, place_id, user_id FROM reviews;

-- READ: Select reviews by place with user details
SELECT '=== REVIEWS FOR BEACH HOUSE ===' AS test_section;
SELECT r.text, r.rating, u.first_name, u.last_name
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = 'place-001';

-- READ: Calculate average rating per place
SELECT '=== AVERAGE RATING BY PLACE ===' AS test_section;
SELECT p.title, AVG(r.rating) AS avg_rating, COUNT(r.id) AS review_count
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title
ORDER BY avg_rating DESC;

-- UPDATE: Modify a review
UPDATE reviews SET text = 'Absolutely wonderful place! The beach view was breathtaking.', rating = 5, updated_at = datetime('now') WHERE id = 'review-001';

-- READ: Verify review update
SELECT '=== REVIEW AFTER UPDATE ===' AS test_section;
SELECT id, text, rating, updated_at FROM reviews WHERE id = 'review-001';

-- ========================================
-- 6. COMPLEX QUERIES - DATA INTEGRITY TESTS
-- ========================================

-- Join users, places, and reviews to show complete data relationships
SELECT '=== COMPLETE DATA RELATIONSHIPS ===' AS test_section;
SELECT
    u.first_name || ' ' || u.last_name AS owner_name,
    p.title AS place_title,
    p.price,
    r.rating,
    reviewer.first_name || ' ' || reviewer.last_name AS reviewer_name,
    r.text AS review_text
FROM places p
JOIN users u ON p.owner_id = u.id
LEFT JOIN reviews r ON p.id = r.place_id
LEFT JOIN users reviewer ON r.user_id = reviewer.id
ORDER BY p.title;

-- Find places with high ratings (4+)
SELECT '=== HIGH-RATED PLACES (AVG RATING >= 4) ===' AS test_section;
SELECT p.title, AVG(r.rating) AS avg_rating
FROM places p
JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title
HAVING AVG(r.rating) >= 4
ORDER BY avg_rating DESC;

-- List all users and count their places
SELECT '=== USER PLACE OWNERSHIP ===' AS test_section;
SELECT u.first_name, u.last_name, u.is_admin, COUNT(p.id) AS place_count
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
GROUP BY u.id, u.first_name, u.last_name, u.is_admin
ORDER BY place_count DESC;

-- ========================================
-- 7. DELETE OPERATIONS (CASCADING TESTS)
-- ========================================

-- DELETE: Remove a review
SELECT '=== DELETING REVIEW-003 ===' AS test_section;
DELETE FROM reviews WHERE id = 'review-003';

-- READ: Verify review deletion
SELECT '=== REMAINING REVIEWS ===' AS test_section;
SELECT id, text, place_id FROM reviews;

-- DELETE: Remove a place (should cascade to reviews and place_amenity)
SELECT '=== DELETING PLACE-002 ===' AS test_section;
DELETE FROM place_amenity WHERE place_id = 'place-002';
DELETE FROM reviews WHERE place_id = 'place-002';
DELETE FROM places WHERE id = 'place-002';

-- READ: Verify place deletion
SELECT '=== REMAINING PLACES ===' AS test_section;
SELECT id, title, owner_id FROM places;

-- DELETE: Remove an amenity (should not affect places)
SELECT '=== DELETING PARKING AMENITY ===' AS test_section;
DELETE FROM place_amenity WHERE amenity_id = 'amenity-003';
DELETE FROM amenities WHERE id = 'amenity-003';

-- READ: Verify amenity deletion
SELECT '=== REMAINING AMENITIES ===' AS test_section;
SELECT id, name FROM amenities;

-- ========================================
-- 8. FINAL DATA INTEGRITY VERIFICATION
-- ========================================

-- Verify admin user still exists
SELECT '=== FINAL ADMIN USER CHECK ===' AS test_section;
SELECT id, email, is_admin FROM users WHERE is_admin = TRUE;

-- Count all records in each table
SELECT '=== FINAL RECORD COUNTS ===' AS test_section;
SELECT 'Users' AS table_name, COUNT(*) AS record_count FROM users
UNION ALL
SELECT 'Places', COUNT(*) FROM places
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'Amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'Place-Amenity Associations', COUNT(*) FROM place_amenity;

-- ========================================
-- TEST SCRIPT COMPLETE
-- ========================================
SELECT '=== CRUD TEST SCRIPT COMPLETED SUCCESSFULLY ===' AS status;
