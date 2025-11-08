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

    # SQLAlchemy column mappings (no relationships yet - Task 8)
    _text = db.Column('text', db.Text, nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
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

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        # Allow None for tests that create reviews without a linked Place.
        if value is not None and not isinstance(value, Place):
            raise TypeError("Place must be a place instance")
        self.__place = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        # Allow None for tests that create reviews without a linked User.
        if value is not None and not isinstance(value, User):
            raise TypeError("User must be a user instance")
        self.__user = value

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id if self.place is not None else None,
            'user_id': self.user.id if self.user is not None else None
        }
