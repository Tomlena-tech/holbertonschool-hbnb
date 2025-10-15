from app.persistence.repository import InMemoryRepository
from app.models.user import User
from datetime import datetime

from app.models.place import Place
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    # ------ CRUD USER ------
    def create_user(self, data: dict) -> User:
        user = User(**data)          
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict) -> User | None:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        # ton repo possède .update(data) → on l’utilise
        self.user_repo.update(user_id, data)
        user.updated_at = datetime.utcnow()
        return user
    
    def __init__(self):
        self.place_repo = InMemoryRepository() 
    # ------ CRUD PLACE ------       
    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self) -> list[Place]:
        """Retourne toutes les places (objets)."""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        pass
    
    def create_place(self, place_data: dict) -> Place:
    #Crée une place (validation auto via setters).
        place = Place(
        title=place_data["title"],
        price=place_data["price"],
        latitude=place_data["latitude"],
        longitude=place_data["longitude"],
        owner_id=place_data["owner_id"],
        description=place_data.get("description", ""),
        amenities=place_data.get("amenities", [])
    )
        self.place_repo.add(place)
        return place
    
    
