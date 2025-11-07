# HBnB Part 3 - Technical Documentation

This directory contains comprehensive technical documentation for Part 3 of the HBnB project, covering authentication, authorization, and security implementation.

## 📚 Documentation Structure

```
docs/
├── README.md                    # This file - Documentation overview
└── tasks/
    ├── TASK_00.md              # Application Configuration
    ├── TASK_01.md              # Password Hashing with Bcrypt
    ├── TASK_02.md              # JWT Authentication
    ├── TASK_03.md              # Authenticated User Access
    └── TASK_04.md              # Administrator Access Control
```

---

## 📖 Task Documentation

### [Task 0: Application Configuration](tasks/TASK_00.md)
**Objective**: Implement Flask Application Factory pattern with configuration management

**Topics Covered**:
- ✅ Application Factory pattern implementation
- ✅ Configuration class hierarchy
- ✅ Environment-specific settings (Dev, Test, Production)
- ✅ Environment variable integration
- ✅ Configuration best practices

**Key Features**:
- Multiple environment support
- Clean configuration separation
- Security-focused secret management

**Status**: ✅ Completed

---

### [Task 1: Password Hashing with Bcrypt](tasks/TASK_01.md)
**Objective**: Implement secure password storage using bcrypt hashing

**Topics Covered**:
- ✅ Flask-Bcrypt integration
- ✅ Password hashing implementation in User model
- ✅ Password verification logic
- ✅ API endpoint security (no password exposure)
- ✅ Cryptographic best practices

**Key Features**:
- Bcrypt password hashing
- Automatic hash generation
- Secure password verification
- Password exclusion from API responses

**Status**: ✅ Completed

---

### [Task 2: JWT Authentication](tasks/TASK_02.md)
**Objective**: Implement token-based authentication using JSON Web Tokens

**Topics Covered**:
- ✅ Flask-JWT-Extended integration
- ✅ Login endpoint with credential verification
- ✅ JWT token generation with custom claims
- ✅ Protected endpoint pattern with `@jwt_required()`
- ✅ Token validation and identity extraction

**Key Features**:
- Stateless authentication
- JWT token generation
- Custom claims support (is_admin flag)
- Protected endpoint decorators
- Token expiration handling

**Status**: ✅ Completed

---

### [Task 3: Authenticated User Access Endpoints](tasks/TASK_03.md)
**Objective**: Secure API endpoints with ownership-based authorization

**Topics Covered**:
- ✅ Authentication vs Authorization concepts
- ✅ Ownership-based access control
- ✅ Business rule enforcement
- ✅ Protected vs Public endpoints
- ✅ Resource ownership patterns

**Key Features**:
- Place creation/modification (owner only)
- Review creation/modification (creator only)
- User self-modification (limited fields)
- Business rules (no self-reviews, no duplicates)
- Public GET endpoints

**Status**: ✅ Completed

---

### [Task 4: Administrator Access Control](tasks/TASK_04.md)
**Objective**: Implement role-based access control for administrative operations

**Topics Covered**:
- ✅ Admin role implementation
- ✅ Admin-only endpoints
- ✅ Admin seeding strategy
- ✅ Ownership bypass for admins
- ✅ Email/password modification by admins

**Key Features**:
- Automatic admin user seeding
- Admin-restricted endpoints (user/amenity creation)
- Admin bypass for ownership restrictions
- Admin email/password modification
- Configurable admin credentials

**Status**: ✅ Completed

---

## 🎯 Quick Start Guide

### For New Developers

1. **Start with Task 0** to understand the application structure and configuration
2. **Move to Task 1** to learn about password security
3. **Continue to Task 2** for authentication basics
4. **Study Task 3** to understand authorization patterns
5. **Finish with Task 4** for admin access control

### For Security Auditors

- Review **Task 1** for password security implementation
- Check **Task 2** for JWT token handling
- Examine **Task 3** for authorization logic
- Analyze **Task 4** for admin access patterns

### For API Consumers

- See **Task 2** for authentication flow
- Check **Task 3** for endpoint requirements
- Review **Task 4** for admin-specific operations

---

## 🔑 Key Technologies

| Technology | Purpose | Documentation |
|------------|---------|---------------|
| **Flask** | Web framework | [Task 0](tasks/TASK_00.md) |
| **Flask-Bcrypt** | Password hashing | [Task 1](tasks/TASK_01.md) |
| **Flask-JWT-Extended** | JWT authentication | [Task 2](tasks/TASK_02.md) |
| **Flask-RESTX** | API framework | All tasks |

---

## 🔒 Security Features Implemented

### Authentication & Authorization
- ✅ Bcrypt password hashing (Task 1)
- ✅ JWT token-based authentication (Task 2)
- ✅ Ownership-based authorization (Task 3)
- ✅ Role-based access control (Task 4)

### Access Control
- ✅ Protected endpoints with `@jwt_required()`
- ✅ Owner validation on resource modifications
- ✅ Admin privilege checking
- ✅ Business rule enforcement

### Data Protection
- ✅ Passwords never exposed in responses
- ✅ Email/password modification restrictions
- ✅ Cryptographically signed JWT tokens
- ✅ Secure secret key management

---

## 📊 API Endpoint Overview

### Public Endpoints (No Auth Required)
```
GET  /api/v1/places/              # List all places
GET  /api/v1/places/<id>          # View place details
GET  /api/v1/reviews/             # List all reviews
GET  /api/v1/amenities/           # List all amenities
POST /api/v1/auth/login           # User login
```

### Authenticated Endpoints
```
POST /api/v1/places/              # Create place (authenticated users)
PUT  /api/v1/places/<id>          # Update place (owners only)
POST /api/v1/reviews/             # Create review (with business rules)
PUT  /api/v1/reviews/<id>         # Update review (creators only)
DELETE /api/v1/reviews/<id>       # Delete review (creators only)
PUT  /api/v1/users/<id>           # Update user (self only, limited)
```

### Admin-Only Endpoints
```
POST /api/v1/users/               # Create user (admin only)
PUT  /api/v1/users/<id>           # Modify any user (admin override)
POST /api/v1/amenities/           # Create amenity (admin only)
PUT  /api/v1/amenities/<id>       # Update amenity (admin only)
PUT  /api/v1/places/<id>          # Update any place (admin bypass)
PUT  /api/v1/reviews/<id>         # Update any review (admin bypass)
DELETE /api/v1/reviews/<id>       # Delete any review (admin bypass)
```

---

## 🧪 Testing

Each task documentation includes:

### Manual Testing
- ✅ cURL command examples
- ✅ Postman collection instructions
- ✅ Expected request/response formats
- ✅ Error scenario testing

### Automated Testing
- ✅ Unit test examples
- ✅ Integration test patterns
- ✅ Authentication test cases
- ✅ Authorization test scenarios

### Example Test Flow

```bash
# 1. Login as admin
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}' \
  | jq -r '.access_token')

# 2. Create a user (admin only)
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"pass123"}'

# 3. Create a place (authenticated user)
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Nice Place","price":100.0,"latitude":40.7128,"longitude":-74.0060}'
```

See individual task documentation for comprehensive testing guides.

---

## 🛠️ Configuration

### Environment Variables

```bash
# Security
SECRET_KEY=your-secret-key-here

# Admin Configuration
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=SecurePassword123!
ADMIN_FIRST_NAME=Admin
ADMIN_LAST_NAME=User

# JWT Configuration (optional)
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes in seconds
```

### Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="dev-secret-key"
export ADMIN_EMAIL="admin@dev.local"

# Run application
python run.py
```

See [Task 0](tasks/TASK_00.md) for detailed configuration guide.

---

## 🐛 Troubleshooting

Each task documentation includes a dedicated troubleshooting section:

- **Task 0**: Configuration and import issues
- **Task 1**: Circular imports, password hashing errors
- **Task 2**: JWT token validation, missing headers
- **Task 3**: Authorization failures, ownership checks
- **Task 4**: Admin seeding, privilege checking

### Common Issues

| Issue | Solution | Reference |
|-------|----------|-----------|
| "Missing Authorization Header" | Include `Authorization: Bearer TOKEN` header | [Task 2](tasks/TASK_02.md#troubleshooting) |
| "Unauthorized action" (403) | Verify ownership of resource | [Task 3](tasks/TASK_03.md#troubleshooting) |
| "Admin privileges required" | Login with admin account | [Task 4](tasks/TASK_04.md#troubleshooting) |
| Circular import error | Use `current_app` for extensions | [Task 1](tasks/TASK_01.md#troubleshooting) |

---

## 📈 Architecture Overview

### Authentication Flow
```
┌─────────┐         ┌─────────┐         ┌──────────┐
│ Client  │ Login   │  Flask  │ Verify  │ Database │
│         ├────────>│   App   ├────────>│          │
│         │         │         │         │          │
│         │<────────┤ JWT     │         │          │
│         │ Token   │ Token   │         │          │
└────┬────┘         └─────────┘         └──────────┘
     │                   ▲
     │ API Request       │
     │ + JWT Token       │ Validate
     │                   │ & Extract
     └───────────────────┘
```

### Authorization Flow
```
Request → @jwt_required() → Get Identity → Check Ownership → Allow/Deny
```

See individual task documentation for detailed architecture diagrams.

---

## 🔐 Security Best Practices

### Implemented
- ✅ Strong password hashing (bcrypt)
- ✅ JWT token-based authentication
- ✅ Ownership validation on modifications
- ✅ Admin role segregation
- ✅ Password exclusion from API responses
- ✅ Secret key from environment variables
- ✅ Business rule enforcement

### Recommended for Production
- ⚠️ Enable HTTPS/TLS
- ⚠️ Implement rate limiting
- ⚠️ Add request/response logging
- ⚠️ Use strong SECRET_KEY (32+ chars)
- ⚠️ Enable CORS with restrictions
- ⚠️ Implement token refresh mechanism
- ⚠️ Add audit logging for admin actions

---

## 📝 Document Conventions

### Structure
Each task document follows this structure:
1. Overview
2. Requirements
3. Concepts/Theory
4. Implementation Details
5. API Endpoints
6. Testing
7. Security/Best Practices
8. Troubleshooting
9. Conclusion

### Code Examples
- ✅ Complete, runnable code snippets
- ✅ Inline comments for clarity
- ✅ Error handling examples
- ✅ Real-world patterns

### Testing Examples
- ✅ cURL commands (copy-paste ready)
- ✅ Python test scripts
- ✅ Expected outputs
- ✅ Error scenarios

---

## 🤝 Contributing

### Documentation Updates

When updating documentation:

1. **Maintain consistency** with existing structure
2. **Include code examples** for all features
3. **Add testing procedures** for new functionality
4. **Update this README** if adding new documents
5. **Follow markdown best practices**

### Task Naming Convention

```
TASK_XX.md where XX is the task number (00-10)
```

---

## 📚 Additional Resources

### Flask Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTX Documentation](https://flask-restx.readthedocs.io/)
- [Flask-Bcrypt Documentation](https://flask-bcrypt.readthedocs.io/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)

### Security Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

### Project Resources
- [HBnB Documentation Repository](https://github.com/Holberton-Uy/hbnb-doc)
- Project Requirements: Part 3 Tasks 0-4

---

## 📞 Support

### For Questions About:

**Implementation Details**: See individual task documentation
**Security Concerns**: Review security sections in each task
**Testing Issues**: Check troubleshooting sections
**Configuration Problems**: See Task 0 documentation

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Nov 2025 | Initial documentation for Tasks 0-4 |

---

## ✅ Completion Checklist

- [x] Task 0: Application Configuration
- [x] Task 1: Password Hashing with Bcrypt
- [x] Task 2: JWT Authentication
- [x] Task 3: Authenticated User Access Endpoints
- [x] Task 4: Administrator Access Control
- [ ] Task 5: Database Repository Implementation
- [ ] Task 6: User Database Mapping
- [ ] Task 7: Additional Model Mappings
- [ ] Task 8: Database Relations
- [ ] Task 9: SQL Database Implementation
- [ ] Task 10: ER Diagram

---

## 📄 License

This documentation is part of the HBnB project for educational purposes.

---

**Last Updated**: November 2025
**Maintained by**: HBnB Development Team
**Status**: Active Development - Part 3 (Tasks 0-4 Complete)
