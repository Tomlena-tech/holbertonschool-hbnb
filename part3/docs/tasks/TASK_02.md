# Task 2: JWT Authentication

## Overview

This document describes the implementation of JSON Web Token (JWT) based authentication for the HBnB application using Flask-JWT-Extended.

**Task Objective**: Implement secure token-based authentication system that allows users to login and access protected endpoints using JWT tokens.

**Completion Date**: November 2025
**Status**: ✅ Completed

---

## Table of Contents

1. [Requirements](#requirements)
2. [JWT Authentication Concepts](#jwt-authentication-concepts)
3. [Implementation Details](#implementation-details)
4. [API Endpoints](#api-endpoints)
5. [Testing](#testing)
6. [Security Considerations](#security-considerations)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

### Functional Requirements

1. **JWT Integration**:
   - Install and configure Flask-JWT-Extended
   - Initialize JWT manager in application factory
   - Configure JWT secret key

2. **Login Endpoint**:
   - Accept email and password credentials
   - Verify credentials against stored user data
   - Generate JWT token with user identity and claims
   - Return token to client

3. **Protected Endpoints**:
   - Implement `@jwt_required()` decorator
   - Extract user identity from JWT tokens
   - Enforce authentication on specific endpoints

### Non-Functional Requirements

- Stateless authentication (no server-side session storage)
- Token-based authorization
- Secure token generation and validation
- Configurable token expiration
- Support for additional claims (e.g., is_admin)

---

## JWT Authentication Concepts

### What is JWT?

**JSON Web Token (JWT)** is an open standard (RFC 7519) that defines a compact and self-contained way to securely transmit information between parties as a JSON object.

### JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│                                     │                                                                                │
│            HEADER                   │                         PAYLOAD                                                │            SIGNATURE
└─────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────┴───────────────────────
```

**Components**:

1. **Header** (Algorithm & Token Type):
   ```json
   {
     "alg": "HS256",
     "typ": "JWT"
   }
   ```

2. **Payload** (Claims):
   ```json
   {
     "sub": "user-id-123",
     "is_admin": true,
     "exp": 1762518947,
     "iat": 1762518047
   }
   ```

3. **Signature** (Verification):
   ```
   HMACSHA256(
     base64UrlEncode(header) + "." + base64UrlEncode(payload),
     secret_key
   )
   ```

### JWT Authentication Flow

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │ Server  │
└────┬────┘                                    └────┬────┘
     │                                              │
     │  1. POST /login (email + password)          │
     ├─────────────────────────────────────────────>│
     │                                              │
     │         2. Verify credentials                │
     │            (check password hash)             │
     │                                              │
     │         3. Generate JWT token                │
     │            (sign with secret key)            │
     │                                              │
     │  4. Return JWT token                         │
     │<─────────────────────────────────────────────┤
     │                                              │
     │  5. Store token (localStorage/memory)        │
     │                                              │
     │  6. Request protected resource               │
     │     (Authorization: Bearer TOKEN)            │
     ├─────────────────────────────────────────────>│
     │                                              │
     │         7. Validate token signature          │
     │            (verify with secret key)          │
     │                                              │
     │         8. Extract user identity             │
     │            from token payload                │
     │                                              │
     │  9. Return protected data                    │
     │<─────────────────────────────────────────────┤
     │                                              │
```

### Benefits of JWT

✅ **Stateless**: No server-side session storage required
✅ **Scalable**: Works across multiple servers/instances
✅ **Self-Contained**: All info is in the token itself
✅ **Secure**: Cryptographically signed
✅ **Portable**: Works across different domains
✅ **Performance**: No database lookup per request

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

**Install**:
```bash
pip install flask-jwt-extended
```

### 2. Flask-JWT-Extended Configuration

**File**: `app/__init__.py`

```python
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Instantiate extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """Application Factory with JWT initialization."""
    app = Flask(__name__)

    # Load configuration (includes SECRET_KEY for JWT)
    app.config.from_object(config_class)

    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Initialize extensions
    bcrypt.init_app(app)
    app.extensions['bcrypt'] = bcrypt

    # Initialize JWT Manager
    jwt.init_app(app)
    app.extensions['jwt'] = jwt

    # Register namespaces
    from app.api.v1.auth import api as auth_ns
    api.add_namespace(auth_ns, path='/api/v1/auth')
    # ... other namespaces ...

    return app
```

**Configuration Requirements**:

The JWT extension uses Flask's `SECRET_KEY` for token signing:

```python
# config.py
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    # JWT uses this automatically
```

**Optional JWT Configuration**:
```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # JWT-specific settings (optional)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
```

### 3. Authentication Namespace

**File**: `app/api/v1/auth.py`

```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app.services import facade

# Create namespace
api = Namespace('auth', description='Authentication operations')

# Define login model for input validation
login_model = api.model('Login', {
    'email': fields.String(
        required=True,
        description='User email address'
    ),
    'password': fields.String(
        required=True,
        description='User password'
    )
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return JWT token.

        Process:
        1. Validate request payload
        2. Retrieve user by email
        3. Verify password using bcrypt
        4. Generate JWT token with identity and claims
        5. Return token to client

        Returns:
            dict: {'access_token': 'JWT_TOKEN_STRING'}

        Errors:
            401: Invalid email or password
        """
        # Get credentials from request payload
        credentials = api.payload

        # Retrieve user by email
        user = facade.get_user_by_email(credentials['email'])

        # Verify user exists and password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Create JWT access token
        access_token = create_access_token(
            identity=str(user.id),  # User ID as token subject
            additional_claims={
                "is_admin": user.is_admin  # Custom claim for authorization
            }
        )

        # Return token
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """
        Protected endpoint requiring valid JWT token.

        Demonstrates:
        - @jwt_required() decorator for authentication
        - get_jwt_identity() to extract user ID
        - get_jwt() to access additional claims

        Returns:
            dict: Welcome message with user ID
        """
        # Get user ID from token
        current_user_id = get_jwt_identity()

        # Get additional claims (optional)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': is_admin
        }, 200
```

**Key Functions**:

1. **`create_access_token()`**:
   ```python
   token = create_access_token(
       identity=user_id,              # Required: user identifier
       additional_claims={...}        # Optional: custom data
   )
   ```

2. **`@jwt_required()`**: Decorator to protect endpoints
   ```python
   @jwt_required()  # Requires valid JWT token
   def protected_endpoint():
       # Only accessible with valid token
       pass
   ```

3. **`get_jwt_identity()`**: Extract token subject (user ID)
   ```python
   user_id = get_jwt_identity()  # Returns identity from token
   ```

4. **`get_jwt()`**: Access full token payload
   ```python
   claims = get_jwt()  # Returns all claims
   is_admin = claims.get('is_admin', False)
   ```

### 4. Protected Endpoint Pattern

**Example**: Protecting user modification endpoint

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route('/<user_id>')
class UserResource(Resource):
    @api.expect(user_model, validate=False)
    @jwt_required()  # ← Requires authentication
    def put(self, user_id):
        """Update user details (authenticated users only)"""

        # Get authenticated user's ID from token
        current_user_id = get_jwt_identity()

        # Verify user is modifying their own data
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Process update...
        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)
        return {'message': 'User updated successfully'}, 200
```

---

## API Endpoints

### Login Endpoint

**POST** `/api/v1/auth/login`

**Request**:
```http
POST /api/v1/auth/login HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjUxODA0NywianRpIjoiOGZhMmYxN2MtNTQ0Yy00OGQ0LWIxYTEtNTQ5NTZlYTAzMmYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjllMTllNzk0LWM4YjItNGE5OC04MzQ4LTY2MTY0Y2QzMGE3NiIsIm5iZiI6MTc2MjUxODA0NywiY3NyZiI6IjAzOWQ5NTllLWM1NTItNDcwZC1hMGVhLWFhMjgzZTZmYzZkNiIsImV4cCI6MTc2MjUxODk0NywiaXNfYWRtaW4iOnRydWV9.QMyUbKLCBqfTQHn2ZNYkW7xfCLR8N0w2Ba6g_nX8UWo"
}
```

**Error Response** (401):
```json
{
  "error": "Invalid credentials"
}
```

### Protected Endpoint Example

**GET** `/api/v1/auth/protected`

**Request**:
```http
GET /api/v1/auth/protected HTTP/1.1
Host: localhost:5000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response** (200):
```json
{
  "message": "Hello, user 9e19e794-c8b2-4a98-8348-66164cd30a76",
  "is_admin": true
}
```

**Error Response** (401 - Missing Token):
```json
{
  "msg": "Missing Authorization Header"
}
```

**Error Response** (422 - Invalid Token):
```json
{
  "msg": "Signature verification failed"
}
```

---

## Testing

### Manual Testing with cURL

#### 1. Test Login (Success)

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.io",
    "password": "admin1234"
  }'
```

**Expected Output**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 2. Test Login (Failure)

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.io",
    "password": "wrong_password"
  }'
```

**Expected Output**:
```json
{
  "error": "Invalid credentials"
}
```

#### 3. Test Protected Endpoint (With Token)

```bash
# Save token to variable
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' \
  | jq -r '.access_token')

# Access protected endpoint
curl -X GET http://localhost:5000/api/v1/auth/protected \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Output**:
```json
{
  "message": "Hello, user 9e19e794-c8b2-4a98-8348-66164cd30a76",
  "is_admin": true
}
```

#### 4. Test Protected Endpoint (Without Token)

```bash
curl -X GET http://localhost:5000/api/v1/auth/protected
```

**Expected Output**:
```json
{
  "msg": "Missing Authorization Header"
}
```

### Testing with Postman

**Step 1: Login**
1. Method: POST
2. URL: `http://localhost:5000/api/v1/auth/login`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "email": "admin@hbnb.io",
     "password": "admin1234"
   }
   ```
5. Send → Copy `access_token` from response

**Step 2: Access Protected Endpoint**
1. Method: GET
2. URL: `http://localhost:5000/api/v1/auth/protected`
3. Headers: `Authorization: Bearer YOUR_TOKEN_HERE`
4. Send → Should receive success response

### Automated Testing

```python
import unittest
from app import create_app
from app.services import facade


class TestJWTAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_success(self):
        """Test successful login returns JWT token"""
        response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'admin@hbnb.io',
                'password': 'admin1234'
            })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)
        # Token should be a non-empty string
        self.assertTrue(len(data['access_token']) > 0)

    def test_login_invalid_email(self):
        """Test login with non-existent email"""
        response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'anypassword'
            })

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_login_invalid_password(self):
        """Test login with incorrect password"""
        response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'admin@hbnb.io',
                'password': 'wrong_password'
            })

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token"""
        # First, login to get token
        login_response = self.client.post('/api/v1/auth/login',
            json={
                'email': 'admin@hbnb.io',
                'password': 'admin1234'
            })
        token = login_response.get_json()['access_token']

        # Access protected endpoint with token
        response = self.client.get('/api/v1/auth/protected',
            headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('is_admin', data)

    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = self.client.get('/api/v1/auth/protected')

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('msg', data)

    def test_protected_endpoint_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        response = self.client.get('/api/v1/auth/protected',
            headers={'Authorization': 'Bearer invalid_token_here'})

        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
```

---

## Security Considerations

### 1. Secret Key Security

**Critical**: The `SECRET_KEY` is used to sign JWT tokens. If compromised, attackers can forge tokens.

✅ **DO**:
```python
# Use strong, random secret keys
import secrets
SECRET_KEY = secrets.token_hex(32)  # 64 character hex string

# Use environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set!")

# Different keys per environment
# Development: 'dev-secret-123'
# Production: Strong random key from secrets manager
```

❌ **DON'T**:
```python
# Weak or default keys
SECRET_KEY = 'secret'
SECRET_KEY = 'default_secret_key'

# Committing secrets to version control
SECRET_KEY = 'my-hardcoded-secret'  # ← In git repo
```

### 2. Token Expiration

**Configure appropriate token lifetimes**:

```python
from datetime import timedelta

class Config:
    # Short-lived access tokens (15-60 minutes)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    # Long-lived refresh tokens (optional)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

**Benefits**:
- Limits damage if token is stolen
- Forces periodic re-authentication
- Enables token revocation strategies

### 3. HTTPS Only

✅ **Always use HTTPS in production**:
- JWT tokens are bearer tokens (anyone with token can use it)
- HTTP transmits tokens in clear text
- HTTPS encrypts all traffic including headers

```python
# Force HTTPS in production
if app.config['ENV'] == 'production':
    @app.before_request
    def force_https():
        if not request.is_secure:
            return redirect(request.url.replace('http://', 'https://'))
```

### 4. Token Storage (Client-Side)

**Client-side storage options**:

| Storage | Security | Persistence | XSS Vulnerable | CSRF Vulnerable |
|---------|----------|-------------|----------------|-----------------|
| localStorage | ⚠️ Low | Yes | ✅ Yes | ❌ No |
| sessionStorage | ⚠️ Low | Session only | ✅ Yes | ❌ No |
| Memory (JS variable) | ✅ High | No | ❌ No | ❌ No |
| httpOnly Cookie | ✅ High | Yes | ❌ No | ✅ Yes |

**Recommendation**:
- Use memory storage or httpOnly cookies
- Avoid localStorage for sensitive tokens

### 5. Token Validation

**Flask-JWT-Extended automatically validates**:
- ✅ Token signature (prevents tampering)
- ✅ Token expiration (prevents replay attacks)
- ✅ Token format (ensures valid JWT)
- ✅ Required claims (sub, exp, iat, etc.)

### 6. Additional Claims Security

**Be careful what you include in tokens**:

✅ **DO include**:
- User ID (subject)
- Role flags (is_admin, is_moderator)
- Non-sensitive metadata

❌ **DON'T include**:
- Passwords or password hashes
- Credit card numbers
- Social security numbers
- Personal health information

**Remember**: JWT tokens are encoded (Base64), not encrypted. Anyone can decode and read the payload.

---

## Troubleshooting

### Issue 1: "Missing Authorization Header"

**Symptoms**:
```json
{
  "msg": "Missing Authorization Header"
}
```

**Solutions**:
1. Verify header format is correct:
   ```
   Authorization: Bearer YOUR_TOKEN_HERE
   ```
2. Check header name is "Authorization" (case-sensitive)
3. Ensure token is included after "Bearer "

### Issue 2: "Signature verification failed"

**Symptoms**:
```json
{
  "msg": "Signature verification failed"
}
```

**Causes**:
- Token was tampered with
- Different `SECRET_KEY` used for signing vs verification
- Token from different environment/server

**Solutions**:
1. Verify `SECRET_KEY` is consistent:
   ```python
   print(app.config['SECRET_KEY'])
   ```
2. Generate new token with correct secret
3. Don't mix tokens between environments

### Issue 3: Token Expired

**Symptoms**:
```json
{
  "msg": "Token has expired"
}
```

**Solutions**:
1. Request new token via `/login`
2. Implement token refresh mechanism:
   ```python
   from flask_jwt_extended import create_refresh_token, jwt_required, get_jwt_identity

   @api.route('/refresh')
   class TokenRefresh(Resource):
       @jwt_required(refresh=True)
       def post(self):
           current_user = get_jwt_identity()
           new_token = create_access_token(identity=current_user)
           return {'access_token': new_token}
   ```
3. Increase token expiration time (not recommended for production)

### Issue 4: Claims Not Accessible

**Problem**:
```python
claims = get_jwt()
is_admin = claims.get('is_admin')  # Returns None
```

**Solution**:
Ensure claims were added during token creation:
```python
# When creating token
access_token = create_access_token(
    identity=str(user.id),
    additional_claims={"is_admin": user.is_admin}  # ← Add claims here
)
```

---

## Conclusion

JWT authentication provides a robust, stateless authentication mechanism for the HBnB application.

**Key Achievements**:
- ✅ Flask-JWT-Extended integration
- ✅ Secure login endpoint with credential verification
- ✅ JWT token generation with custom claims
- ✅ Protected endpoint pattern with `@jwt_required()`
- ✅ User identity extraction
- ✅ Admin flag support via claims

**Security Benefits**:
- **Stateless**: No server-side session storage
- **Scalable**: Works across multiple servers
- **Secure**: Cryptographically signed tokens
- **Flexible**: Custom claims for authorization
- **Standards-Based**: RFC 7519 compliant

This implementation enables secure, scalable authentication for all protected API endpoints in the HBnB application.

---

**Previous**: [Task 1: Password Hashing with Bcrypt](TASK_01.md)
**Next**: [Task 3: Authenticated User Access Endpoints](TASK_03.md)
