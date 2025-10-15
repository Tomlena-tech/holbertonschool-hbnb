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
            ValueError: If value is empty or exceeds max_length
        """
        if not value or len(value) == 0:
            raise ValueError(f"{field_name} is required")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must not exceed {max_length} characters")
    
    def to_dict(self):
        """Convert object to dictionary representation
        
        Returns:
            dict: Dictionary with all attributes
        """
        result = {}
        
        # Add standard attributes
        result['id'] = self.id
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        
        # Add other attributes
        for key, value in self.__dict__.items():
            # Skip already added attributes
            if key in ['id', 'created_at', 'updated_at']:
                continue
                
            # Handle private attributes (starting with _)
            if key.startswith('_'):
                clean_key = key.lstrip('_')
                if hasattr(value, 'id'):
                    result[clean_key] = value.id
                elif isinstance(value, list):
                    result[clean_key] = [item.id if hasattr(item, 'id') else item for item in value]
                else:
                    result[clean_key] = value
            # Handle public attributes
            else:
                if hasattr(value, 'id'):
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
    