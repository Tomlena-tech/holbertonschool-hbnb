#!/usr/bin/python3
"""Place model with property validation"""
from app.models.base_model import BaseModel


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
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): The place title (max 100 characters).
            description (str): Description of the place.
            price (float): Price per night (must be > 0).
            latitude (float): Latitude coordinate (-90.0 to 90.0).
            longitude (float): Longitude coordinate (-180.0 to 180.0).
            owner (User): The user who owns this place.
            
        Raises:
            TypeError: If argument types are incorrect.
            ValueError: If values are out of valid range.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        
        owner.add_place(self)
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        """
        Validate and set the place title.
        
        Args:
            value (str): The title to assign.
            
        Raises:
            TypeError: If value is not a string.
            ValueError: If title is empty or exceeds 100 characters.
        """
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value or not value.strip():
            raise ValueError("Title is required")
        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters")
        self._title = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        """
        Validate and set the place description.
        
        Args:
            value (str): The description to assign.
            
        Raises:
            TypeError: If value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        """
        Validate and set the price.
        
        Args:
            value (float): The price to assign.
            
        Raises:
            TypeError: If value is not a number.
            ValueError: If price is not greater than 0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        self._price = float(value)
    
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """
        Validate and set the latitude.
        
        Args:
            value (float): The latitude to assign.
            
        Raises:
            TypeError: If value is not a number.
            ValueError: If latitude is not between -90.0 and 90.0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """
        Validate and set the longitude.
        
        Args:
            value (float): The longitude to assign.
            
        Raises:
            TypeError: If value is not a number.
            ValueError: If longitude is not between -180.0 and 180.0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        """
        Validate and set the owner.
        
        Args:
            value: The User object who owns this place.
            
        Raises:
            TypeError: If value is not a User instance.
        """
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
        self._owner = value
    
    def add_review(self, review):
        """
        Add a review to this place.
        
        Args:
            review (Review): A Review instance to associate.
        """
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """
        Add an amenity to this place.
        
        Args:
            amenity (Amenity): An Amenity instance to associate.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def average_rating(self):
        """
        Calculate the average rating from all reviews.
        
        Returns:
            float: Average rating or 0.0 if no reviews.
        """
        if not self.reviews:
            return 0.0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def to_dict(self):
        """
        Convert the Place instance into a dictionary.
        
        Returns:
            dict: Dictionary containing place information.
        """
        result = super().to_dict()
        if 'owner' in result and hasattr(self._owner, 'id'):
            result['owner'] = self._owner.id
        return result
    