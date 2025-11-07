# Task 4: Administrator Access Control

## Overview

This document describes the implementation of role-based access control (RBAC) for the HBnB application, specifically focusing on administrator privileges and access restrictions.

**Task Objective**: Implement administrator-only endpoints and allow administrators to bypass ownership restrictions for managing users, amenities, places, and reviews.

**Completion Date**: November 7, 2025
**Status**: ✅ Completed and Tested

---

## Table of Contents

1. [Requirements](#requirements)
2. [Architecture](#architecture)
3. [Implementation Details](#implementation-details)
4. [API Endpoints](#api-endpoints)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

---

## Requirements

### Functional Requirements

1. **Admin-Only Endpoints**:
   - `POST /api/v1/users/` - Only administrators can create new users
   - `POST /api/v1/amenities/` - Only administrators can create amenities
   - `PUT /api/v1/amenities/<amenity_id>` - Only administrators can modify amenities

2. **Admin Privilege Extensions**:
   - `PUT /api/v1/users/<user_id>` - Administrators can modify any user's email and password
   - `PUT /api/v1/places/<place_id>` - Administrators can modify any place regardless of ownership
   - `PUT /api/v1/reviews/<review_id>` - Administrators can modify any review regardless of ownership
   - `DELETE /api/v1/reviews/<review_id>` - Administrators can delete any review regardless of ownership

3. **Admin User Management**:
   - Automatic creation of initial administrator account on application startup
   - Configurable admin credentials via environment variables
   - Idempotent seeding (safe to run multiple times)

### Non-Functional Requirements

- Maintain backward compatibility with existing non-admin user permissions
- Secure handling of admin credentials
- Clear error messages for unauthorized access (HTTP 403)
- Email uniqueness validation for admin user modifications

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Startup                      │
├─────────────────────────────────────────────────────────────┤
│  1. Initialize Flask App                                     │
│  2. Initialize Extensions (Bcrypt, JWT)                      │
│  3. Seed Admin User (if not exists)  ← NEW                  │
│  4. Register API Namespaces                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Request Flow                             │
├─────────────────────────────────────────────────────────────┤
│  Client → Endpoint                                           │
│     ↓                                                        │
│  JWT Validation (@jwt_required)                              │
│     ↓                                                        │
│  Extract JWT Claims (get_jwt())                              │
│     ↓                                                        │
│  Check is_admin flag                                         │
│     ↓                                                        │
│  ┌─────────────┬──────────────┐                            │
│  │  is_admin   │  !is_admin   │                            │
│  │  = True     │  = False     │                            │
│  └──────┬──────┴──────┬───────┘                            │
│         ↓             ↓                                      │
│   Allow Access    Check Ownership                           │
│                        ↓                                     │
│                  ┌─────┴─────┐                              │
│                  │  Authorized│                              │
│                  │  or 403   │                              │
│                  └───────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### JWT Token Structure

Admin JWT tokens include an additional claim:

```json
{
  "sub": "user_id",
  "is_admin": true,
  "exp": 1234567890,
  "iat": 1234567890,
  "type": "access"
}
```

---

## Implementation Details

### 1. Configuration Management

**File**: `config.py`

Added admin user configuration with environment variable support:

```python
class Config:
    # Admin user configuration
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@hbnb.io')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')
    ADMIN_FIRST_NAME = os.getenv('ADMIN_FIRST_NAME', 'Admin')
    ADMIN_LAST_NAME = os.getenv('ADMIN_LAST_NAME', 'HBnB')
```

**Environment Variables**:
- `ADMIN_EMAIL` - Admin user email address
- `ADMIN_PASSWORD` - Admin user password
- `ADMIN_FIRST_NAME` - Admin user first name
- `ADMIN_LAST_NAME` - Admin user last name

### 2. Admin User Seeding

**File**: `app/__init__.py`

Implemented automatic admin user creation on application startup:

```python
def seed_admin_user(app):
    """
    Seeds an initial admin user if no admin exists in the system.

    This function:
    - Checks if any admin user already exists
    - Creates one using credentials from app configuration if not found
    - Prevents duplicate admin user creation
    - Prints confirmation message
    """
    from app.services import facade

    all_users = facade.get_all_users()
    admin_exists = any(user.is_admin for user in all_users)

    if not admin_exists:
        admin_data = {
            'first_name': app.config['ADMIN_FIRST_NAME'],
            'last_name': app.config['ADMIN_LAST_NAME'],
            'email': app.config['ADMIN_EMAIL'],
            'password': app.config['ADMIN_PASSWORD'],
            'is_admin': True
        }

        existing_user = facade.get_user_by_email(admin_data['email'])
        if existing_user:
            print(f"User with email {admin_data['email']} already exists")
        else:
            facade.create_user(admin_data)
            print(f"Admin user created: {admin_data['email']}")
```

**Integration in `create_app()`**:

```python
# Seed the initial admin user
with app.app_context():
    seed_admin_user(app)
```

### 3. Admin Access Control Pattern

**Standard Pattern Used Across All Endpoints**:

```python
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

@jwt_required()
def protected_endpoint():
    # Get JWT claims
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    # Admin check
    if not is_admin:
        return {'error': 'Admin privileges required'}, 403

    # Process request...
```

**Ownership Bypass Pattern**:

```python
@jwt_required()
def ownership_protected_endpoint(resource_id):
    current_user_id = get_jwt_identity()
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    resource = facade.get_resource(resource_id)

    # Check ownership: allow if admin or owner
    if not is_admin and resource.owner_id != current_user_id:
        return {'error': 'Unauthorized'}, 403

    # Process request...
```

### 4. Endpoint Modifications

#### A. User Management (`app/api/v1/users.py`)

**POST /api/v1/users/**: Restricted to admins only

```python
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user (Admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Process user creation...
```

**PUT /api/v1/users/<user_id>**: Enhanced admin capabilities

```python
@jwt_required()
def put(self, user_id):
    """Update user details by ID"""
    current_user_id = get_jwt_identity()
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    # Authorization: user themselves or admin
    if current_user_id != user_id and not is_admin:
        return {'error': 'Unauthorized action'}, 403

    # Non-admin users cannot modify email or password
    if not is_admin:
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400
    else:
        # Admin can modify email with uniqueness check
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
```

#### B. Amenity Management (`app/api/v1/amenities.py`)

**POST /api/v1/amenities/**: Admin only

```python
@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    def post(self):
        """Register a new amenity (Admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
```

**PUT /api/v1/amenities/<amenity_id>**: Admin only

```python
@jwt_required()
def put(self, amenity_id):
    """Update an amenity's information (Admin only)"""
    current_user = get_jwt()
    if not current_user.get('is_admin'):
        return {'error': 'Admin privileges required'}, 403
```

#### C. Place Management (`app/api/v1/places.py`)

**PUT /api/v1/places/<place_id>**: Admin bypass for ownership

```python
@jwt_required()
def put(self, place_id):
    """Update a place's information"""
    current_user_id = get_jwt_identity()
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    place = facade.get_place(place_id)

    # Check ownership: allow if admin or owner
    if not is_admin and place.owner.id != current_user_id:
        return {'error': 'Unauthorized'}, 403
```

#### D. Review Management (`app/api/v1/reviews.py`)

**PUT /api/v1/reviews/<review_id>**: Admin bypass for ownership

```python
@jwt_required()
def put(self, review_id):
    """Update a review's information"""
    current_user_id = get_jwt_identity()
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    review = facade.get_review(review_id)

    # Check ownership: allow if admin or owner
    if not is_admin and review.user.id != current_user_id:
        return {'error': 'Unauthorized'}, 403
```

**DELETE /api/v1/reviews/<review_id>**: Admin bypass for ownership

```python
@jwt_required()
def delete(self, review_id):
    """Delete a review"""
    current_user_id = get_jwt_identity()
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    review = facade.get_review(review_id)

    # Check ownership: allow if admin or owner
    if not is_admin and review.user.id != current_user_id:
        return {'error': 'Unauthorized'}, 403
```

---

## API Endpoints

### Admin Authentication

#### Login as Admin

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Admin-Only Endpoints

#### Create User (Admin Only)

```bash
POST /api/v1/users/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Success Response** (201):
```json
{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

**Error Response** (403 - Non-Admin):
```json
{
  "error": "Admin privileges required"
}
```

#### Create Amenity (Admin Only)

```bash
POST /api/v1/amenities/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "WiFi"
}
```

**Success Response** (201):
```json
{
  "id": "uuid",
  "name": "WiFi"
}
```

#### Update Amenity (Admin Only)

```bash
PUT /api/v1/amenities/<amenity_id>
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Free WiFi"
}
```

### Admin Privilege Extensions

#### Update Any User's Email (Admin Only)

```bash
PUT /api/v1/users/<user_id>
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "password": "newpassword123"
}
```

#### Update Any Place (Admin Bypass)

```bash
PUT /api/v1/places/<place_id>
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated Description"
}
```

#### Update Any Review (Admin Bypass)

```bash
PUT /api/v1/reviews/<review_id>
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "text": "Admin updated review",
  "rating": 5
}
```

#### Delete Any Review (Admin Bypass)

```bash
DELETE /api/v1/reviews/<review_id>
Authorization: Bearer <admin_token>
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Admin Configuration
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=SecurePassword123!
ADMIN_FIRST_NAME=System
ADMIN_LAST_NAME=Administrator

# JWT Configuration
SECRET_KEY=your-secret-key-here
```

### Production Configuration

For production environments:

1. **Never use default credentials**
2. **Use strong passwords** (minimum 12 characters, mixed case, numbers, special characters)
3. **Store credentials securely** (use secret management services like AWS Secrets Manager, HashiCorp Vault)
4. **Rotate admin passwords regularly**
5. **Enable audit logging** for admin actions

---

## Testing

### Manual Testing Results

All tests passed successfully:

| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| Admin user auto-creation | Admin created on startup | ✅ Admin user created: admin@hbnb.io | PASS |
| Admin login | JWT token with is_admin=true | ✅ Token received with is_admin claim | PASS |
| Admin creates user | 201 Created | ✅ User created successfully | PASS |
| Non-admin creates user | 403 Forbidden | ✅ "Admin privileges required" | PASS |
| Admin creates amenity | 201 Created | ✅ Amenity created successfully | PASS |
| Non-admin creates amenity | 403 Forbidden | ✅ "Admin privileges required" | PASS |
| Admin modifies user email | 200 OK | ✅ Email updated successfully | PASS |
| Admin updates any place | 200 OK | ✅ Place updated successfully | PASS |
| Admin updates any review | 200 OK | ✅ Review updated successfully | PASS |
| Admin deletes any review | 200 OK | ✅ Review deleted successfully | PASS |
| Non-admin retains permissions | Normal operation | ✅ All original permissions work | PASS |

### Test Scripts

#### 1. Test Admin Login

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin1234"}'
```

#### 2. Test Admin Create User

```bash
ADMIN_TOKEN="your_admin_token_here"

curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 3. Test Non-Admin Blocked

```bash
USER_TOKEN="non_admin_token_here"

curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{
    "first_name": "Another",
    "last_name": "User",
    "email": "another@example.com",
    "password": "password123"
  }'

# Expected: {"error": "Admin privileges required"}
```

---

## Security Considerations

### 1. Authentication & Authorization

- **JWT Token Security**: All admin actions require valid JWT tokens
- **Token Expiration**: Tokens expire after configured time (default: 15 minutes)
- **Claim Validation**: `is_admin` flag is validated on every request
- **No Token Tampering**: JWT signature prevents unauthorized modification

### 2. Password Security

- **Bcrypt Hashing**: All passwords hashed using Bcrypt before storage
- **No Plain Text**: Passwords never stored or logged in plain text
- **Strong Defaults**: Encourage strong password policies

### 3. Email Uniqueness

- **Validation**: Email uniqueness checked before creation/update
- **Case Sensitivity**: Email comparisons should be case-insensitive
- **Error Handling**: Clear error messages without leaking information

### 4. Audit Trail

**Recommendation**: Implement logging for all admin actions:

```python
import logging

logger = logging.getLogger(__name__)

@jwt_required()
def admin_action():
    current_user_jwt = get_jwt()
    is_admin = current_user_jwt.get('is_admin', False)

    if is_admin:
        logger.info(f"Admin action performed by user {get_jwt_identity()}")
```

### 5. Rate Limiting

**Recommendation**: Implement rate limiting for admin endpoints to prevent abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@limiter.limit("10 per minute")
@jwt_required()
def admin_endpoint():
    # Admin logic...
```

---

## Troubleshooting

### Issue: Admin User Not Created

**Symptoms**: No admin user exists after application startup

**Solutions**:
1. Check application logs for error messages
2. Verify database connection is working
3. Ensure `facade.create_user()` is functioning correctly
4. Check if user with admin email already exists (non-admin)

### Issue: "Admin privileges required" for Admin User

**Symptoms**: Admin user receives 403 errors on admin endpoints

**Solutions**:
1. Verify `is_admin` field in user model is set to `True`
2. Check JWT token includes `is_admin` claim:
   ```bash
   # Decode JWT token at https://jwt.io
   ```
3. Verify `additional_claims` in token creation (auth.py):
   ```python
   create_access_token(
       identity=str(user.id),
       additional_claims={"is_admin": user.is_admin}  # Check this
   )
   ```

### Issue: Email Already Exists Error

**Symptoms**: Cannot modify user email even as admin

**Solutions**:
1. Verify target email is not already in use
2. Check email uniqueness validation logic
3. Ensure existing_user.id != user_id comparison is correct

### Issue: Ownership Bypass Not Working

**Symptoms**: Admin cannot modify other users' resources

**Solutions**:
1. Verify `get_jwt()` import is present
2. Check `is_admin` flag extraction: `get_jwt().get('is_admin', False)`
3. Ensure ownership check uses OR logic: `if not is_admin and resource.owner_id != current_user_id`

---

## Future Enhancements

### 1. Role-Based Access Control (RBAC)

Extend beyond simple admin/non-admin to support multiple roles:

```python
ROLES = {
    'admin': ['create_user', 'delete_user', 'manage_amenities'],
    'moderator': ['delete_review', 'update_review'],
    'user': ['create_place', 'create_review']
}
```

### 2. Admin Activity Logging

Track all admin actions in dedicated audit table:

```python
class AdminAuditLog(BaseModel):
    admin_id = String
    action = String  # 'CREATE_USER', 'DELETE_REVIEW', etc.
    resource_type = String
    resource_id = String
    timestamp = DateTime
```

### 3. Multi-Factor Authentication (MFA)

Require MFA for admin accounts:

```python
@api.route('/admin/verify-mfa')
def verify_mfa():
    # Verify TOTP code
    # Issue admin token only after MFA verification
```

### 4. Granular Permissions

Allow configuration of specific admin permissions:

```python
class AdminPermission(BaseModel):
    admin_id = String
    permission = String  # 'users.create', 'places.delete', etc.
    granted_at = DateTime
```

---

## Conclusion

The administrator access control system provides a robust foundation for managing privileged operations in the HBnB application. The implementation follows security best practices and maintains backward compatibility while enabling powerful administrative capabilities.

**Key Achievements**:
- ✅ Automatic admin user seeding
- ✅ Secure JWT-based authorization
- ✅ Comprehensive admin privileges
- ✅ Ownership bypass for content moderation
- ✅ Backward compatible with existing functionality
- ✅ Fully tested and documented

For questions or issues, please refer to the troubleshooting section or contact the development team.
