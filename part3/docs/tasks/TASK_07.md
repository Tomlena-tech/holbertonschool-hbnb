# Task 7: Database Mapping for Place, Review, and Amenity Models

## Overview

This document describes the implementation of SQLAlchemy ORM mappings for the Place, Review, and Amenity models, extending database persistence beyond the User model.

**Task Objective**: Map Place, Review, and Amenity entities to database tables using SQLAlchemy ORM while maintaining existing property-based validation. Relationships between entities are deferred to Task 8.

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

1. **Map Amenity Model**:
   - Add `__tablename__ = 'amenities'`
   - Map `name` column with unique constraint
   - Preserve existing property validation

2. **Map Place Model**:
   - Add `__tablename__ = 'places'`
   - Map columns: title, description, price, latitude, longitude
   - Preserve existing property validation
   - Defer relationships to Task 8

3. **Map Review Model**:
   - Add `__tablename__ = 'reviews'`
   - Map columns: text, rating
   - Preserve existing property validation
   - Defer relationships to Task 8

4. **Update Models Package**:
   - Export all models from `app/models/__init__.py`
   - Ensure models are registered with SQLAlchemy

### Non-Functional Requirements

- Maintain backward compatibility with existing code
- Preserve all existing validation logic
- Follow same pattern established in Task 6 (User model)
- No breaking changes to API endpoints
- Clean separation of concerns

---

## Architecture

### Model Mapping Strategy

Following the pattern established in Task 6, each model follows this structure:

```
┌─────────────────────────────────────────────────────────────┐
│                    Model Class Structure                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  class ModelName(BaseModel):                                │
│      __tablename__ = 'table_name'                           │
│                                                              │
│      # SQLAlchemy column mappings to private attributes     │
│      _attribute = db.Column('column_name', Type, ...)       │
│                                                              │
│      def __init__(self, ...):                               │
│          # Initialize with validation via properties        │
│                                                              │
│      @property                                               │
│      def attribute(self):                                    │
│          return self._attribute                             │
│                                                              │
│      @attribute.setter                                       │
│      def attribute(self, value):                            │
│          # Validation logic                                 │
│          self._attribute = value                            │
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
│  ├─ user_repo: UserRepository                               │
│  ├─ place_repo: InMemoryRepository (Task 8: migrate)        │
│  ├─ review_repo: InMemoryRepository (Task 8: migrate)       │
│  └─ amenity_repo: InMemoryRepository (Task 8: migrate)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Model Layer                          │
├─────────────────────────────────────────────────────────────┤
│  BaseModel (db.Model, __abstract__=True)                    │
│  ├─ User (mapped in Task 6)                                 │
│  ├─ Amenity (mapped in Task 7) ✅                           │
│  ├─ Place (mapped in Task 7) ✅                             │
│  └─ Review (mapped in Task 7) ✅                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
├─────────────────────────────────────────────────────────────┤
│  SQLAlchemy ORM → SQLite Database                           │
│  Tables: users, amenities, places, reviews                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### 1. Amenity Model Mapping

**File**: `app/models/amenity.py`

**Code Changes**:

```python
from .base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """
    Amenity model with SQLAlchemy ORM mapping.

    Represents amenities that can be associated with places.
    """

    __tablename__ = 'amenities'

    # SQLAlchemy column mapping
    _name = db.Column('name', db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        super().is_max_length('Name', value, 50)
        self._name = value
```

**Key Features**:
- **Column**: `name` (VARCHAR(50), NOT NULL, UNIQUE)
- **Validation**: Type checking, empty string check, max length 50
- **Unique Constraint**: Prevents duplicate amenity names
- **Property Pattern**: Uses `_name` internally, exposes `name` via property

### 2. Place Model Mapping

**File**: `app/models/place.py`

**Code Changes**:

```python
from .base_model import BaseModel
from .user import User
from app.extensions import db


class Place(BaseModel):
    """
    Represents a place / accommodation with SQLAlchemy ORM mapping.
    """

    __tablename__ = 'places'

    # SQLAlchemy column mappings (no relationships yet - Task 8)
    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.Text, nullable=True)
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)
```

**Column Specifications**:

| Column | Type | Constraints | Validation |
|--------|------|-------------|------------|
| `title` | VARCHAR(100) | NOT NULL | Non-empty, max 100 chars |
| `description` | TEXT | NULL | Optional, string type |
| `price` | FLOAT | NOT NULL | Non-negative numeric |
| `latitude` | FLOAT | NOT NULL | Range: -90.0 to 90.0 |
| `longitude` | FLOAT | NOT NULL | Range: -180.0 to 180.0 |

**Property Updates**:

All properties updated to use private attributes:
- `self.__title` → `self._title`
- `self.__description` → `self._description`
- `self.__price` → `self._price`
- `self.__latitude` → `self._latitude`
- `self.__longitude` → `self._longitude`

**Note**: Owner relationship (`owner_id` foreign key) will be added in Task 8.

### 3. Review Model Mapping

**File**: `app/models/review.py`

**Code Changes**:

```python
from .base_model import BaseModel
from .place import Place
from .user import User
from app.extensions import db


class Review(BaseModel):
    """
    Review model with SQLAlchemy ORM mapping.

    Represents a review written by a user about a place.
    """

    __tablename__ = 'reviews'

    # SQLAlchemy column mappings (no relationships yet - Task 8)
    _text = db.Column('text', db.Text, nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)
```

**Column Specifications**:

| Column | Type | Constraints | Validation |
|--------|------|-------------|------------|
| `text` | TEXT | NOT NULL | Non-empty string |
| `rating` | INTEGER | NOT NULL | Range: 1-5 |

**Property Updates**:
- `self.__text` → `self._text`
- `self.__rating` → `self._rating`

**Note**: Foreign keys `user_id` and `place_id` will be added in Task 8.

### 4. Models Package Update

**File**: `app/models/__init__.py`

**Before**:
```python
from app.models.user import User

# TODO: Import other models when they are migrated to SQLAlchemy
# from app.models.amenity import Amenity
# from app.models.place import Place
# from app.models.review import Review

__all__ = ['User']
```

**After**:
```python
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

__all__ = ['User', 'Amenity', 'Place', 'Review']
```

**Purpose**:
- Ensures all models are imported when `from app import models` is executed
- Registers models with SQLAlchemy before `db.create_all()`
- Enables table creation during application initialization

---

## Database Schema

### Tables Created

After Task 7 implementation, the database contains 4 tables:

1. **users** (from Task 6)
2. **amenities** (new in Task 7)
3. **places** (new in Task 7)
4. **reviews** (new in Task 7)

### Amenities Table

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

**Inherited from BaseModel**:
- `id`: UUID string (36 characters)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last modification

**Business Constraints**:
- Name must be unique across all amenities
- Maximum length: 50 characters

### Places Table

```sql
CREATE TABLE places (
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
)
```

**Business Constraints**:
- Title required (max 100 characters)
- Description optional (unlimited length)
- Price must be non-negative
- Latitude must be between -90.0 and 90.0
- Longitude must be between -180.0 and 180.0

**Missing (Task 8)**:
- `owner_id` foreign key to users table

### Reviews Table

```sql
CREATE TABLE reviews (
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
)
```

**Business Constraints**:
- Text required (unlimited length)
- Rating must be between 1 and 5

**Missing (Task 8)**:
- `user_id` foreign key to users table
- `place_id` foreign key to places table
- Unique constraint on (user_id, place_id)

---

## Testing

### Test 1: Model Imports
✅ **PASSED**: All models import without errors

```python
from app.models import User, Amenity, Place, Review
# No ImportError raised
```

### Test 2: Database Tables Created
✅ **PASSED**: All tables created successfully

Expected tables: `['amenities', 'places', 'reviews', 'users']`

### Test 3: Amenity Column Mapping
✅ **PASSED**: Columns mapped correctly

```python
# Columns: name, id, created_at, updated_at
# Constraints: name is UNIQUE
```

### Test 4: Place Column Mapping
✅ **PASSED**: Columns mapped correctly

```python
# Columns: title, description, price, latitude, longitude, id, created_at, updated_at
# All required columns present
```

### Test 5: Review Column Mapping
✅ **PASSED**: Columns mapped correctly

```python
# Columns: text, rating, id, created_at, updated_at
# All required columns present
```

### Test 6: Property Validation Preserved
✅ **PASSED**: All validation logic intact

- Amenity name validation (type, empty, max length)
- Place title validation (type, empty, max length)
- Place price validation (type, non-negative)
- Place coordinates validation (type, range)
- Review text validation (type, empty)
- Review rating validation (type, range)

### Test 7: Application Startup
✅ **PASSED**: Application starts without errors

```bash
python run.py
# No errors during initialization
```

---

## Best Practices

### 1. Column Naming Strategy

**Pattern**: Private attribute with underscore prefix

```python
# SQLAlchemy column (Python attribute)
_name = db.Column('name', ...)  # Database column name

# Property accessor (public interface)
@property
def name(self):
    return self._name
```

**Benefits**:
- Clean separation between storage and interface
- Property decorators can add validation
- Database column names remain clean (no underscores)

### 2. Validation Preservation

**Pattern**: Keep validation in property setters

```python
@property
def rating(self):
    return self._rating

@rating.setter
def rating(self, value):
    if not isinstance(value, int):
        raise TypeError("Rating must be an integer")
    super().is_in_range('Rating', value, 0, 6)
    self._rating = value  # Only set if validation passes
```

**Benefits**:
- Single source of truth for validation
- Validation runs on both creation and updates
- Database constraints complement application logic

### 3. Gradual Migration

**Pattern**: Migrate models incrementally

```python
# Task 6: User only
user_repo = SQLAlchemyRepository(User)  # Database
place_repo = InMemoryRepository()        # In-memory

# Task 7: Add table mappings (no repository changes yet)
# Task 8: Add relationships
# Task 9+: Migrate repositories to database
```

**Benefits**:
- Reduces risk of breaking changes
- Easier to test and debug
- Clear separation of concerns per task

### 4. Import Organization

**Pattern**: Import db from extensions module

```python
from app.extensions import db  # ✅ Correct

# NOT from app import db  # ❌ Causes circular import
```

**Benefits**:
- Avoids circular import issues
- Extensions initialized before models
- Follows Flask best practices

---

## Summary

Task 7 successfully completed database mapping for three additional models:

**Files Modified**: 4 files
- ✅ `app/models/amenity.py` - Added table mapping and column definition
- ✅ `app/models/place.py` - Added table mapping and 5 column definitions
- ✅ `app/models/review.py` - Added table mapping and 2 column definitions
- ✅ `app/models/__init__.py` - Exported all models for SQLAlchemy registration

**Database Schema**:
- ✅ 4 tables total (users, amenities, places, reviews)
- ✅ All columns mapped with appropriate types
- ✅ Constraints applied (NOT NULL, UNIQUE where needed)
- ✅ BaseModel attributes inherited (id, created_at, updated_at)

**Validation**:
- ✅ All existing property validation preserved
- ✅ No breaking changes to existing code
- ✅ Backward compatibility maintained

**Deferred to Task 8**:
- ⏭️ Foreign key columns (owner_id, user_id, place_id)
- ⏭️ SQLAlchemy relationships (User→Place, Place→Review, etc.)
- ⏭️ Association table for Place↔Amenity many-to-many

**Next Steps**: Task 8 will add relationships between entities using SQLAlchemy's relationship() function and foreign keys.

---

**Previous**: [Task 6: User Database Mapping](TASK_06.md)
**Next**: [Task 8: Entity Relationships](TASK_08.md)
