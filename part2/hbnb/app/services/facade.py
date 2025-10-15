from datetime import datetime
from app.models.user import User
from part2.hbnb.app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository[User]()

    # ------ CRUD USER ------
    def create_user(self, data: dict) -> User:
        user = User(**data)          # ton __init__ fait toute la validation
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> list[User]:
        return self.user_repo.list()

    def update_user(self, user_id: str, data: dict) -> User | None:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        # on autorise uniquement les champs publics
        for key in ('first_name', 'last_name', 'email'):
            if key in data:
                setattr(user, key, data[key])
        user.updated_at = datetime.utcnow()
        # pas besoin de .save() : objet déjà dans le dict
        return user
