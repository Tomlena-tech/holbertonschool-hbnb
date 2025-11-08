from .base_model import BaseModel
from .place import Place
from .user import User
from app.extensions import db


class Review(BaseModel):
    """
    Review model with SQLAlchemy ORM mapping.

    Represents a review written by a user about a place.
    """

    __tablename__ = 'reviews'

    # SQLAlchemy column mappings
    _text = db.Column('text', db.Text, nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)

    # Foreign keys for relationships
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='user_reviews', foreign_keys=[user_id])
    place = db.relationship('Place', backref='reviews', foreign_keys=[place_id])

    # Unique constraint: one review per user per place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        # Validate and set relationships
        if place is not None and not isinstance(place, Place):
            raise TypeError("Place must be a place instance")
        if user is not None and not isinstance(user, User):
            raise TypeError("User must be a user instance")
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Text cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        super().is_in_range('Rating', value, 0, 6)
        self._rating = value


    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id if self.place is not None else None,
            'user_id': self.user.id if self.user is not None else None
        }
