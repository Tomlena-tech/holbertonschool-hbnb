#!/usr/bin/python3
"""Place - Holberton-compliant"""
from app.models.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity


class Place(BaseModel):
    """Model representing a place in the HBnB system"""
    
    def __init__(self, *, title: str, description: str,
                 price: float, latitude: float, longitude: float,
                 owner: "User"):
        """Initialize a new place
        
        Args:
            title: Place title (required, max 100 characters)
            description: Place description (optional)
            price: Price per night (must be > 0)
            latitude: Latitude coordinate (-90.0 to 90.0)
            longitude: Longitude coordinate (-180.0 to 180.0)
            owner: User object who owns this place
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate title
        if not title or len(title) > 100:
            raise ValueError("Title is required and must not exceed 100 characters")
        
        # Validate price
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        # Validate latitude
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        
        # Validate longitude
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        
        owner.add_place(self)

    def add_review(self, review: "Review") -> None:
        """Add a review to this place
        
        Args:
            review: Review object to add
        """
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity: "Amenity") -> None:
        """Add an amenity to this place
        
        Args:
            amenity: Amenity object to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def average_rating(self) -> float:
        """Calculate average rating from reviews
        
        Returns:
            float: Average rating or 0.0 if no reviews
        """
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    def is_available(self, start: str, end: str) -> bool:
        """Check if place is available for given dates
        
        Args:
            start: Start date string
            end: End date string
            
        Returns:
            bool: True if available (stub implementation)
        """
        return True
    