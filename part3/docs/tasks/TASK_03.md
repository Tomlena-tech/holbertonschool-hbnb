# Task 3: Authenticated User Access Endpoints

## Overview

This document describes the implementation of authentication and authorization for user-specific endpoints in the HBnB application, including ownership validation and access control.

**Task Objective**: Secure API endpoints to restrict access to authenticated users only, implementing JWT-based authorization with ownership validation for places, reviews, and user data modifications.

**Completion Date**: November 2025
**Status**: ✅ Completed

---

## Table of Contents

1. [Requirements](#requirements)
2. [Authorization Concepts](#authorization-concepts)
3. [Implementation Details](#implementation-details)
4. [Protected Endpoints](#protected-endpoints)
5. [Testing](#testing)
6. [Security Patterns](#security-patterns)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

### Functional Requirements

1. **Authenticated Endpoints**:
   - POST `/api/v1/places/` - Create place (authenticated users)
   - POST `/api/v1/reviews/` - Create review (authenticated users with restrictions)
   - PUT `/api/v1/places/<place_id>` - Update place (owners only)
   - PUT `/api/v1/reviews/<review_id>` - Update review (creators only)
   - DELETE `/api/v1/reviews/<review_id>` - Delete review (creators only)
   - PUT `/api/v1/users/<user_id>` - Update user (self only, limited fields)

2. **Public Endpoints** (No Authentication Required):
   - GET `/api/v1/places/` - List all places
   - GET `/api/v1/places/<place_id>` - View place details
   - GET `/api/v1/reviews/` - List all reviews
   - GET `/api/v1/amenities/` - List all amenities

3. **Business Rules**:
   - Users cannot review their own places
   - Users can only submit one review per place
   - Users cannot modify email or password via PUT endpoint
   - Place owners are automatically set to authenticated user
   - Review creators are automatically set to authenticated user

### Non-Functional Requirements

- Proper HTTP status codes (401, 403, 400)
- Clear error messages
- Ownership validation on all modifications
- Consistent authorization pattern across endpoints

---

## Authorization Concepts

### Authentication vs Authorization

```
┌──────────────────────────────────────────────────────────────┐
│                        Authentication                         │
├──────────────────────────────────────────────────────────────┤
│  "Who are you?"                                               │
│  ✅ User provides credentials (JWT token)                     │
│  ✅ System verifies identity                                  │
│  ✅ Result: Known user identity                               │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                         Authorization                         │
├──────────────────────────────────────────────────────────────┤
│  "What are you allowed to do?"                                │
│  ✅ User attempts to access resource                          │
│  ✅ System checks permissions/ownership                       │
│  ✅ Result: Access granted or denied                          │
└──────────────────────────────────────────────────────────────┘
```

**Example Scenarios**:

| Action | Authentication | Authorization | Result |
|--------|---------------|---------------|--------|
| View place list | ❌ Not required | ❌ Not required | ✅ Allow |
| Create place | ✅ Required | ✅ Any authenticated user | ✅ Allow |
| Update own place | ✅ Required | ✅ Owner check | ✅ Allow |
| Update others' place | ✅ Required | ❌ Not owner | ❌ Deny (403) |
| No token provided | ❌ Failed | N/A | ❌ Deny (401) |

### Ownership-Based Access Control

```
┌─────────────────────────────────────────────────────────────┐
│                  Resource Ownership Model                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User                                                        │
│   ├── owns → Places                                         │
│   │           └── has → Reviews (by other users)           │
│   └── creates → Reviews (for others' places)                │
│                                                              │
│  Access Rules:                                               │
│  • Can UPDATE/DELETE own resources                           │
│  • Cannot UPDATE/DELETE others' resources                    │
│  • Cannot review own places                                  │
│  • Can only review each place once                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### 1. Place Endpoints

#### Create Place (Authenticated)

**File**: `app/api/v1/places.py`

```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(
        fields.String,
        required=False,
        description="List of amenity IDs"
    )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @jwt_required()  # ← Requires authentication
    def post(self):
        """
        Create a new place (Authenticated users only).

        The owner_id is automatically set to the authenticated user.
        """
        # Get authenticated user's ID from JWT token
        current_user = get_jwt_identity()

        # Get place data from request
        place_data = api.payload

        # Set owner to authenticated user
        place_data['owner_id'] = current_user

        # Set amenities to empty list if not provided
        if 'amenities' not in place_data:
            place_data['amenities'] = []

        # Create place
        new_place = facade.create_place(place_data)
        if not new_place:
            return {'error': 'Owner not found'}, 400

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places (Public endpoint)"""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            }
            for place in places
        ], 200
```

#### Update Place (Owner Only)

```python
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details (Public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ],
            'reviews': [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id
                }
                for review in place.reviews
            ]
        }, 200

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the place owner')
    @jwt_required()
    def put(self, place_id):
        """
        Update place information (Owner only).

        Authorization:
        - Must be authenticated
        - Must be the place owner
        """
        # Get authenticated user's ID
        current_user_id = get_jwt_identity()

        # Get the place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check ownership
        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized'}, 403

        # Update place
        place_data = api.payload
        facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200
```

### 2. Review Endpoints

**File**: `app/api/v1/reviews.py`

```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or business rule violation')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """
        Create a new review (Authenticated users only).

        Business Rules:
        - Users cannot review their own places
        - Users can only submit one review per place
        - user_id is automatically set to authenticated user
        """
        # Get authenticated user's ID
        current_user = get_jwt_identity()

        # Get review data
        review_data = api.payload
        review_data['user_id'] = current_user

        # Get the place
        place_id = review_data.get('place_id')
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Business Rule 1: Cannot review own place
        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place'}, 400

        # Business Rule 2: Cannot review same place twice
        existing_reviews = facade.get_reviews_by_place(place_id)
        for review in existing_reviews:
            if review.user.id == current_user:
                return {
                    'error': 'You have already reviewed this place'
                }, 400

        # Create review
        new_review = facade.create_review(review_data)
        if not new_review:
            return {'error': 'User or Place not found'}, 400

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user.id,
            'place_id': new_review.place.id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews (Public endpoint)"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ], 200
```

#### Update and Delete Review (Creator Only)

```python
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details (Public endpoint)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the review creator')
    @jwt_required()
    def put(self, review_id):
        """
        Update review information (Creator only).

        Authorization:
        - Must be authenticated
        - Must be the review creator
        """
        current_user = get_jwt_identity()

        # Get the review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership
        if review.user.id != current_user:
            return {'error': 'Unauthorized'}, 403

        # Update review
        review_data = api.payload
        facade.update_review(review_id, review_data)
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the review creator')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review (Creator only).

        Authorization:
        - Must be authenticated
        - Must be the review creator
        """
        current_user = get_jwt_identity()

        # Get the review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership
        if review.user.id != current_user:
            return {'error': 'Unauthorized'}, 403

        # Delete review
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200
```

### 3. User Endpoints

**File**: `app/api/v1/users.py`

```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})


@api.route('/<user_id>')
class UserResource(Resource):
    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input - Cannot modify email or password')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Can only modify own user data')
    @jwt_required()
    def put(self, user_id):
        """
        Update user details (Self only, limited fields).

        Authorization:
        - Must be authenticated
        - Must be updating own user data
        - Cannot modify email or password

        Allowed fields:
        - first_name
        - last_name
        """
        # Get authenticated user's ID
        current_user = get_jwt_identity()

        # Check if user is updating their own data
        if current_user != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Get the user
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Get update data
        user_data = api.payload

        # Business Rule: Cannot modify email or password
        if 'email' in user_data or 'password' in user_data:
            return {
                'error': 'You cannot modify email or password'
            }, 400

        # Update user
        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
```

---

## Protected Endpoints

### Summary Table

| Endpoint | Method | Authentication | Authorization | Public |
|----------|--------|---------------|---------------|--------|
| `/places/` | GET | ❌ No | ❌ No | ✅ Yes |
| `/places/` | POST | ✅ Yes | Any auth user | ❌ No |
| `/places/<id>` | GET | ❌ No | ❌ No | ✅ Yes |
| `/places/<id>` | PUT | ✅ Yes | Owner only | ❌ No |
| `/reviews/` | GET | ❌ No | ❌ No | ✅ Yes |
| `/reviews/` | POST | ✅ Yes | Auth + rules | ❌ No |
| `/reviews/<id>` | GET | ❌ No | ❌ No | ✅ Yes |
| `/reviews/<id>` | PUT | ✅ Yes | Creator only | ❌ No |
| `/reviews/<id>` | DELETE | ✅ Yes | Creator only | ❌ No |
| `/users/<id>` | PUT | ✅ Yes | Self only | ❌ No |

### Authorization Flow

```
┌──────────────────────────────────────────────────────────┐
│              Request to Protected Endpoint                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  @jwt_required()     │
          │  Authentication      │
          └──────────┬───────────┘
                     │
          ┌──────────▼───────────┐
          │   Valid JWT Token?   │
          └──┬────────────────┬──┘
             │                │
          No │                │ Yes
             │                │
             ▼                ▼
    ┌──────────────┐   ┌──────────────────────┐
    │ Return 401   │   │ get_jwt_identity()   │
    │ Unauthorized │   │ Extract user ID      │
    └──────────────┘   └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │  Authorization Check │
                       │  (Ownership/Role)    │
                       └──┬────────────────┬──┘
                          │                │
                     Pass │                │ Fail
                          │                │
                          ▼                ▼
                  ┌──────────────┐  ┌──────────────┐
                  │ Process      │  │ Return 403   │
                  │ Request      │  │ Forbidden    │
                  │ Return 200   │  └──────────────┘
                  └──────────────┘
```

---

## Testing

### Test Scenarios

#### 1. Create Place (Authenticated)

```bash
# Login to get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' \
  | jq -r '.access_token')

# Create place
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Beautiful Apartment",
    "description": "Cozy apartment in city center",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "amenities": []
  }'
```

**Expected**: 201 Created, place with owner_id set to authenticated user

#### 2. Create Place (Unauthenticated - Should Fail)

```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Apartment",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

**Expected**: 401 Unauthorized

#### 3. Update Own Place (Should Succeed)

```bash
# Assuming $TOKEN is from place owner
curl -X PUT http://localhost:5000/api/v1/places/<place-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Beautiful Apartment",
    "price": 120.0
  }'
```

**Expected**: 200 OK

#### 4. Update Someone Else's Place (Should Fail)

```bash
# Login as different user
TOKEN2=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"other@example.com","password":"password123"}' \
  | jq -r '.access_token')

# Try to update place owned by first user
curl -X PUT http://localhost:5000/api/v1/places/<place-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{"title": "Hacked!"}'
```

**Expected**: 403 Forbidden

#### 5. Create Review for Own Place (Should Fail)

```bash
# Get place_id where owner is authenticated user
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "<own-place-id>"
  }'
```

**Expected**: 400 Bad Request - "You cannot review your own place"

#### 6. Create Duplicate Review (Should Fail)

```bash
# First review (should succeed)
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Nice place!",
    "rating": 4,
    "place_id": "<other-place-id>"
  }'

# Second review for same place (should fail)
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Still nice!",
    "rating": 5,
    "place_id": "<other-place-id>"
  }'
```

**Expected**: First succeeds (201), second fails (400) - "You have already reviewed this place"

#### 7. Update User (Email/Password - Should Fail)

```bash
curl -X PUT http://localhost:5000/api/v1/users/<user-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "newemail@example.com",
    "password": "newpassword"
  }'
```

**Expected**: 400 Bad Request - "You cannot modify email or password"

#### 8. Update User (Allowed Fields - Should Succeed)

```bash
curl -X PUT http://localhost:5000/api/v1/users/<user-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "NewFirstName",
    "last_name": "NewLastName"
  }'
```

**Expected**: 200 OK

---

## Security Patterns

### 1. Consistent Authorization Pattern

**Template**:
```python
@jwt_required()
def protected_endpoint(resource_id):
    # 1. Get authenticated user
    current_user_id = get_jwt_identity()

    # 2. Fetch resource
    resource = facade.get_resource(resource_id)
    if not resource:
        return {'error': 'Resource not found'}, 404

    # 3. Check ownership
    if resource.owner_id != current_user_id:
        return {'error': 'Unauthorized'}, 403

    # 4. Process request
    # ...
```

### 2. Automatic Owner Assignment

**Always set owner from JWT token**:
```python
@jwt_required()
def create_resource():
    current_user = get_jwt_identity()
    data = api.payload

    # Set owner automatically (don't trust client input)
    data['owner_id'] = current_user

    resource = facade.create_resource(data)
    # ...
```

### 3. Business Rule Validation

**Validate before persistence**:
```python
@jwt_required()
def create_review():
    current_user = get_jwt_identity()
    review_data = api.payload

    place = facade.get_place(review_data['place_id'])

    # Rule 1: Cannot review own place
    if place.owner_id == current_user:
        return {'error': 'Cannot review own place'}, 400

    # Rule 2: Cannot review twice
    existing = facade.get_user_review_for_place(
        current_user,
        place.id
    )
    if existing:
        return {'error': 'Already reviewed'}, 400

    # Proceed with creation
    # ...
```

---

## Troubleshooting

### Issue: "Unauthorized action" even with valid token

**Symptoms**: 403 error when updating own resource

**Solutions**:
1. Verify user_id matches:
   ```python
   print(f"Current user: {current_user_id}")
   print(f"Resource owner: {resource.owner_id}")
   ```
2. Check ID types match (str vs UUID)
3. Ensure token contains correct user ID

### Issue: Business rules not enforced

**Problem**: Users can review own places or review twice

**Solution**: Verify business logic runs before creation:
```python
# Add debug logging
print(f"Place owner: {place.owner.id}")
print(f"Current user: {current_user}")
print(f"Are equal: {place.owner.id == current_user}")
```

### Issue: Public endpoints requiring authentication

**Problem**: GET endpoints returning 401

**Solution**: Remove `@jwt_required()` decorator from public endpoints:
```python
# Public endpoint - no decorator
def get(self):
    """Public endpoint"""
    # ...

# Protected endpoint - has decorator
@jwt_required()
def post(self):
    """Protected endpoint"""
    # ...
```

---

## Conclusion

Task 3 implements comprehensive authentication and authorization for the HBnB application.

**Key Achievements**:
- ✅ JWT-based authentication on all protected endpoints
- ✅ Ownership validation for places and reviews
- ✅ Business rule enforcement (no self-reviews, no duplicates)
- ✅ Self-only user updates with field restrictions
- ✅ Public endpoints remain accessible
- ✅ Consistent authorization patterns
- ✅ Clear error messages and HTTP status codes

**Security Benefits**:
- **Protected Resources**: Only owners can modify resources
- **Business Logic**: Rules enforced at API level
- **Clear Boundaries**: Public vs protected endpoints well-defined
- **Audit Trail**: Owner IDs tracked automatically
- **Defense in Depth**: Multiple validation layers

This implementation ensures secure, user-specific access control throughout the HBnB application.

---

**Previous**: [Task 2: JWT Authentication](TASK_02.md)
**Next**: [Task 4: Administrator Access Control](TASK_04.md)
