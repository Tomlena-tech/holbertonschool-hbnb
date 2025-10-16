from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity 

class HBnBFacade:
    """Facade for HBnB application operations."""
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
    