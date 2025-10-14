#!/usr/bin/python3
"""User - Business entity for HBnB project"""
from app.models.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.place import Place


class User(BaseModel):
    """Model representing a user in the HBnB system"""
    
    def __init__(self, *, first_name: str, last_name: str, email: str, 
                 is_admin: bool = False):
        """Initialize a new user
        
        Args:
            first_name: First name (required, max 50 characters)
            last_name: Last name (required, max 50 characters)
            email: Email address (required, valid format)
            is_admin: Admin status (default: False)
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate first_name
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must not exceed 50 characters")
        
        # Validate last_name
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must not exceed 50 characters")
        
        # Validate email
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place: "Place") -> None:
        """Add a place to the user's owned places
        
        Args:
            place: Place object to add
        """
        if place not in self.places:
            self.places.append(place)

    def remove_place(self, place: "Place") -> None:
        """Remove a place from owned places
        
        Args:
            place: Place object to remove
        """
        if place in self.places:
            self.places.remove(place)
