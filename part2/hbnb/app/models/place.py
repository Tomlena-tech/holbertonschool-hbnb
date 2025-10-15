#!/usr/bin/python3
"""Place model with property validation"""
from .base_model import BaseModel
from .user import User
class Place(BaseModel):
    """
    Represents a place/accommodation in the system.
    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes.
    Instance Attributes:
        title (str): Place title (max 100 characters).
        description (str): Place description (optional).
        price (float): Price per night (must be > 0).
        latitude (float): Latitude coordinate (-90.0 to 90.0).
        longitude (float): Longitude coordinate (-180.0 to 180.0).
        owner (User): User who owns this place.
        reviews (list): List of reviews for this place.
        amenities (list): List of amenities available.
    """
    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner,
        description=None
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self.__title = value
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self.__description = value
    @property
    def price(self):
        return self.__price
    @price.setter    
    def price(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        self.__price = value
    @property
    def latitude(self):
        return self.__latitude
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        super().is_in_range("latitude", value, -90.0, 90.0)
        self.__latitude = float(value)
    @property
    def longitude(self):
        return self.__longitude
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        super().is_in_range("longitude", value, -180.0, 180.0)
        self.__longitude = float(value)
    @property
    def owner(self):
        return self.__owner
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
        self.__owner = value
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    def delete_review(self, review):
        """Delete a review from the place."""
        self.reviews.remove(review)
    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id
        }
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': self.amenities,
            'reviews': self.reviews
        }
        