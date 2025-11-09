-- HBnB Application Initial Data
-- Part 3: SQL Data Insertion Script
--
-- This script populates the database with initial required data:
-- - Administrator user account
-- - Initial amenities

-- ============================================================================
-- ADMINISTRATOR USER
-- ============================================================================
-- Insert the default admin user with fixed UUID and hashed password
-- Password: admin1234 (hashed with bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$Yk2x62v6Wf1R.JMf1iy3q.5n90TesuqrBtwZJESS6ZuHd.9beqg8K',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ============================================================================
-- INITIAL AMENITIES
-- ============================================================================
-- Insert three common amenities for places
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    (
        'a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d',
        'WiFi',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e',
        'Swimming Pool',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        'c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f',
        'Air Conditioning',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
