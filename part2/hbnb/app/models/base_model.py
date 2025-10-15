#!/usr/bin/python3
"""Base model for all entities"""
import uuid
from datetime import datetime
from abc import ABC


class BaseModel(ABC):
    """Abstract base class with common attributes and methods"""
    
    def __init__(self):
        """Initialize base attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()
    
    def delete(self):
        """Delete the entity"""
        pass
    
    def is_max_length(self, field_name, value, max_length):
        """
        Helper method to validate maximum length.
        
        Args:
            field_name (str): Name of the field being validated
            value (str): The value to check
            max_length (int): Maximum allowed length
            
        Raises:
            ValueError: If value exceeds max_length
        """
        if len(value) > max_length:
            raise ValueError(f"{field_name} must not exceed {max_length} characters")
    
    def to_dict(self):
        """Convert object to dictionary representation
        
        Returns:
            dict: Dictionary with all attributes
        """
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                # Pour les attributs privés, on enlève l'underscore
                clean_key = key.lstrip('_')
                if isinstance(value, datetime):
                    result[clean_key] = value.isoformat()
                elif hasattr(value, 'id'):
                    result[clean_key] = value.id
                elif isinstance(value, list):
                    result[clean_key] = [item.id if hasattr(item, 'id') else item for item in value]
                else:
                    result[clean_key] = value
            elif not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif hasattr(value, 'id'):
                    result[key] = value.id
                elif isinstance(value, list):
                    result[key] = [item.id if hasattr(item, 'id') else item for item in value]
                else:
                    result[key] = value
        return result
    
    def update(self, data):
        """Update the attributes based on the provided dictionary
        
        Args:
            data: Dictionary with attributes to update
            
        Returns:
            self: The updated object
        """
        for key, value in data.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
        self.save()
        return self
    