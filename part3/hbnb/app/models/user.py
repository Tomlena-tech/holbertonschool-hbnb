from .base_model import BaseModel
from app import db
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    """
    Represents a user in the system.

    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes,
        along with utility methods like `save()` and validation helpers.

    Table Attributes (SQLAlchemy Columns):
        first_name (str): User's first name (max 50 characters).
        last_name (str): User's last name (max 50 characters).
        email (str): Unique and validated email address.
        password_hash (str): Hashed password (max 128 characters).
        is_admin (bool): Indicates whether the user has administrative privileges.
    
    Relationships:
        places: One-to-many relationship with Place model.
        reviews: One-to-many relationship with Review model.
    """
    __tablename__ = 'users'
    
    # SQLAlchemy Columns
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a new User instance.

        Args:
            first_name (str): The user's first name (max 50 characters).
            last_name (str): The user's last name (max 50 characters).
            email (str): The user's unique, valid email address.
            password (str): The user's password (will be hashed).
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.

        Raises:
            TypeError: If argument types are incorrect.
            ValueError: If the email format is invalid or validation fails.
        """
        # Validate before setting
        self.validate_first_name(first_name)
        self.validate_last_name(last_name)
        self.validate_email(email)
        
        # Set attributes
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify if password matches the hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def verify_password(self, password: str) -> bool:
        """Alias for check_password to match JWT tutorial naming."""
        return self.check_password(password)
    
    # Validation methods
    def validate_first_name(self, value):
        """Validate first name"""
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name exceeds maximum length of 50")
    
    def validate_last_name(self, value):
        """Validate last name"""
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name exceeds maximum length of 50")
    
    def validate_email(self, value):
        """Validate email format"""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")

    def to_dict(self):
        """
        Convert the User instance into a dictionary representation.

        Returns:
            dict: A dictionary containing basic user information.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
