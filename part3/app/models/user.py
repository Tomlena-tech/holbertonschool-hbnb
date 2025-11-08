from .base_model import BaseModel
from app.extensions import db
from flask import current_app
import re


class User(BaseModel):
    """
    Represents a user in the system with SQLAlchemy ORM mapping.

    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes,
        along with utility methods like `save()` and validation helpers.

    Class Attributes:
        emails (set): Tracks unique user emails across all instances to
            prevent duplicates.

    Database Columns:
        first_name (String(50)): User's first name, not nullable.
        last_name (String(50)): User's last name, not nullable.
        email (String(120)): Unique and validated email, not nullable.
        password (String(128)): Hashed password, not nullable.
        is_admin (Boolean): Admin privileges flag, default False.

    Instance Attributes:
        places (list): List of places associated with the user.
        reviews (list): List of reviews authored by the user.
    """
    __tablename__ = 'users'

    # SQLAlchemy column mappings (mapped to private attributes)
    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    _User__is_admin = db.Column('is_admin', db.Boolean, default=False,
                                 nullable=False)

    # Class attribute for in-memory email tracking
    emails = set()

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a new User instance.

        Args:
            first_name (str): The user's first name (max 50 characters).
            last_name (str): The user's last name (max 50 characters).
            email (str): The user's unique, valid email address.
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.

        Raises:
            TypeError: If argument types are incorrect.
            ValueError: If the email format is invalid or already exists.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        bcrypt = current_app.extensions['bcrypt']
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        bcrypt = current_app.extensions['bcrypt']
        return bcrypt.check_password_hash(self.password, password)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """
        Validate and set the user's first name.

        Args:
            value (str): The first name to assign.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the name exceeds 50 characters.
        """
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length("First name", value, 50)
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length("Last name", value, 50)
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """
        Validate and set the user's email.

        Ensures:
            - Value is a string.
            - Email format is valid.
            - Email is unique across all users.

        Args:
            value (str): The email address to assign.

        Raises:
            TypeError: If the email is not a string.
            ValueError: If the email format is invalid or already exists.
        """
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        if hasattr(self, '_email'):
            if self._email != value and value in User.emails:
                raise ValueError("Email already exists")
            User.emails.discard(self._email)
        else:
            if value in User.emails:
                raise ValueError("Email already exists")
        self._email = value
        User.emails.add(value)

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """
        Validate and set the admin status.

        Args:
            value (bool): True if the user is an admin, False otherwise.

        Raises:
            TypeError: If value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self.__is_admin = value

    def add_place(self, place):
        """
        Add a place to the user's associated places list.

        Args:
            place (object): A Place instance to associate with the user.
        """
        self.places.append(place)

    def add_review(self, review):
        """
        Add a review to the user's associated reviews list.

        Args:
            review (object): A Review instance to associate with the user.
        """
        self.reviews.append(review)

    def delete_review(self, review):
        """
        Remove a review from the user's associated reviews list.

        Args:
            review (object): The Review instance to remove.

        Raises:
            ValueError: If the review is not in the user's list.
        """
        self.reviews.remove(review)

    def update(self, data):
        """
        Update user attributes, with special handling for password hashing.

        Args:
            data (dict): A dictionary containing attribute names and their new values.
        """
        for key, value in data.items():
            if key == 'password':
                # Hash the password instead of setting it directly
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

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
            'email': self.email
        }
