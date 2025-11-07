from .base_model import BaseModel
from app import db


class Amenity(BaseModel):
    
    __tablename__ = 'amenities'
    
    # SQLAlchemy Columns
    name = db.Column(db.String(50), nullable=False, unique=True)


    def __init__(self, name):

    # Validate before assigning
        self.validate_name(name)
        
    # Relationship
    # places est créé automatiquement via backref dans Place.amenities
        
        
        self.name = name

    def validate_name(self, value):
        """Validate name."""
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name exceeds maximum length of 50")
    
    def to_dict(self):
        """Convert to dict."""
        return {
            'id': self.id,
            'name': self.name
        }
