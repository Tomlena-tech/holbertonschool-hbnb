# HBnB - BL and API

## Project Overview

This project implements a modular HBnB (Holberton BnB) application with a clear separation of concerns across three layers:

- **Presentation Layer (API)**: Handles HTTP requests and responses
- **Business Logic Layer (Models & Services)**: Contains the core business logic
- **Persistence Layer**: Manages data storage with SQLAlchemy ORM (SQLite for development, MySQL for production)

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── api/                     # Presentation layer
│   │   ├── __init__.py
│   │   ├── v1/                  # API version 1
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       ├── amenities.py     # Amenity endpoints
│   ├── models/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   ├── amenity.py           # Amenity model
│   ├── services/                # Service layer (Facade pattern)
│   │   ├── __init__.py          # Facade singleton instance
│   │   ├── facade.py            # HBnBFacade class
│   ├── persistence/             # Persistence layer
│       ├── __init__.py
│       ├── repository.py        # Repository interface and in-memory implementation
├── run.py                       # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
```

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Flask application in development mode:

```bash
python run.py
```

The application will run on `http://127.0.0.1:5000/` with debug mode enabled.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

```
http://127.0.0.1:5000/api/v1/
```

## Architecture

### Facade Pattern

The `HBnBFacade` class in `app/services/facade.py` serves as the main interface between the presentation layer and the business logic/persistence layers. It manages all repositories and coordinates operations across different entities.

### Repository Pattern

The `Repository` abstract base class defines the interface for data persistence operations. The `InMemoryRepository` implementation provides in-memory storage for development and testing. This will be replaced with a database-backed implementation in Part 3.

## Business Logic Layer

The Business Logic layer contains the core entities and their business rules. All models inherit from `BaseModel` which provides common functionality.

### BaseModel

The `BaseModel` class (`app/models/base_model.py`) provides common attributes and methods for all entities:

- **Attributes**:
  - `id` (str): Universally unique identifier (UUID)
  - `created_at` (datetime): Timestamp when the object was created
  - `updated_at` (datetime): Timestamp when the object was last modified

- **Methods**:
  - `save()`: Updates the `updated_at` timestamp
  - `update(data)`: Updates object attributes from a dictionary
  - `is_max_length(name, value, max_length)`: Validates string length
  - `is_in_range(name, value, min, max)`: Validates numeric ranges

### Entities

#### User

The `User` class (`app/models/user.py`) represents users in the system.

**Attributes**:
- `first_name` (str): User's first name (max 50 characters, required)
- `last_name` (str): User's last name (max 50 characters, required)
- `email` (str): Unique email address with format validation (required)
- `is_admin` (bool): Administrative privileges flag (default: False)
- `places` (list): Places owned by the user
- `reviews` (list): Reviews written by the user

**Methods**:
- `add_place(place)`: Associate a place with the user
- `add_review(review)`: Associate a review with the user
- `delete_review(review)`: Remove a review from the user

**Example**:
```python
from app.models.user import User

# Create a new user
user = User(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    is_admin=False
)

print(f"User ID: {user.id}")
print(f"Created at: {user.created_at}")
```

#### Place

The `Place` class (`app/models/place.py`) represents accommodations/properties.

**Attributes**:
- `title` (str): Place title (max 100 characters, required)
- `description` (str): Detailed description (optional)
- `price` (float): Price per night (must be positive)
- `latitude` (float): Latitude coordinate (-90.0 to 90.0)
- `longitude` (float): Longitude coordinate (-180.0 to 180.0)
- `owner` (User): User instance who owns the place (required)
- `reviews` (list): Reviews associated with the place
- `amenities` (list): Amenities available at the place

**Methods**:
- `add_review(review)`: Add a review to the place
- `delete_review(review)`: Remove a review from the place
- `add_amenity(amenity)`: Add an amenity to the place

**Example**:
```python
from app.models.user import User
from app.models.place import Place

# Create owner
owner = User(
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com"
)

# Create a place
place = Place(
    title="Cozy Apartment",
    description="A nice place to stay",
    price=100.0,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner
)

# Associate place with owner
owner.add_place(place)
```

#### Review

The `Review` class (`app/models/review.py`) represents user reviews of places.

**Attributes**:
- `text` (str): Review content (required)
- `rating` (int): Rating from 1 to 5 (required)
- `place` (Place): Place being reviewed (required)
- `user` (User): User who wrote the review (required)

**Example**:
```python
from app.models.review import Review

# Create a review
review = Review(
    text="Great stay! Very comfortable.",
    rating=5,
    place=place,
    user=user
)

# Associate review with place and user
place.add_review(review)
user.add_review(review)
```

#### Amenity

The `Amenity` class (`app/models/amenity.py`) represents features/services available at places.

**Attributes**:
- `name` (str): Amenity name (max 50 characters, required)

**Example**:
```python
from app.models.amenity import Amenity

# Create amenities
wifi = Amenity(name="Wi-Fi")
parking = Amenity(name="Free Parking")
pool = Amenity(name="Swimming Pool")

# Add amenities to a place
place.add_amenity(wifi)
place.add_amenity(parking)
place.add_amenity(pool)
```

### Relationships

The entities have the following relationships:

1. **User → Place** (One-to-Many)
   - A user can own multiple places
   - Each place has exactly one owner

2. **Place → Review** (One-to-Many)
   - A place can have multiple reviews
   - Each review belongs to one place

3. **User → Review** (One-to-Many)
   - A user can write multiple reviews
   - Each review is written by one user

4. **Place → Amenity** (Many-to-Many)
   - A place can have multiple amenities
   - An amenity can be associated with multiple places

### Data Validation

All entities include comprehensive validation:

- **String Length**: Maximum character limits enforced
- **Email Format**: Regex validation for proper email format
- **Email Uniqueness**: Ensures no duplicate emails across users
- **Numeric Ranges**: Latitude, longitude, and rating constraints
- **Positive Values**: Price must be positive
- **Type Checking**: All attributes are type-validated
- **Required Fields**: Non-empty validation for required attributes

### Complete Usage Example

```python
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

# Create users
owner = User(
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com"
)

guest = User(
    first_name="Bob",
    last_name="Johnson",
    email="bob@example.com"
)

# Create a place
place = Place(
    title="Beachfront Villa",
    description="Beautiful villa with ocean view",
    price=250.0,
    latitude=36.7783,
    longitude=-119.4179,
    owner=owner
)

# Add amenities
wifi = Amenity(name="Wi-Fi")
pool = Amenity(name="Pool")
place.add_amenity(wifi)
place.add_amenity(pool)

# Create a review
review = Review(
    text="Amazing place! Highly recommend.",
    rating=5,
    place=place,
    user=guest
)

# Establish relationships
owner.add_place(place)
place.add_review(review)
guest.add_review(review)

# Access related data
print(f"Place: {place.title}")
print(f"Owner: {place.owner.first_name} {place.owner.last_name}")
print(f"Amenities: {[a.name for a in place.amenities]}")
print(f"Reviews: {len(place.reviews)}")
print(f"Average Rating: {review.rating}")
```