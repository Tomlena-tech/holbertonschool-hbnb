#!/usr/bin/python3
"""Review model with property validation"""
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review for a place in the system.
    
    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes.
    
    Instance Attributes:
        text (str): Review text/comment (required).
        rating (int): Rating from 1 to 5 (required).
        place (Place): Place being reviewed.
        user (User): User who wrote the review.
    """
    
    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): The review text/comment.
            rating (int): Rating from 1 to 5.
            place (Place): The place being reviewed.
            user (User): The user who wrote the review.
            
        Raises:
            TypeError: If argument types are incorrect.
            ValueError: If values are invalid.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        
        # Add this review to the place
        place.add_review(self)
        # Add this review to the user
        user.add_review(self)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        """
        Validate and set the review text.
        
        Args:
            value (str): The text to assign.
            
        Raises:
            TypeError: If value is not a string.
            ValueError: If text is empty or only whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Review text must be a string")
        if not value or not value.strip():
            raise ValueError("Review text is required")
        self._text = value
    
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        """
        Validate and set the rating.
        
        Args:
            value (int): The rating to assign (1-5).
            
        Raises:
            TypeError: If value is not an integer.
            ValueError: If rating is not between 1 and 5.
        """
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
    
    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        """
        Validate and set the place.
        
        Args:
            value: The Place object being reviewed.
            
        Raises:
            TypeError: If value is not a Place instance.
        """
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError("Place must be a Place instance")
        self._place = value
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        """
        Validate and set the user.
        
        Args:
            value: The User object who wrote the review.
            
        Raises:
            TypeError: If value is not a User instance.
        """
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("User must be a User instance")
        self._user = value
    
    def to_dict(self):
        """
        Convert the Review instance into a dictionary.
        
        Returns:
            dict: Dictionary containing review information.
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place': self._place.id,
            'user': self._user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        