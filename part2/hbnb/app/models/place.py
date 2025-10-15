#!/usr/bin/python3
"""Place model with property validation"""
from .base_model import BaseModel
from datetime import datetime


class Place(BaseModel):
    """
    Represents a place/accommodation in the system.
    Inherits from:
        BaseModel: Provides `id`, `created_at`, and `updated_at` attributes.
    Instance Attributes:
        title (str): Place title (max 100 characters).
        description (str): Place description (optional).
        price (float): Price per night (must be ≥ 0).
        latitude (float): Latitude coordinate (-90.0 to 90.0).
        longitude (float): Longitude coordinate (-180.0 to 180.0).
        owner_id (str): ID of the User who owns this place.
        amenities (list[str]): List of amenities IDs.
    """

    def __init__(self, title: str, price: float, latitude: float, longitude: float,
                 owner_id: str, description: str = None, amenities: list = None):
        super().__init__()
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []   # liste d'IDs (str)

    # ----------------  validateurs  ----------------
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string or None")
        self._description = value or ""

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a float/int")
        if value < 0:
            raise ValueError("Price must be non-negative")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a float/int")
        super().is_in_range("latitude", value, -90.0, 90.0)
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a float/int")
        super().is_in_range("longitude", value, -180.0, 180.0)
        self._longitude = float(value)

    # ----------------  sérialisation  ----------------
    def to_dict(self, light=False):
        if light:
            return {
                'id': self.id,
                'title': self.title,
                'latitude': self.latitude,
                'longitude': self.longitude
        }
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'amenities': self.amenities
    }
    