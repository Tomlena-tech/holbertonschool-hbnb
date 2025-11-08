-- HBnB Application Database Schema
-- Part 3: SQL Schema for Table Generation
--
-- This script creates all database tables for the HBnB application
-- with proper constraints, foreign keys, and indexes.

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
-- Stores user account information with authentication and authorization data
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index on email for faster lookups during authentication
CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- AMENITIES TABLE
-- ============================================================================
-- Stores amenity types that can be associated with places
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index on name for faster lookups
CREATE INDEX idx_amenities_name ON amenities(name);

-- ============================================================================
-- PLACES TABLE
-- ============================================================================
-- Stores accommodation listings with geographic and pricing information
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraint
    CONSTRAINT fk_places_owner
        FOREIGN KEY (owner_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);

-- ============================================================================
-- REVIEWS TABLE
-- ============================================================================
-- Stores user reviews for places with ratings
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraints
    CONSTRAINT fk_reviews_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_reviews_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- Business rule: one review per user per place
    CONSTRAINT unique_user_place_review
        UNIQUE (user_id, place_id),

    -- Business rule: rating must be between 1 and 5
    CONSTRAINT chk_rating_range
        CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes for performance
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- ============================================================================
-- PLACE_AMENITY TABLE (Many-to-Many Junction Table)
-- ============================================================================
-- Associates places with their amenities
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,

    -- Composite primary key prevents duplicate associations
    PRIMARY KEY (place_id, amenity_id),

    -- Foreign key constraints
    CONSTRAINT fk_place_amenity_place
        FOREIGN KEY (place_id)
        REFERENCES places(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_place_amenity_amenity
        FOREIGN KEY (amenity_id)
        REFERENCES amenities(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Indexes for faster joins
CREATE INDEX idx_place_amenity_place_id ON place_amenity(place_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);
