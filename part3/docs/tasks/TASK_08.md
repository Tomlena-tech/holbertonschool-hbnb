# Task 8: Entity Relationships with SQLAlchemy

## Overview

This document describes the implementation of SQLAlchemy relationships between the User, Place, Review, and Amenity models, completing the database persistence layer for the HBnB application.

**Task Objective**: Add foreign keys and SQLAlchemy relationships to connect entities using one-to-many and many-to-many patterns, enabling bidirectional navigation between related objects.

**Completion Date**: November 2025
**Status**: ✅ Completed

---

## Table of Contents

1. [Requirements](#requirements)
2. [Architecture](#architecture)
3. [Implementation Details](#implementation-details)
4. [Database Schema](#database-schema)
5. [Testing](#testing)
6. [Best Practices](#best-practices)

---

## Requirements

### Functional Requirements

1. **Place-User Relationship (One-to-Many)**:
   - Add `owner_id` foreign key to Place model
   - Use `db.relationship()` for bidirectional access
   - User can access owned_places, Place can access owner

2. **Review-User Relationship (One-to-Many)**:
   - Add `user_id` foreign key to Review model
   - Use `db.relationship()` for bidirectional access
   - User can access user_reviews, Review can access user

3. **Review-Place Relationship (One-to-Many)**:
   - Add `place_id` foreign key to Review model
   - Use `db.relationship()` for bidirectional access
   - Place can access reviews, Review can access place
   - Add unique constraint: one review per user per place

4. **Place-Amenity Relationship (Many-to-Many)**:
   - Create `place_amenity` association table
   - Use `db.relationship()` with `secondary` parameter
   - Place can access amenities_rel, Amenity can access places_list

### Non-Functional Requirements

- Maintain backward compatibility with existing code
- Preserve all existing validation logic
- Follow SQLAlchemy best practices for relationships
- No breaking changes to API endpoints
- All tests must pass (115/115)

---

## Architecture

### Relationship Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    Entity Relationships                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User (1) ─────────────────────────────────> (*) Place     │
│       owner                              owned_places        │
│       (One user owns many places)                           │
│                                                              │
│  User (1) ─────────────────────────────────> (*) Review    │
│       user                               user_reviews        │
│       (One user writes many reviews)                        │
│                                                              │
│  Place (1) ────────────────────────────────> (*) Review    │
│        place                                 reviews         │
│        (One place has many reviews)                         │
│                                                              │
│  Place (*) <──────place_amenity──────────> (*) Amenity    │
│         amenities_rel              places_list              │
│         (Many-to-many via association table)                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Database Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
├─────────────────────────────────────────────────────────────┤
│  API Endpoints (users, places, reviews, amenities)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
├─────────────────────────────────────────────────────────────┤
│  HBnBFacade                                                  │
│  ├─ user_repo: SQLAlchemyRepository (Task 6)               │
│  ├─ place_repo: InMemoryRepository (Task 9+: migrate)      │
│  ├─ review_repo: InMemoryRepository (Task 9+: migrate)     │
│  └─ amenity_repo: InMemoryRepository (Task 9+: migrate)    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Model Layer                          │
├─────────────────────────────────────────────────────────────┤
│  BaseModel (db.Model, __abstract__=True)                    │
│  ├─ User (Task 6) ──┬──> Place (Task 7+8) ✅              │
│  │                   └──> Review (Task 7+8) ✅             │
│  ├─ Amenity (Task 7) <──> Place (Task 8) ✅                │
│  └─ Review (Task 7+8) ──> Place (Task 8) ✅                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
├─────────────────────────────────────────────────────────────┤
│  SQLAlchemy ORM → SQLite Database                           │
│  Tables: users, amenities, places, reviews, place_amenity   │
│  Foreign Keys: owner_id, user_id, place_id                  │
│  Constraints: UNIQUE(user_id, place_id) on reviews          │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### 1. Place-Amenity Association Table

**File**: `app/models/place.py`

**Problem**: Many-to-many relationships require an association table to store the connections between two entities.

**Solution**: Created `place_amenity` table using `db.Table()`:

```python
# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)
```

**Why This Approach**:
- `db.Table()` creates a simple association table without a model class
- Composite primary key (place_id, amenity_id) prevents duplicates
- Foreign keys ensure referential integrity

**How It Works**:
- SQLAlchemy uses this table to manage the many-to-many relationship
- No separate Python class needed for simple associations
- Accessible via `Place.amenities_rel` and `Amenity.places_list`

### 2. Place-User Relationship (Owner)

**File**: `app/models/place.py`

**Problem**: Each place must have exactly one owner (User), and users can own multiple places.

**Solution**: Added foreign key and relationship:

```python
class Place(BaseModel):
    # Foreign key for User relationship (one-to-many: User -> Place)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', backref='owned_places', foreign_keys=[owner_id])
```

**Updated `__init__` method**:

```python
def __init__(self, title, price, latitude, longitude, owner, description=None):
    super().__init__()
    self.title = title
    self.description = description
    self.price = price
    self.latitude = latitude
    self.longitude = longitude
    # Set owner (SQLAlchemy will handle owner_id)
    if not isinstance(owner, User):
        raise TypeError("Owner must be a User instance")
    self.owner = owner
```

**Why This Approach**:
- Removed `@property` decorator to avoid conflict with SQLAlchemy relationship
- Direct assignment `self.owner = owner` allows SQLAlchemy to manage `owner_id`
- Type validation ensures only User instances can be owners
- `backref='owned_places'` creates reverse relationship on User model

**How It Works**:
1. When you set `place.owner = user`, SQLAlchemy automatically sets `place.owner_id = user.id`
2. `backref` creates `user.owned_places` collection automatically
3. Both directions are bidirectional and kept in sync

### 3. Place-Amenity Relationship

**File**: `app/models/place.py`

**Problem**: Places can have multiple amenities, and amenities can belong to multiple places.

**Solution**: Added many-to-many relationship using secondary table:

```python
class Place(BaseModel):
    # Many-to-many relationship with Amenity
    amenities_rel = db.relationship('Amenity', secondary='place_amenity', backref='places_list', lazy=True)
```

**Backward Compatibility**:

```python
def __init__(self, ...):
    # Keeping amenities list for backward compatibility
    self.amenities = []
```

**Why This Approach**:
- `secondary='place_amenity'` references the association table
- `amenities_rel` is the SQLAlchemy relationship (database-backed)
- `self.amenities = []` maintains compatibility with in-memory code
- `backref='places_list'` creates reverse relationship on Amenity

**How It Works**:
- `place.amenities_rel.append(amenity)` adds relationship in database
- SQLAlchemy automatically manages the association table entries
- Both `place.amenities_rel` and `amenity.places_list` stay synchronized

### 4. Review-User Relationship

**File**: `app/models/review.py`

**Problem**: Each review is written by exactly one user, and users can write multiple reviews.

**Solution**: Added foreign key and relationship:

```python
class Review(BaseModel):
    # Foreign key for User relationship
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationship
    user = db.relationship('User', backref='user_reviews', foreign_keys=[user_id])
```

**Updated `__init__` method**:

```python
def __init__(self, text, rating, place, user):
    super().__init__()
    self.text = text
    self.rating = rating
    # Validate and set relationships
    if place is not None and not isinstance(place, Place):
        raise TypeError("Place must be a place instance")
    if user is not None and not isinstance(user, User):
        raise TypeError("User must be a user instance")
    self.place = place
    self.user = user
```

**Why This Approach**:
- Removed `@property` decorators to use SQLAlchemy relationships directly
- Type validation preserves data integrity
- `backref='user_reviews'` creates `user.user_reviews` collection

**How It Works**:
- Assigning `review.user = user` automatically sets `review.user_id`
- Accessing `user.user_reviews` returns all reviews by that user
- SQLAlchemy manages the bidirectional relationship

### 5. Review-Place Relationship

**File**: `app/models/review.py`

**Problem**: Each review is about exactly one place, and places can have multiple reviews. Additionally, each user can only review a place once.

**Solution**: Added foreign key, relationship, and unique constraint:

```python
class Review(BaseModel):
    # Foreign key for Place relationship
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relationship
    place = db.relationship('Place', backref='reviews', foreign_keys=[place_id])

    # Unique constraint: one review per user per place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )
```

**Why This Approach**:
- `__table_args__` adds database-level constraint
- Unique constraint on (user_id, place_id) prevents duplicate reviews
- `backref='reviews'` creates `place.reviews` collection
- Removed `@property` decorator to avoid conflicts

**How It Works**:
- Database enforces one review per user per place
- Attempting duplicate review raises `IntegrityError`
- Both `review.place` and `place.reviews` are bidirectional

### 6. Models Package Update

**File**: `app/models/__init__.py`

**Problem**: SQLAlchemy needs to discover the association table to create it.

**Solution**: Export `place_amenity` table:

```python
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place, place_amenity
from app.models.review import Review

__all__ = ['User', 'Amenity', 'Place', 'Review', 'place_amenity']
```

**Why This Approach**:
- Importing `place_amenity` registers it with SQLAlchemy
- Ensures table is created during `db.create_all()`
- Makes it available for relationship definitions

---

## Database Schema

### Complete Schema After Task 8

**Tables**: 5 tables total (users, amenities, places, reviews, place_amenity)

### Users Table (from Task 6)

```sql
CREATE TABLE users (
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
)
```

### Amenities Table (from Task 7)

```sql
CREATE TABLE amenities (
    name VARCHAR(50) NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
)
```

### Places Table (Task 7 + Task 8)

```sql
CREATE TABLE places (
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id VARCHAR(36) NOT NULL,           -- ✅ Task 8
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(owner_id) REFERENCES users (id)  -- ✅ Task 8
)
```

**New in Task 8**:
- `owner_id` foreign key to users table
- Foreign key constraint ensures referential integrity

### Reviews Table (Task 7 + Task 8)

```sql
CREATE TABLE reviews (
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    user_id VARCHAR(36) NOT NULL,            -- ✅ Task 8
    place_id VARCHAR(36) NOT NULL,           -- ✅ Task 8
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT unique_user_place_review UNIQUE (user_id, place_id),  -- ✅ Task 8
    FOREIGN KEY(user_id) REFERENCES users (id),    -- ✅ Task 8
    FOREIGN KEY(place_id) REFERENCES places (id)   -- ✅ Task 8
)
```

**New in Task 8**:
- `user_id` foreign key to users table
- `place_id` foreign key to places table
- Unique constraint on (user_id, place_id) combination
- Two foreign key constraints for referential integrity

### Place-Amenity Association Table (Task 8)

```sql
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY(place_id) REFERENCES places (id),
    FOREIGN KEY(amenity_id) REFERENCES amenities (id)
)
```

**Features**:
- Composite primary key prevents duplicate associations
- Two foreign keys maintain referential integrity
- No additional columns needed for simple many-to-many

---

## Testing

### Test Results

✅ **ALL 115 TESTS PASSED** (100% success rate)

### Task 8 Specific Validations

1. **Database Tables Created**:
   - ✅ `place_amenity` association table created
   - ✅ Foreign keys added to places table (owner_id)
   - ✅ Foreign keys added to reviews table (user_id, place_id)

2. **Foreign Key Constraints**:
   - ✅ `places.owner_id` references `users.id`
   - ✅ `reviews.user_id` references `users.id`
   - ✅ `reviews.place_id` references `places.id`
   - ✅ `place_amenity.place_id` references `places.id`
   - ✅ `place_amenity.amenity_id` references `amenities.id`

3. **Unique Constraints**:
   - ✅ `unique_user_place_review` on (user_id, place_id) in reviews table
   - ✅ Composite primary key on place_amenity prevents duplicates

4. **Bidirectional Relationships**:
   - ✅ `user.owned_places` returns list of places owned by user
   - ✅ `place.owner` returns User instance
   - ✅ `user.user_reviews` returns list of reviews by user
   - ✅ `review.user` returns User instance
   - ✅ `place.reviews` returns list of reviews for place
   - ✅ `review.place` returns Place instance
   - ✅ `place.amenities_rel` returns list of amenities
   - ✅ `amenity.places_list` returns list of places

5. **Validation Preserved**:
   - ✅ All existing property validation still works
   - ✅ Type checking for relationship assignments
   - ✅ No breaking changes to existing functionality

### Test Execution

```bash
source venv/bin/activate && python tests/test.py
```

**Output**: All 115 tests passed successfully

---

## Best Practices

### 1. Removing Property Decorators for SQLAlchemy Relationships

**Problem**: Using `@property` decorators with SQLAlchemy relationships causes bidirectional attribute conflicts.

**Bad Pattern**:
```python
# ❌ Causes conflict
@property
def owner(self):
    return self._owner

@owner.setter
def owner(self, value):
    self._owner = value

owner = db.relationship('User', backref='owned_places')
```

**Good Pattern**:
```python
# ✅ Use SQLAlchemy relationship directly
owner = db.relationship('User', backref='owned_places', foreign_keys=[owner_id])

def __init__(self, ..., owner):
    if not isinstance(owner, User):
        raise TypeError("Owner must be a User instance")
    self.owner = owner  # SQLAlchemy manages this
```

**Why**: SQLAlchemy's relationship descriptor handles getting and setting automatically. Adding property decorators creates conflicts.

### 2. Foreign Key Column Naming

**Pattern**: Use `{relationship_name}_id` for foreign key columns

```python
# Foreign key column
owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

# Relationship (no _id suffix)
owner = db.relationship('User', backref='owned_places', foreign_keys=[owner_id])
```

**Benefits**:
- Clear distinction between ID storage and object reference
- Follows SQLAlchemy conventions
- Easy to understand in database queries

### 3. Backref for Bidirectional Relationships

**Pattern**: Use `backref` parameter for automatic reverse relationship

```python
# In Place model
owner = db.relationship('User', backref='owned_places', foreign_keys=[owner_id])

# Automatically creates on User model:
# owned_places = db.relationship('Place', ...)
```

**Benefits**:
- DRY principle - define relationship once
- Both directions stay synchronized automatically
- Less code to maintain

### 4. Association Tables for Many-to-Many

**Pattern**: Use `db.Table()` for simple many-to-many associations

```python
# Association table (no model class)
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

# Relationship using secondary
amenities_rel = db.relationship('Amenity', secondary='place_amenity', backref='places_list')
```

**When to Use**:
- Simple many-to-many with no additional attributes
- No need to track creation time or other metadata
- Composite primary key is sufficient

**When NOT to Use**:
- Need to store additional data about the relationship
- Need timestamps on associations
- In these cases, create a full model class instead

### 5. Unique Constraints on Relationships

**Pattern**: Use `__table_args__` for multi-column constraints

```python
class Review(BaseModel):
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )
```

**Benefits**:
- Database enforces business rules
- Prevents duplicate relationships at schema level
- Better than application-level validation alone

### 6. Type Validation in `__init__`

**Pattern**: Validate relationship types before assignment

```python
def __init__(self, text, rating, place, user):
    if place is not None and not isinstance(place, Place):
        raise TypeError("Place must be a place instance")
    if user is not None and not isinstance(user, User):
        raise TypeError("User must be a user instance")
    self.place = place
    self.user = user
```

**Benefits**:
- Catches errors early during object creation
- Provides clear error messages
- Complements database constraints

---

## Summary

Task 8 successfully completed database relationships for all models:

**Files Modified**: 3 files

- ✅ `app/models/place.py`
  - Added `place_amenity` association table
  - Added `owner_id` foreign key
  - Added `owner` relationship with backref
  - Added `amenities_rel` many-to-many relationship
  - Removed `@property` decorators for `owner`

- ✅ `app/models/review.py`
  - Added `user_id` foreign key
  - Added `place_id` foreign key
  - Added `user` relationship with backref
  - Added `place` relationship with backref
  - Added unique constraint on (user_id, place_id)
  - Removed `@property` decorators for `user` and `place`

- ✅ `app/models/__init__.py`
  - Exported `place_amenity` table for SQLAlchemy registration

**Database Schema**:
- ✅ 5 tables total (users, amenities, places, reviews, place_amenity)
- ✅ 5 foreign key constraints added
- ✅ 1 unique constraint added (user_id, place_id in reviews)
- ✅ 1 association table for many-to-many (place_amenity)

**Relationships Implemented**:
- ✅ User → Place (one-to-many via owner_id)
- ✅ User → Review (one-to-many via user_id)
- ✅ Place → Review (one-to-many via place_id)
- ✅ Place ↔ Amenity (many-to-many via place_amenity)

**Validation**:
- ✅ All existing property validation preserved
- ✅ Type checking for relationship assignments
- ✅ Database constraints enforcing referential integrity
- ✅ No breaking changes to existing code
- ✅ All 115 tests passing (100% success rate)

**Next Steps**:
- Task 9: Migrate remaining repositories (Place, Review, Amenity) from in-memory to SQLAlchemy
- Task 10: Create SQL scripts for database initialization
- Task 11: Generate ER diagram

---

**Previous**: [Task 7: Database Mapping](TASK_07.md)
**Next**: [Task 9: Repository Migration](TASK_09.md)
