from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity 

class HBnBFacade:
    """Facade for HBnB application operations."""
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError('Name is required')
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity  

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get_all(amenity_id)

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
        return None
    
    