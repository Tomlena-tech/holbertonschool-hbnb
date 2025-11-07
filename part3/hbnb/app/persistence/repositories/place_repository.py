"""
Place Repository Module

This module provides the PlaceRepository class which extends SQLAlchemyRepository
with place-specific database operations.
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place entity with place-specific queries.
    
    Extends SQLAlchemyRepository to provide custom place operations
    beyond the basic CRUD functionality.
    """
    
    def __init__(self):
        """Initialize the PlaceRepository with the Place model."""
        super().__init__(Place)
    
    def get_places_by_owner(self, owner_id):
        """
        Retrieve all places owned by a specific user.
        
        Args:
            owner_id (str): The owner's user ID.
            
        Returns:
            list[Place]: List of places owned by the user.
        """
        return self.model.query.filter_by(owner_id=owner_id).all()
