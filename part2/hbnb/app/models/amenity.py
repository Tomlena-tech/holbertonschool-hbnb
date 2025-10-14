#!/usr/bin/python3
"""Amenity model"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Model representing an amenity/facility"""
    
    def __init__(self, *, name: str):
        """Initialize a new amenity
        
        Args:
            name: Amenity name (required, max 50 characters)
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate name
        if not name or len(name) > 50:
            raise ValueError("Name is required and must not exceed 50 characters")
        
        self.name = name
        