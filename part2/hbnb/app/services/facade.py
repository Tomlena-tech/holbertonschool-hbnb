from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place 

class HBnBFacade:
    """Facade for HBnB application operations."""
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # ============================================
    # USER METHODS
    # ============================================
    
    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        
        self.user_repo.update(user_id, user)
        return user

    # ============================================
    # AMENITY METHODS
    # ============================================
    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        if not amenity_data.get('name'):
            raise ValueError('Name is required')
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        self.amenity_repo.update(amenity_id, amenity)
        return amenity
    # ============================================
    # PLACE METHODS
    # ============================================
    
    def create_place(self, place_data):
        """Create a new place with validation"""
        # Validation du title
        if not place_data.get('title'):
            raise ValueError('Title is required')
        
        # Validation du price
        if 'price' not in place_data:
            raise ValueError('Price is required')
        try:
            price = float(place_data['price'])
            if price <= 0:
                raise ValueError('Price must be positive')
        except (TypeError, ValueError):
            raise ValueError('Price must be a positive number')
        
        # Validation de latitude
        if 'latitude' not in place_data:
            raise ValueError('Latitude is required')
        try:
            latitude = float(place_data['latitude'])
            if not (-90.0 < latitude < 90.0):
                raise ValueError('Latitude must be between -90 and 90')
        except (TypeError, ValueError):
            raise ValueError('Latitude must be a number between -90 and 90')
        
        # Validation de longitude
        if 'longitude' not in place_data:
            raise ValueError('Longitude is required')
        try:
            longitude = float(place_data['longitude'])
            if not (-180.0 < longitude < 180.0):
                raise ValueError('Longitude must be between -180 and 180')
        except (TypeError, ValueError):
            raise ValueError('Longitude must be a number between -180 and 180')
        
        # Validation de owner_id
        if not place_data.get('owner_id'):
            raise ValueError('Owner ID is required')
        
        # Créer le place
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
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place with validation"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Validation et mise à jour du title
        if 'title' in place_data:
            if not place_data['title']:
                raise ValueError('Title cannot be empty')
            place.title = place_data['title']
        
        # Validation et mise à jour du description
        if 'description' in place_data:
            place.description = place_data['description']
        
        # Validation et mise à jour du price
        if 'price' in place_data:
            try:
                price = float(place_data['price'])
                if price <= 0:
                    raise ValueError('Price must be positive')
                place.price = price
            except (TypeError, ValueError):
                raise ValueError('Price must be a positive number')
        
        # Validation et mise à jour de latitude
        if 'latitude' in place_data:
            try:
                latitude = float(place_data['latitude'])
                if not (-90.0 < latitude < 90.0):
                    raise ValueError('Latitude must be between -90 and 90')
                place.latitude = latitude
            except (TypeError, ValueError):
                raise ValueError('Latitude must be a number between -90 and 90')
        
        # Validation et mise à jour de longitude
        if 'longitude' in place_data:
            try:
                longitude = float(place_data['longitude'])
                if not (-180.0 < longitude < 180.0):
                    raise ValueError('Longitude must be between -180 and 180')
                place.longitude = longitude
            except (TypeError, ValueError):
                raise ValueError('Longitude must be a number between -180 and 180')
        
        # Mise à jour de owner_id
        if 'owner_id' in place_data:
            place.owner_id = place_data['owner_id']
        
        # Mise à jour des amenities
        if 'amenities' in place_data:
            place.amenities = place_data['amenities']
        
        self.place_repo.update(place_id, place)
        return place   
