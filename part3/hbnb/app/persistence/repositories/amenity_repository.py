"""
Amenity Repository Module

This module provides the AmenityRepository class which extends SQLAlchemyRepository
with amenity-specific database operations.
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity entity with amenity-specific queries.
    
    Extends SQLAlchemyRepository to provide custom amenity operations
    beyond the basic CRUD functionality.
    """
    
    def __init__(self):
        """Initialize the AmenityRepository with the Amenity model."""
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by its name.
        
        Args:
            name (str): The amenity name.
            
        Returns:
            Amenity: The amenity if found, None otherwise.
        """
        return self.model.query.filter_by(name=name).first()
