#!/usr/bin/python3
"""Review model"""
from models.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.place import Place
    from models.user import User


class Review(BaseModel):
    """Model representing a review for a place"""
    
    def __init__(self, *, text: str, rating: int, place: "Place", user: "User"):
        """Initialize a new review
        
        Args:
            text: Review text/comment (required)
            rating: Rating from 1 to 5 (required)
            place: Place being reviewed (required)
            user: User who wrote the review (required)
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate text
        if not text or not text.strip():
            raise ValueError("Review text is required")
        
        # Validate rating
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        
        # Add this review to the place
        place.add_review(self)
        