from .base_model import BaseModel
from app import db

class Review(BaseModel):
    
    
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False) 
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # place et user sont créés automatiquement via backref dans Place.reviews et User.reviews

    def __init__(self, text, rating, place_id, user_id):

        # Validate before assigning
        self.validate_text(text)
        self.validate_rating(rating)
        
        #SQLAlchemy columns
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        
    def validate_text(self, value):
        """Validate text."""
        if not value:
            raise ValueError("Text cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
    
    def validate_rating(self, value):
        """Validate rating (1-5)."""
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
    
    def to_dict(self):
        """Convert to dict."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        }

