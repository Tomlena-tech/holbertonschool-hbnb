# Task 1: Password Hashing with Bcrypt

## Overview

This document describes the implementation of secure password hashing in the User model using Flask-Bcrypt for the HBnB application.

**Task Objective**: Implement secure password storage by hashing passwords with bcrypt before persisting them to the database, and ensure passwords are never exposed in API responses.

**Completion Date**: November 2025
**Status**: ✅ Completed

---

## Table of Contents

1. [Requirements](#requirements)
2. [Security Context](#security-context)
3. [Implementation Details](#implementation-details)
4. [API Modifications](#api-modifications)
5. [Testing](#testing)
6. [Security Best Practices](#security-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

### Functional Requirements

1. **Password Hashing**:
   - Hash passwords using bcrypt before storage
   - Never store plain-text passwords
   - Implement password verification method

2. **API Security**:
   - Accept password on user creation (POST)
   - Never return passwords in responses (GET)
   - Hash passwords automatically before persistence

3. **Flask-Bcrypt Integration**:
   - Install and configure Flask-Bcrypt extension
   - Initialize bcrypt in application factory
   - Make bcrypt accessible to User model

### Non-Functional Requirements

- Strong cryptographic hashing algorithm (bcrypt)
- Automatic password hashing (no manual intervention)
- Protection against rainbow table attacks
- Secure password verification

---

## Security Context

### Why Password Hashing?

**The Problem**:
```
❌ INSECURE: Storing passwords in plain text
┌────────────────────────────────┐
│  Database                      │
├────────────────────────────────┤
│  user@example.com | password123│
│  admin@hbnb.io    | admin1234  │
└────────────────────────────────┘
```

If the database is compromised, all passwords are exposed immediately.

**The Solution**:
```
✅ SECURE: Storing password hashes
┌────────────────────────────────────────────────────────────┐
│  Database                                                   │
├────────────────────────────────────────────────────────────┤
│  user@example.com | $2b$12$KIXqQJ9Hc8vK... (hash)         │
│  admin@hbnb.io    | $2b$12$8mBnH2fQd7pL... (hash)         │
└────────────────────────────────────────────────────────────┘
```

Even if compromised, attackers cannot reverse-engineer the original passwords.

### Why Bcrypt?

**Bcrypt Advantages**:
1. **Adaptive**: Configurable work factor (computational cost)
2. **Salted**: Each password gets unique salt (prevents rainbow tables)
3. **Slow**: Intentionally slow to prevent brute-force attacks
4. **Industry Standard**: Proven, battle-tested algorithm

**Bcrypt vs Other Algorithms**:

| Algorithm | Security | Speed | Adaptive | Recommended |
|-----------|----------|-------|----------|-------------|
| MD5 | ❌ Broken | Very Fast | No | ❌ Never |
| SHA-1 | ❌ Broken | Fast | No | ❌ Never |
| SHA-256 | ⚠️ Ok | Fast | No | ⚠️ Not ideal |
| Bcrypt | ✅ Strong | Slow | Yes | ✅ Yes |
| Argon2 | ✅ Stronger | Configurable | Yes | ✅ Yes |

---

## Implementation Details

### 1. Installation

**File**: `requirements.txt`

```txt
flask
flask-restx
flask-bcrypt
flask-jwt-extended
```

**Install Dependencies**:
```bash
pip install flask-bcrypt
# or
pip install -r requirements.txt
```

### 2. Flask-Bcrypt Configuration

**File**: `app/__init__.py`

```python
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Instantiate Bcrypt extension
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Application Factory with Bcrypt initialization."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Initialize Bcrypt with the Flask app
    bcrypt.init_app(app)
    # Store in extensions dict for easy access
    app.extensions['bcrypt'] = bcrypt

    # Initialize JWT
    jwt.init_app(app)
    app.extensions['jwt'] = jwt

    # ... register namespaces ...

    return app
```

**Key Points**:
- **Global Instance**: `bcrypt = Bcrypt()` creates extension instance
- **Initialization**: `bcrypt.init_app(app)` binds to Flask app
- **Extension Registry**: Stored in `app.extensions['bcrypt']` for access

### 3. User Model Implementation

**File**: `app/models/user.py`

```python
from .base_model import BaseModel
from flask import current_app
import re


class User(BaseModel):
    """
    User model with secure password hashing.

    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): Unique email address
        password (str): Bcrypt-hashed password (never plain text)
        is_admin (bool): Administrator flag
        places (list): User's associated places
        reviews (list): User's reviews
    """

    emails = set()

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a User instance.

        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): Unique email address
            password (str): Plain text password (will be hashed)
            is_admin (bool): Admin privileges flag

        Note:
            Password is automatically hashed during initialization.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)  # Hash password immediately
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def hash_password(self, password):
        """
        Hash the password using bcrypt before storing.

        Args:
            password (str): Plain text password

        Sets:
            self.password (str): Bcrypt-hashed password string

        Security:
            - Uses bcrypt with automatic salt generation
            - Work factor determined by bcrypt defaults (12 rounds)
            - Resulting hash includes algorithm, cost, salt, and hash
        """
        # Access bcrypt from current Flask app context
        bcrypt = current_app.extensions['bcrypt']

        # Generate hash and decode to UTF-8 string for storage
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify if provided password matches stored hash.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise

        Security:
            - Timing-safe comparison (prevents timing attacks)
            - No exceptions thrown on mismatch
            - Uses bcrypt's built-in comparison
        """
        bcrypt = current_app.extensions['bcrypt']

        # Check password against stored hash
        return bcrypt.check_password_hash(self.password, password)

    # ... other properties and methods ...

    def to_dict(self):
        """
        Convert User to dictionary representation.

        Returns:
            dict: User data WITHOUT password field

        Security:
            Password is explicitly excluded from output
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            # ❌ password field intentionally omitted
        }
```

**Key Implementation Details**:

1. **Accessing Bcrypt**:
   ```python
   bcrypt = current_app.extensions['bcrypt']
   ```
   - Uses Flask's `current_app` to access application context
   - Retrieves bcrypt from extensions registry
   - Solves circular import issues

2. **Hashing Process**:
   ```python
   self.password = bcrypt.generate_password_hash(password).decode('utf-8')
   ```
   - `generate_password_hash()` creates bcrypt hash
   - Returns bytes object
   - `.decode('utf-8')` converts to string for storage

3. **Verification Process**:
   ```python
   return bcrypt.check_password_hash(self.password, password)
   ```
   - Compares provided password against stored hash
   - Returns boolean (True/False)
   - Timing-safe comparison

### 4. Bcrypt Hash Structure

**Example Hash**:
```
$2b$12$KIXqQJ9Hc8vKJ9HqL9HqL.OeKqJ9HqL9HqL9HqL9HqL9HqL9HqL
│ │  │  │                                                     │
│ │  │  │                                                     └─ Hash (31 chars)
│ │  │  └─ Salt (22 chars)
│ │  └─ Cost factor (2^12 = 4096 rounds)
│ └─ Minor version
└─ Algorithm identifier ($2b = bcrypt)
```

**Components**:
- **Algorithm**: `$2b$` (bcrypt variant)
- **Cost Factor**: `12` (4096 iterations)
- **Salt**: Random 22-character salt
- **Hash**: 31-character hash output

---

## API Modifications

### 1. User Creation Endpoint

**File**: `app/api/v1/users.py`

**Before** (Insecure):
```python
def post(self):
    """Register a new user"""
    user_data = api.payload
    # Password stored in plain text ❌
    new_user = facade.create_user(user_data)
    return {
        'id': new_user.id,
        'email': new_user.email,
        'password': new_user.password  # ❌ Exposed!
    }, 201
```

**After** (Secure):
```python
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @jwt_required()
    def post(self):
        """Register a new user (Admin only)"""
        # Verify admin privileges
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user (password automatically hashed in User.__init__)
        new_user = facade.create_user(user_data)

        # Return WITHOUT password ✅
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
            # ✅ No password field
        }, 201
```

### 2. User Retrieval Endpoint

**File**: `app/api/v1/users.py`

```python
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Use to_dict() which excludes password ✅
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            # ✅ No password field
        }, 200
```

### 3. Authentication Endpoint

**File**: `app/api/v1/auth.py`

```python
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = api.payload

        # Retrieve user by email
        user = facade.get_user_by_email(credentials['email'])

        # Verify password using bcrypt ✅
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Create JWT token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        return {'access_token': access_token}, 200
```

---

## Testing

### Manual Testing with cURL

#### 1. Create User with Password

```bash
# Get admin token first
ADMIN_TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' \
  | jq -r '.access_token')

# Create new user
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "MySecurePass123!"
  }'
```

**Expected Response**:
```json
{
  "id": "uuid-here",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

**✅ Password NOT in response**

#### 2. Verify Password is Hashed

```python
# Check in Python shell
from app import create_app
from app.services import facade

app = create_app()
with app.app_context():
    user = facade.get_user_by_email('john@example.com')
    print(f"Stored password: {user.password}")
    # Output: $2b$12$KIXqQJ9Hc8vK...
    print(f"Is hash: {user.password.startswith('$2b$')}")
    # Output: True
```

#### 3. Test Password Verification

```bash
# Correct password - should succeed
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"MySecurePass123!"}'

# Response: {"access_token": "..."}

# Incorrect password - should fail
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"WrongPassword"}'

# Response: {"error": "Invalid credentials"}
```

#### 4. Test GET Endpoint

```bash
# Get user details
curl -X GET http://localhost:5000/api/v1/users/<user-id> \
  -H "Content-Type: application/json"
```

**Expected Response**:
```json
{
  "id": "uuid-here",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

**✅ Password NOT in response**

### Automated Testing

```python
import unittest
from app import create_app
from app.services import facade


class TestPasswordHashing(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_password_is_hashed(self):
        """Test that passwords are hashed, not stored in plain text"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'PlainTextPassword123'
        }

        user = facade.create_user(user_data)

        # Password should be hashed (starts with $2b$)
        self.assertTrue(user.password.startswith('$2b$'))
        # Password should NOT be the plain text
        self.assertNotEqual(user.password, 'PlainTextPassword123')

    def test_password_verification_success(self):
        """Test successful password verification"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test2@example.com',
            'password': 'CorrectPassword'
        }

        user = facade.create_user(user_data)

        # Correct password should verify
        self.assertTrue(user.verify_password('CorrectPassword'))

    def test_password_verification_failure(self):
        """Test failed password verification with wrong password"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test3@example.com',
            'password': 'CorrectPassword'
        }

        user = facade.create_user(user_data)

        # Incorrect password should not verify
        self.assertFalse(user.verify_password('WrongPassword'))

    def test_password_not_in_api_response(self):
        """Test that password is not exposed in API responses"""
        # Create admin user and get token
        response = self.client.post('/api/v1/auth/login',
            json={'email': 'admin@hbnb.io', 'password': 'admin1234'})
        token = response.get_json()['access_token']

        # Create user via API
        response = self.client.post('/api/v1/users/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'first_name': 'API',
                'last_name': 'User',
                'email': 'api@example.com',
                'password': 'TestPassword123'
            })

        data = response.get_json()

        # Password should NOT be in response
        self.assertNotIn('password', data)
        # Should have other fields
        self.assertIn('email', data)
        self.assertEqual(data['email'], 'api@example.com')


if __name__ == '__main__':
    unittest.main()
```

---

## Security Best Practices

### 1. Password Storage

✅ **DO**:
- Hash passwords immediately upon receipt
- Use bcrypt with adequate work factor (12+ rounds)
- Never log passwords (even during debugging)
- Store hashes as strings in database

❌ **DON'T**:
- Store plain-text passwords
- Use reversible encryption
- Use fast hashing algorithms (MD5, SHA-1)
- Transmit passwords in URL parameters

### 2. Password Transmission

✅ **DO**:
- Use HTTPS for all password transmission
- Send passwords in request body (POST)
- Use secure headers (Content-Type: application/json)

❌ **DON'T**:
- Send passwords in query strings
- Log request bodies containing passwords
- Echo passwords back to clients

### 3. API Response Security

✅ **DO**:
- Use `to_dict()` method that excludes password
- Explicitly define response fields
- Validate all output data

❌ **DON'T**:
- Serialize entire model without filtering
- Include password in any API response
- Return hash to non-admin users

### 4. Password Policy

**Recommended Requirements**:
```python
def validate_password_strength(password):
    """Validate password meets security requirements."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"

    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"

    return True, "Password is valid"
```

---

## Troubleshooting

### Issue 1: Circular Import Error

**Symptoms**:
```
ImportError: cannot import name 'bcrypt' from partially initialized module 'app'
```

**Solution**:
Use `current_app` to access bcrypt:
```python
from flask import current_app

def hash_password(self, password):
    bcrypt = current_app.extensions['bcrypt']
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')
```

### Issue 2: "Working outside application context"

**Symptoms**:
```
RuntimeError: Working outside of application context
```

**Solution**:
Ensure operations are within app context:
```python
from app import create_app

app = create_app()
with app.app_context():
    # Operations here
    user = facade.create_user(user_data)
```

### Issue 3: Password Verification Always Fails

**Symptoms**:
All login attempts fail even with correct passwords

**Solutions**:
1. Verify password was hashed during creation:
   ```python
   print(user.password.startswith('$2b$'))  # Should be True
   ```
2. Check character encoding (should be UTF-8):
   ```python
   self.password = bcrypt.generate_password_hash(password).decode('utf-8')
   ```
3. Ensure same bcrypt instance is used for both operations

### Issue 4: Password Appears in Logs

**Problem**:
```python
# Bad logging
logger.info(f"Creating user with data: {user_data}")
# Logs: Creating user with data: {'email': '...', 'password': 'secret123'}
```

**Solution**:
```python
# Good logging
safe_data = {k: v for k, v in user_data.items() if k != 'password'}
logger.info(f"Creating user with data: {safe_data}")
# Logs: Creating user with data: {'email': '...', 'first_name': '...'}
```

---

## Conclusion

Password hashing with bcrypt provides robust security for user credentials in the HBnB application.

**Key Achievements**:
- ✅ Bcrypt integration with Flask
- ✅ Automatic password hashing on user creation
- ✅ Secure password verification
- ✅ Password exclusion from API responses
- ✅ Protection against common attacks
- ✅ Industry-standard cryptography

**Security Benefits**:
- **Rainbow Table Protection**: Unique salt per password
- **Brute-Force Resistance**: Slow hashing (configurable work factor)
- **Future-Proof**: Adaptive cost factor can be increased
- **Battle-Tested**: Industry-standard algorithm

This implementation ensures that even in the event of a database breach, user passwords remain protected.

---

**Previous**: [Task 0: Application Configuration](TASK_00.md)
**Next**: [Task 2: JWT Authentication](TASK_02.md)
