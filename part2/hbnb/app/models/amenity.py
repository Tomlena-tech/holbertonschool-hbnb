#!/usr/bin/python3
"""Amenity model with property validation"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity/facility in the system.
    
    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes.
    
    Instance Attributes:
        name (str): Amenity name (max 50 characters).
    """
    
    def __init__(self, name):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): The amenity name (max 50 characters).
            
        Raises:
            TypeError: If name is not a string.
            ValueError: If name is empty or exceeds 50 characters.
        """
        super().__init__()
        self.name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Validate and set the amenity name.
        
        Args:
            value (str): The name to assign.
            
        Raises:
            TypeError: If value is not a string.
            ValueError: If name is empty or exceeds 50 characters.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value or not value.strip():
            raise ValueError("Name is required")
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        self._name = value
    
    def to_dict(self):
        """
        Convert the Amenity instance into a dictionary.
        
        Returns:
            dict: Dictionary containing amenity information.
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        