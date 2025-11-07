"""
Review Repository Module

This module provides the ReviewRepository class which extends SQLAlchemyRepository
with review-specific database operations.
"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review entity with review-specific queries.
    
    Extends SQLAlchemyRepository to provide custom review operations
    beyond the basic CRUD functionality.
    """
    
    def __init__(self):
        """Initialize the ReviewRepository with the Review model."""
        super().__init__(Review)
    
    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): The place ID.
            
        Returns:
            list[Review]: List of reviews for the place.
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """
        Retrieve all reviews written by a specific user.
        
        Args:
            user_id (str): The user ID.
            
        Returns:
            list[Review]: List of reviews written by the user.
        """
        return self.model.query.filter_by(user_id=user_id).all()
