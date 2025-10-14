#!/usr/bin/python3
"""User - entité métier"""
from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, *, email: str, password_hash: str,
                 first_name: str, last_name: str, is_admin: bool = False):
        super().__init__()
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def authenticate(self, email: str, pwd: str) -> "User | None":
        return self if self.email == email and self.password_hash == pwd else None

    def update_profile(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self, k) and k not in {"id", "created_at", "updated_at"}:
                setattr(self, k, v)
        self.save()

    def add_place(self, place: "Place") -> None:
        if place not in self._owned_places:
            self._owned_places.append(place)

    def remove_place(self, place: "Place") -> None:
        try:
            self._owned_places.remove(place)
        except ValueError:
            pass

  
