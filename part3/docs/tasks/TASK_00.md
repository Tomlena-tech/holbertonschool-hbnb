# Task 0: Application Configuration

## Overview

This document describes the implementation of the Flask Application Factory pattern with configuration management for the HBnB application.

**Task Objective**: Update the Flask Application Factory to include a configuration object, enabling the application to switch between different environment settings (development, testing, production).

**Completion Date**: November 2025
**Status**: ✅ Completed

---

## Table of Contents

1. [Requirements](#requirements)
2. [Architecture](#architecture)
3. [Implementation Details](#implementation-details)
4. [Configuration Options](#configuration-options)
5. [Usage Examples](#usage-examples)
6. [Testing](#testing)
7. [Best Practices](#best-practices)

---

## Requirements

### Functional Requirements

1. **Application Factory Pattern**:
   - Implement `create_app()` method that accepts configuration object
   - Use `config.DevelopmentConfig` as default configuration
   - Apply configuration to Flask app instance

2. **Configuration Management**:
   - Support multiple environment configurations
   - Allow runtime configuration selection
   - Provide sensible defaults

### Non-Functional Requirements

- Clean separation of configuration from application code
- Easy switching between environments
- Support for environment variable overrides
- Extensible configuration system

---

## Architecture

### Application Factory Pattern

The Application Factory pattern creates Flask application instances on demand with specific configurations, enabling:

- **Multiple Instances**: Create different app instances with different configs
- **Testing**: Easy to create isolated app instances for testing
- **Flexibility**: Runtime configuration selection
- **Security**: Configuration isolation

### Design Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                     Configuration Layer                      │
├─────────────────────────────────────────────────────────────┤
│  config.py                                                   │
│  ├── Config (Base)                                          │
│  │   ├── SECRET_KEY                                         │
│  │   ├── DEBUG                                              │
│  │   └── ADMIN_*                                            │
│  ├── DevelopmentConfig (extends Config)                     │
│  │   └── DEBUG = True                                       │
│  ├── TestingConfig (extends Config)                         │
│  │   └── TESTING = True                                     │
│  └── ProductionConfig (extends Config)                      │
│      └── DEBUG = False                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Application Factory                         │
├─────────────────────────────────────────────────────────────┤
│  app/__init__.py                                            │
│                                                              │
│  def create_app(config_class="config.DevelopmentConfig"):  │
│      app = Flask(__name__)                                  │
│      app.config.from_object(config_class)                   │
│      # Initialize extensions                                │
│      # Register blueprints                                  │
│      return app                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Instance                      │
├─────────────────────────────────────────────────────────────┤
│  Development: create_app()                                   │
│  Testing: create_app("config.TestingConfig")                │
│  Production: create_app("config.ProductionConfig")          │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### 1. Configuration File Structure

**File**: `config.py`

```python
import os


class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

    # Admin user configuration
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@hbnb.io')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')
    ADMIN_FIRST_NAME = os.getenv('ADMIN_FIRST_NAME', 'Admin')
    ADMIN_LAST_NAME = os.getenv('ADMIN_LAST_NAME', 'HBnB')


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

**Key Features**:
- **Inheritance**: Child configs inherit from base `Config` class
- **Environment Variables**: Support for `os.getenv()` overrides
- **Defaults**: Sensible defaults for all configurations
- **Dictionary Mapping**: Easy config selection via string keys

### 2. Application Factory Implementation

**File**: `app/__init__.py`

```python
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Import namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

# Instantiate extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application Factory: Creates and configures a Flask application.

    Args:
        config_class (str): Fully qualified configuration class name.
            Defaults to 'config.DevelopmentConfig'.

    Returns:
        Flask: Configured Flask application instance.

    Example:
        # Development (default)
        app = create_app()

        # Testing
        app = create_app("config.TestingConfig")

        # Production
        app = create_app("config.ProductionConfig")
    """
    app = Flask(__name__)

    # Load configuration from object
    app.config.from_object(config_class)

    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Initialize extensions with the Flask app
    bcrypt.init_app(app)
    app.extensions['bcrypt'] = bcrypt
    jwt.init_app(app)
    app.extensions['jwt'] = jwt

    # Seed the initial admin user
    with app.app_context():
        seed_admin_user(app)

    # Register API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
```

**Key Features**:
- **Parameter Acceptance**: Takes `config_class` as string parameter
- **Default Configuration**: Uses `DevelopmentConfig` by default
- **from_object()**: Flask method to load configuration from class
- **Extension Initialization**: All extensions initialized after configuration
- **Return Instance**: Returns configured Flask app

### 3. Application Entry Point

**File**: `run.py`

```python
from app import create_app

# Create app with default (development) configuration
app = create_app()

if __name__ == '__main__':
    app.run()
```

**Alternative Configurations**:

```python
# Testing configuration
app = create_app("config.TestingConfig")

# Production configuration
app = create_app("config.ProductionConfig")

# Using dictionary mapping
from config import config
app = create_app(config['production'])
```

---

## Configuration Options

### Base Configuration (`Config`)

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `SECRET_KEY` | string | 'default_secret_key' | JWT signing key, session encryption |
| `DEBUG` | boolean | False | Enable debug mode |
| `ADMIN_EMAIL` | string | 'admin@hbnb.io' | Default admin email |
| `ADMIN_PASSWORD` | string | 'admin1234' | Default admin password |
| `ADMIN_FIRST_NAME` | string | 'Admin' | Default admin first name |
| `ADMIN_LAST_NAME` | string | 'HBnB' | Default admin last name |

### Development Configuration (`DevelopmentConfig`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `DEBUG` | True | Enable debug mode, auto-reload, detailed errors |

### Testing Configuration (`TestingConfig`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `TESTING` | True | Enable testing mode |
| `DEBUG` | True | Enable debug output for tests |

### Production Configuration (`ProductionConfig`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `DEBUG` | False | Disable debug mode for security |

---

## Usage Examples

### 1. Development Environment

```python
from app import create_app

# Create development app (default)
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 2. Testing Environment

```python
import unittest
from app import create_app

class TestCase(unittest.TestCase):
    def setUp(self):
        # Create testing app instance
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_example(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
```

### 3. Production Environment

```python
from app import create_app
import os

# Create production app
app = create_app("config.ProductionConfig")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

### 4. Environment Variable Override

```bash
# Set environment variables
export SECRET_KEY="super-secret-production-key"
export ADMIN_EMAIL="admin@mycompany.com"
export ADMIN_PASSWORD="StrongPassword123!"

# Run application (uses environment variables)
python run.py
```

---

## Testing

### Verification Steps

1. **Default Configuration Test**:
   ```python
   from app import create_app

   app = create_app()
   assert app.config['DEBUG'] == True
   print("✅ Default configuration loaded")
   ```

2. **Custom Configuration Test**:
   ```python
   app = create_app("config.ProductionConfig")
   assert app.config['DEBUG'] == False
   print("✅ Production configuration loaded")
   ```

3. **Environment Variable Test**:
   ```python
   import os
   os.environ['SECRET_KEY'] = 'test-key'

   app = create_app()
   assert app.config['SECRET_KEY'] == 'test-key'
   print("✅ Environment variable override works")
   ```

### Manual Testing

```bash
# Test development mode
python run.py

# Check debug mode is enabled
curl http://localhost:5000/api/v1/users/
# Should show detailed errors if any occur

# Test with environment variables
SECRET_KEY="my-secret" python run.py
```

---

## Best Practices

### 1. Security

**Production**:
- ✅ Use strong `SECRET_KEY` from environment variable
- ✅ Never commit secrets to version control
- ✅ Set `DEBUG = False` in production
- ✅ Use environment-specific credentials

**Development**:
- ✅ Use different `SECRET_KEY` than production
- ✅ Keep test credentials separate
- ✅ Document default credentials

### 2. Environment Variables

**Recommended Approach**:

```bash
# .env.development
SECRET_KEY=dev-secret-key-123
DEBUG=True
ADMIN_EMAIL=admin@dev.local

# .env.production
SECRET_KEY=prod-strong-secret-key-xyz
DEBUG=False
ADMIN_EMAIL=admin@company.com
```

**Loading with python-dotenv**:

```python
from dotenv import load_dotenv
import os

# Load environment-specific .env file
env = os.getenv('FLASK_ENV', 'development')
load_dotenv(f'.env.{env}')

from app import create_app
app = create_app(f"config.{env.capitalize()}Config")
```

### 3. Configuration Validation

**Add validation in config classes**:

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    @classmethod
    def validate(cls):
        """Validate critical configuration settings."""
        if cls.SECRET_KEY == 'default_secret_key':
            raise ValueError("SECRET_KEY must be set in production!")
```

### 4. Multiple Instances

**Creating multiple apps**:

```python
# Development API server
dev_app = create_app("config.DevelopmentConfig")

# Testing instance for unit tests
test_app = create_app("config.TestingConfig")

# Both can run simultaneously for different purposes
```

---

## Troubleshooting

### Issue: Configuration Not Loading

**Symptoms**: App uses default values despite setting environment variables

**Solutions**:
1. Verify environment variables are exported:
   ```bash
   echo $SECRET_KEY
   ```
2. Check variable names match exactly (case-sensitive)
3. Restart application after setting variables
4. Use `.env` file with `python-dotenv`

### Issue: Wrong Configuration Loaded

**Symptoms**: App runs in wrong mode (debug on in production)

**Solutions**:
1. Verify config class string is correct:
   ```python
   # Wrong
   app = create_app("ProductionConfig")

   # Correct
   app = create_app("config.ProductionConfig")
   ```
2. Check for typos in config class names
3. Verify config is being passed to `create_app()`

### Issue: Import Errors

**Symptoms**: `ImportError: cannot import name 'Config'`

**Solutions**:
1. Ensure `config.py` is in project root
2. Check Python path includes project root
3. Verify config class names match exactly

---

## Advanced Configuration

### Database Configuration

**Extending for database support**:

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL',
        'sqlite:///dev.db'
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:pass@localhost/dbname'
    )
```

### Logging Configuration

```python
class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')


class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    LOG_LEVEL = 'WARNING'
    LOG_FILE = '/var/log/hbnb/app.log'
```

---

## Conclusion

The Application Factory pattern with configuration management provides:

**Key Benefits**:
- ✅ Environment-specific configurations
- ✅ Easy testing with isolated instances
- ✅ Secure credential management
- ✅ Flexible deployment options
- ✅ Clean code organization

**Implementation Status**:
- ✅ Base configuration class created
- ✅ Development, Testing, Production configs defined
- ✅ Application factory accepts config parameter
- ✅ Environment variable support implemented
- ✅ Extension initialization integrated
- ✅ Admin seeding configured

This foundational pattern enables scalable, maintainable, and secure Flask application development across all environments.

---

**Next**: [Task 1: Password Hashing with Bcrypt](TASK_01.md)
