# Task 6: User Database Mapping with SQLAlchemy

## Overview

This document describes the implementation of SQLAlchemy ORM mappings for the User model, completing the database persistence layer started in Task 5.

**Task Objective**: Map the User model to a database table using SQLAlchemy while maintaining existing property-based validation and password hashing functionality.

**Completion Date**: November 8, 2025
**Status**: ✅ Completed and Tested

---

## Table of Contents

1. [Requirements](#requirements)
2. [Technical Challenges](#technical-challenges)
3. [Implementation Details](#implementation-details)
4. [Architecture](#architecture)
5. [Testing Results](#testing-results)
6. [Troubleshooting](#troubleshooting)

---

## Requirements

### Functional Requirements

1. **SQLAlchemy Model Mapping**:
   - Inherit User model from `db.Model`
   - Add `__tablename__` to specify table name
   - Map all attributes to SQLAlchemy columns
   - Preserve existing property-based validation

2. **Database Initialization**:
   - Create database tables with `db.create_all()`
   - Ensure tables created before admin seeding
   - Handle application context requirements

3. **Circular Import Resolution**:
   - Resolve circular import issues with `db` instance
   - Enable models to access `db` without import errors
   - Maintain clean architecture

4. **Repository Integration**:
   - Create specialized `UserRepository` class
   - Extend `SQLAlchemyRepository` with user-specific methods
   - Integrate with facade layer

### Non-Functional Requirements

- Maintain backward compatibility with existing code
- Preserve password hashing functionality
- Keep property validation logic intact
- Clean separation of concerns

---

## Technical Challenges

### Challenge 1: Circular Import with `db` Instance

**Problem**:
```
app/__init__.py imports API namespaces
  → API modules import facade
    → facade imports repository
      → repository imports db from app
        → app/__init__.py (circular!)
```

**Solution**: Created `app/extensions.py` module to initialize extensions independently:

```python
# app/extensions.py
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
```

**Why this works**:
- Extensions are initialized before app creation
- Models can import from `app.extensions` instead of `app`
- Breaks the circular dependency chain
- Standard Flask pattern for large applications

### Challenge 2: Property Decorators vs SQLAlchemy Columns

**Problem**: Property decorators with the same name as columns were overriding SQLAlchemy's column definitions, preventing proper database schema creation.

**Solution**: Map SQLAlchemy columns to the internal private attributes used by properties:

```python
class User(BaseModel):
    __tablename__ = 'users'

    # Column name maps to private attribute used by @property
    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    _User__is_admin = db.Column('is_admin', db.Boolean, default=False, nullable=False)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        # Validation logic
        self._first_name = value
```

**How it works**:
- Column attribute: `_first_name` (what SQLAlchemy uses)
- Database column name: `'first_name'` (first parameter to `db.Column()`)
- Property accessor: `first_name` (what API uses)
- Preserves validation while enabling database mapping

### Challenge 3: Model Registration Before Table Creation

**Problem**: `db.create_all()` needs models to be imported and registered with SQLAlchemy before it can create tables.

**Solution**: Import models explicitly in application context:

```python
# app/__init__.py
with app.app_context():
    from app import models  # Register models
    db.create_all()         # Create tables
    seed_admin_user(app)    # Seed admin
```

---

## Implementation Details

### 1. Created Extensions Module

**File**: `app/extensions.py` (NEW)

```python
"""
Flask extensions module.

This module initializes Flask extensions separately from the app factory
to avoid circular import issues.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
```

**Purpose**: Centralized extension initialization that breaks circular imports.

### 2. Updated BaseModel with SQLAlchemy

**File**: `app/models/base_model.py`

```python
from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Abstract base model with common attributes for all entities.
    Inherits from SQLAlchemy's db.Model for ORM functionality.
    """

    __abstract__ = True  # Prevent table creation for BaseModel

    # SQLAlchemy column mappings
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow,
                          nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow, nullable=False)

    # ... rest of the methods remain unchanged
```

**Key Changes**:
- Inherits from `db.Model` instead of plain Python class
- Added `__abstract__ = True` to prevent table creation
- SQLAlchemy column definitions for common attributes
- Imports `db` from `app.extensions`

### 3. Mapped User Model Columns

**File**: `app/models/user.py`

```python
from app.models.base_model import BaseModel
from app.extensions import db
from flask import current_app


class User(BaseModel):
    """User model with SQLAlchemy ORM mapping."""

    __tablename__ = 'users'

    # SQLAlchemy columns mapped to private attributes
    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    _User__is_admin = db.Column('is_admin', db.Boolean, default=False,
                                 nullable=False)

    # Properties continue to work as before
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name must be between 1 and 50 characters")
        self._first_name = value

    # ... rest of properties and methods remain unchanged
```

**Column Mapping Strategy**:

| Python Attribute | Database Column | Property Accessor |
|------------------|----------------|-------------------|
| `_first_name` | `first_name` | `first_name` |
| `_last_name` | `last_name` | `last_name` |
| `_email` | `email` | `email` |
| `password` | `password` | `password` (direct) |
| `_User__is_admin` | `is_admin` | `is_admin` |

### 4. Created UserRepository

**File**: `app/persistence/user_repository.py` (NEW)

```python
"""
User Repository Module

This module provides a specialized repository for User model operations,
extending the base SQLAlchemyRepository with user-specific functionality.
"""

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User model with specialized query methods.

    Extends SQLAlchemyRepository to provide user-specific operations
    such as email-based lookups for authentication purposes.
    """

    def __init__(self):
        """Initialize UserRepository with User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.

        This method is commonly used for authentication and login flows
        where the email serves as the unique identifier for user lookup.

        Args:
            email (str): The email address to search for.

        Returns:
            User: The user instance if found, None otherwise.
        """
        return self.get_by_attribute('email', email)
```

**Benefits**:
- Domain-specific method: `get_user_by_email()`
- Extends generic `SQLAlchemyRepository`
- Clean abstraction for user operations
- Easy to add more user-specific queries

### 5. Fixed Repository Circular Import

**File**: `app/persistence/repository.py`

```python
class SQLAlchemyRepository(Repository):
    """
    Database repository implementation using SQLAlchemy ORM.
    """

    @property
    def _db(self):
        """Late import of db to avoid circular imports."""
        from app.extensions import db
        return db

    def __init__(self, model):
        """Initialize repository with a SQLAlchemy model class."""
        self.model = model

    def add(self, obj):
        """Add a new object to the database."""
        self._db.session.add(obj)
        self._db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self._db.session.get(self.model, obj_id)

    # ... rest of methods use self._db instead of db
```

**Key Change**: Property-based late import of `db` ensures it's imported only when needed, after app initialization.

### 6. Updated Application Initialization

**File**: `app/__init__.py`

```python
from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    app.extensions['bcrypt'] = bcrypt
    jwt.init_app(app)
    app.extensions['jwt'] = jwt
    db.init_app(app)  # Initialize SQLAlchemy

    # Register API (import inside function to avoid circular imports)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Import and register API namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Database initialization and admin seeding
    with app.app_context():
        # Import models to register with SQLAlchemy
        from app import models

        # Create database tables
        db.create_all()

        # Seed admin user
        seed_admin_user(app)

    return app
```

**Critical Order**:
1. Initialize extensions with app
2. Import API namespaces (now safe, no circular imports)
3. Import models to register with SQLAlchemy
4. Create database tables (`db.create_all()`)
5. Seed admin user

### 7. Created Models Package Init

**File**: `app/models/__init__.py`

```python
"""
Models package initialization.

This module exports all model classes to ensure they're registered
with SQLAlchemy when imported.
"""

from app.models.user import User

__all__ = ['User']
```

**Purpose**: Ensures User model is imported when `from app import models` is called.

### 8. Updated Facade to Use UserRepository

**File**: `app/services/facade.py`

```python
from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade class centralizing access to repositories.
    """

    def __init__(self):
        """
        Initialize repositories.
        User repository uses SQLAlchemy for database persistence,
        others use in-memory storage.
        """
        self.user_repo = UserRepository()      # ✅ Database with specialized methods
        self.place_repo = InMemoryRepository()  # In-memory for now
        self.review_repo = InMemoryRepository() # In-memory for now
        self.amenity_repo = InMemoryRepository() # In-memory for now

    # ... rest of methods remain unchanged
```

---

## Architecture

### Database Schema Created

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

### Data Flow: User Creation

```
┌────────────────────────────────────────────────────────────┐
│                  USER CREATION WITH DATABASE                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. POST /api/v1/users/                                   │
│     ├─ Request: {"first_name": "John", ...}              │
│     │                                                      │
│  2. users_api.post()                                      │
│     ├─ JWT validation (@jwt_required)                     │
│     ├─ Admin check (is_admin claim)                       │
│     │                                                      │
│  3. facade.create_user(data)                              │
│     ├─ user = User(**data)                                │
│     │   ├─ Property setters validate data                 │
│     │   └─ hash_password() hashes password                │
│     │                                                      │
│  4. user_repo.add(user)                                   │
│     ├─ UserRepository.add(user)                           │
│     │   ├─ db.session.add(user)                           │
│     │   └─ db.session.commit()                            │
│     │       └─ SQLAlchemy maps object to table            │
│     │           └─ INSERT INTO users VALUES (...)         │
│     │               └─ ✅ Persisted to database            │
│     │                                                      │
│  5. Return serialized user                                │
│     └─ Response: {"id": "...", "email": "...", ...}      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Architecture Benefits

**Clean Separation of Concerns**:
- Extensions module provides dependency injection point
- Models focus on business logic and validation
- Repositories handle data persistence
- No circular dependencies

**Backward Compatibility**:
- Existing property-based validation preserved
- Password hashing still works correctly
- API endpoints unchanged
- Business logic unaffected

**Scalability**:
- Pattern reusable for all models (Place, Review, Amenity)
- Generic repository implementation
- Database-agnostic (SQLite, PostgreSQL, MySQL)

---

## Testing Results

### Test 1: Database Schema
✅ **PASSED**: Tables created successfully
```
Tables: ['amenity', 'place', 'review', 'users']
```

✅ **PASSED**: User table schema correct
```
User table columns:
  first_name           VARCHAR(50)     NOT NULL
  last_name            VARCHAR(50)     NOT NULL
  email                VARCHAR(120)    NOT NULL
  password             VARCHAR(128)    NOT NULL
  is_admin             BOOLEAN         NOT NULL
  id                   VARCHAR(36)     NOT NULL
  created_at           DATETIME        NOT NULL
  updated_at           DATETIME        NOT NULL
```

### Test 2: Admin User Seeding
✅ **PASSED**: Admin user created on app startup
```
Admin exists: True
Is admin: True
Email: admin@hbnb.io
Password hashed: $2b$12$F6C...
```

### Test 3: Password Verification
✅ **PASSED**: Correct password accepted
✅ **PASSED**: Wrong password rejected

### Test 4: User CRUD Operations
✅ **PASSED**: User creation persists to database
✅ **PASSED**: User retrieval by ID works
✅ **PASSED**: User update works
✅ **PASSED**: Changes persist across operations

### Test 5: Password Update Hashing
✅ **PASSED**: Password update triggers hashing
✅ **PASSED**: New hashed password stored in database
✅ **PASSED**: New password verification works

### Test 6: Get User by Email
✅ **PASSED**: Email-based lookup works
✅ **PASSED**: UserRepository method functions correctly

### Test 7: Get All Users
✅ **PASSED**: All users retrieved from database
✅ **PASSED**: Multiple users supported

---

## Troubleshooting

### Issue 1: "cannot import name 'db' from partially initialized module 'app'"

**Cause**: Circular import when trying to import `db` from `app` module.

**Solution**: Import from `app.extensions` instead:
```python
# ❌ Don't do this
from app import db

# ✅ Do this
from app.extensions import db
```

### Issue 2: Properties not working after SQLAlchemy mapping

**Cause**: SQLAlchemy columns overriding property definitions.

**Solution**: Map columns to private attributes:
```python
# Column maps to private attribute
_first_name = db.Column('first_name', db.String(50))

# Property uses private attribute
@property
def first_name(self):
    return self._first_name
```

### Issue 3: "No such table: users"

**Cause**: `db.create_all()` not called or called before models imported.

**Solution**: Import models before calling `db.create_all()`:
```python
with app.app_context():
    from app import models  # Import first!
    db.create_all()        # Then create tables
```

---

## Lessons Learned

1. **Extensions Module Pattern**: Creating a separate extensions module is a Flask best practice that prevents circular imports in large applications

2. **Column Mapping Flexibility**: SQLAlchemy's `db.Column('name', ...)` syntax allows Python attribute names to differ from database column names, enabling property integration

3. **Model Registration**: Models must be imported before `db.create_all()` for SQLAlchemy to know which tables to create

4. **Late Imports**: Property-based late imports (`@property def _db()`) provide flexibility for resolving circular dependencies

5. **Order Matters**: Extension initialization → API imports → Model imports → Table creation → Data seeding

6. **Specialized Repositories**: Extending generic repositories with domain-specific methods (like `get_user_by_email()`) improves code organization

---

## Summary

Task 6 successfully completed the database persistence layer by:

✅ **Created extensions module** to break circular imports
✅ **Mapped User model** to database table with SQLAlchemy
✅ **Preserved property validation** while adding ORM functionality
✅ **Created UserRepository** with specialized query methods
✅ **Initialized database tables** with `db.create_all()`
✅ **Maintained backward compatibility** with existing code
✅ **All tests passing** including CRUD operations and password hashing

**Files Modified**: 7 files
**New Files**: 3 files (`app/extensions.py`, `app/persistence/user_repository.py`, `app/models/__init__.py`)
**Database**: SQLite with 4 tables (users, place, review, amenity)

**Next Steps (Task 7)**: Map Place, Review, and Amenity models to database tables and establish relationships between entities.

---

**Previous**: [Task 5: Database Repository Implementation](TASK_05.md)
**Next**: [Task 7: More Database Mapping](TASK_07.md)
