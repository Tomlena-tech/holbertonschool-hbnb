#!/usr/bin/python3
"""Facade complète – compatible TES modèles main"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from models.place import Place   # <-- ajuste si ton import est différent


class HBnBFacade:
    """Facade for HBnB application operations."""

    def __init__(self):
        self.user_repo   = InMemoryRepository()
        self.amenity_repo= InMemoryRepository()
        self.place_repo  = InMemoryRepository()

    # ----------  USERS  ----------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for k in ('first_name', 'last_name', 'email'):
            if k in user_data:
                setattr(user, k, user_data[k])
        self.user_repo.update(user_id, user)
        return user

    # ----------  AMENITIES  ----------
    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError('Name is required')
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # ----------  PLACES  ----------
    def create_place(self, place_data):
        if not place_data.get('title'):
            raise ValueError('Title is required')
        if 'price' not in place_data:
            raise ValueError('Price is required')
        try:
            price = float(place_data['price'])
            if price <= 0:
                raise ValueError('Price must be positive')
        except (TypeError, ValueError):
            raise ValueError('Price must be a positive number')
        if 'latitude' not in place_data:
            raise ValueError('Latitude is required')
        try:
            latitude = float(place_data['latitude'])
            if not (-90.0 < latitude < 90.0):
                raise ValueError('Latitude must be between -90 and 90')
        except (TypeError, ValueError):
            raise ValueError('Latitude must be a number between -90 and 90')
        if 'longitude' not in place_data:
            raise ValueError('Longitude is required')
        try:
            longitude = float(place_data['longitude'])
            if not (-180.0 < longitude < 180.0):
                raise ValueError('Longitude must be between -180 and 180')
        except (TypeError, ValueError):
            raise ValueError('Longitude must be a number between -180 and 180')
        if not place_data.get('owner_id'):
            raise ValueError('Owner ID is required')
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=place_data['owner_id'],
            amenities=place_data.get('amenities', [])
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if 'title' in place_data:
            if not place_data['title']:
                raise ValueError('Title cannot be empty')
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            try:
                price = float(place_data['price'])
                if price <= 0:
                    raise ValueError('Price must be positive')
                place.price = price
            except (TypeError, ValueError):
                raise ValueError('Price must be a positive number')
        if 'latitude' in place_data:
            try:
                latitude = float(place_data['latitude'])
                if not (-90.0 < latitude < 90.0):
                    raise ValueError('Latitude must be between -90 and 90')
                place.latitude = latitude
            except (TypeError, ValueError):
                raise ValueError('Latitude must be a number between -90 and 90')
        if 'longitude' in place_data:
            try:
                longitude = float(place_data['longitude'])
                if not (-180.0 < longitude < 180.0):
                    raise ValueError('Longitude must be between -180 and 180')
                place.longitude = longitude
            except (TypeError, ValueError):
                raise ValueError('Longitude must be a number between -180 and 180')
        if 'owner_id' in place_data:
            place.owner_id = place_data['owner_id']
        if 'amenities' in place_data:
            place.amenities = place_data['amenities']
        self.place_repo.update(place_id, place)
        return place
    # Singleton utilisé par les namespaces
facade = HBnBFacade()
