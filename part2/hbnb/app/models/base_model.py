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
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
    
    def delete(self):
        """Delete the entity (to be implemented with repository)"""
        pass
    
    def to_dict(self): #add to don't have to repeat in each class
        """Convert object to dictionary representation
        
        Returns:
            dict: Dictionary with all attributes
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
