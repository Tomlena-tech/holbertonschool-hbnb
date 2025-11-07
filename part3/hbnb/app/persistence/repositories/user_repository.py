"""
User Repository Module

This module provides the UserRepository class which extends SQLAlchemyRepository
with user-specific database operations.
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User entity with user-specific queries.
    
    Extends SQLAlchemyRepository to provide custom user operations
    beyond the basic CRUD functionality.
    """
    
    def __init__(self):
        """Initialize the UserRepository with the User model."""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.
        
        Args:
            email (str): The email address to search for.
            
        Returns:
            User: The user object if found, None otherwise.
        """
        return self.model.query.filter_by(email=email).first()
