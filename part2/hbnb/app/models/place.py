#!/usr/bin/python3
"""Place - Holberton-compliant"""
from models.base_model import BaseModel
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
        """Initialize a new place"""
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
        
        # Sync bidirectional relationship
        owner.add_place(self)
        # relations with reviews and amenities are managed in their respective classes
    def add_review(self, review: "Review") -> None:
        """Add a review to this place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity: "Amenity") -> None:
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def average_rating(self) -> float:
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    def is_available(self, start: str, end: str) -> bool:
        """Check availability (stub)"""
        return True
