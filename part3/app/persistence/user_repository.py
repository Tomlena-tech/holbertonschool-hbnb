"""
User Repository Module

This module provides a specialized repository for User model operations,
extending the base SQLAlchemyRepository with user-specific functionality.
"""

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User model with specialized query methods.

    Extends SQLAlchemyRepository to provide user-specific operations
    such as email-based lookups for authentication purposes.
    """

    def __init__(self):
        """Initialize UserRepository with User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.

        This method is commonly used for authentication and login flows
        where the email serves as the unique identifier for user lookup.

        Args:
            email (str): The email address to search for.

        Returns:
            User: The user instance if found, None otherwise.

        Example:
            >>> user_repo = UserRepository()
            >>> user = user_repo.get_user_by_email("admin@hbnb.io")
            >>> if user:
            ...     print(f"Found user: {user.first_name}")
        """
        return self.get_by_attribute('email', email)
