#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade for HBnB application operations."""

    def __init__(self):
        self.user_repo   = InMemoryRepository()
        self.amenity_repo= InMemoryRepository()
        self.place_repo  = InMemoryRepository()
        self.review_repo = InMemoryRepository()


    # ----------  USERS  ----------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
# ------------------------------------------------------------

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
# ------------------------------------------------------------

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

# ------------------------------------------------------------

    def get_all_users(self):
        return self.user_repo.get_all()
    
# ------------------------------------------------------------

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for k in ('first_name', 'last_name', 'email'):
            if k in user_data:
                setattr(user, k, user_data[k])
        self.user_repo.update(user_id, user)
        return user

# ----------  AMENITIES  -----------------------------------

    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError('Name is required')
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity
    
# ------------------------------------------------------------

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
# ------------------------------------------------------------

    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
# ------------------------------------------------------------

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

# ----------  PLACES  ---------------------------------------
  # app/services/facade.py

    def create_place(self, place_data):
        """Create a new place"""
        
        
        if not place_data.get('title'):
            raise ValueError('Title is required')
        if len(place_data['title']) > 100:
            raise ValueError('Title exceeds maximum length of 100')
        
        try:
            price = float(place_data.get('price', 0))
            if price < 0:
                raise ValueError('Price must be a positive number')
        except (TypeError, ValueError):
            raise ValueError('Price must be a positive number')
        
        try:
            latitude = float(place_data.get('latitude', 0))
            if not (-90 < latitude < 90):
                raise ValueError('Latitude must be between -90 and 90')
        except (TypeError, ValueError):
            raise ValueError('Latitude must be a number between -90 and 90')
        
        
        try:
            longitude = float(place_data.get('longitude', 0))
            if not (-180 < longitude < 180):
                raise ValueError('Longitude must be between -180 and 180')
        except (TypeError, ValueError):
            raise ValueError('Longitude must be a number between -180 and 180')
        
        
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError('Owner ID is required')
        
        owner = self.user_repo.get(owner_id)  
        if not owner:
            raise ValueError('Owner not found')
        

        place = Place(
            title=place_data['title'],
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner,  
            description=place_data.get('description')  
        )
        
        self.place_repo.add(place)
        return place
        
    # ------------------------------------------------------------

    def get_place(self, place_id):
            return self.place_repo.get(place_id)
        
    # ------------------------------------------------------------

    def get_all_places(self):
            return self.place_repo.get_all()
    
# ------------------------------------------------------------

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
    # ------------------------------------------------------------
    
    # app/services/facade.py

    def create_review(self, review_data):
        """Create a new review"""
        
        # Validations...
        if not review_data.get('text'):
            raise ValueError('Text is required')
        
        try:
            rating = int(review_data.get('rating', 0))
            if not (1 <= rating <= 5):
                raise ValueError('Rating must be between 1 and 5')
        except (TypeError, ValueError):
            raise ValueError('Rating must be an integer between 1 and 5')
        
        # ✅ RÉCUPÈRE LES OBJETS
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        
        if not user_id:
            raise ValueError('User ID is required')
        if not place_id:
            raise ValueError('Place ID is required')
        
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        
        if not user:
            raise ValueError('User not found')
        if not place:
            raise ValueError('Place not found')
        
        # ✅ PASSE LES OBJETS
        review = Review(
            text=review_data['text'],
            rating=rating,
            place=place,  # ← Objet Place
            user=user     # ← Objet User
        )
        
        self.review_repo.add(review)
        return review
    
    # ------------------------------------------------------------
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    # ------------------------------------------------------------
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    # ------------------------------------------------------------
    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
         # Update text
        if 'text' in review_data:
            if not review_data['text']:
                raise ValueError('Text cannot be empty')
            review.text = review_data['text']
        # Update rating
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not (1 <= rating <= 5):
                    raise ValueError('Rating must be between 1 and 5')
                review.rating = rating
            except (TypeError, ValueError):
                raise ValueError('Rating must be an integer between 1 and 5')
        if 'user_id' in review_data:
            review.user_id = review_data['user_id']
        if 'place_id' in review_data:
            review.place_id = review_data['place_id']
        self.review_repo.update(review_id, review)
        return review
    
    # ------------------------------------------------------------
    def get_reviews_by_place(self, place_id):
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]
        
        
# ------------------------------------------------------------
    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
