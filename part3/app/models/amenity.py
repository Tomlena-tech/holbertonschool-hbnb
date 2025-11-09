from .base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """
    Amenity model with SQLAlchemy ORM mapping.

    Represents amenities that can be associated with places.
    """

    __tablename__ = 'amenities'

    # SQLAlchemy column mapping
    _name = db.Column('name', db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        super().is_max_length('Name', value, 50)
        self._name = value

    def update(self, data):
        return super().update(data)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
