from app.persistence.repository import InMemoryRepository
from app.models.user import User
from datetime import datetime

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
    