from datetime import datetime
from part2.hbnb.app.models.user import User
from part2.hbnb.app.persistence.repository import InMemoryRepository 

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()


    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update a user by ID with the provided data."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        self.user_repo.save(user)
        return user
