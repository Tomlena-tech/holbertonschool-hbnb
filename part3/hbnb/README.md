# HBnB Part 3 - In-Memory Implementation

This directory contains the Part 3 implementation of the HBnB project using in-memory storage.

## Structure

```
hbnb/
├── app/                  # Application package
│   ├── __init__.py      # App factory
│   ├── models/          # Data models (User, Place, Review, Amenity)
│   ├── persistence/     # Repository pattern (InMemory)
│   ├── services/        # Business logic (Facade)
│   └── api/             # REST API endpoints
├── run.py               # Application entry point
├── config.py            # Configuration (dev/prod/test)
└── requirements.txt     # Python dependencies
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

The API will be available at `http://localhost:5000/api/v1/`

## Features

- ✅ Complete REST API (17 endpoints)
- ✅ CRUD operations for all entities
- ✅ Business rules (no self-review, no duplicate reviews)
- ✅ In-memory persistence with Repository pattern
- ✅ Facade pattern for business logic
- ✅ Swagger documentation

## API Endpoints

- `/api/v1/users` - User management
- `/api/v1/amenities` - Amenity management
- `/api/v1/places` - Place management
- `/api/v1/reviews` - Review management

## Testing

All 10 tasks validated. See `../VERIFICATION_TASKS_1-10.md` for details.
