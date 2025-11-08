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
