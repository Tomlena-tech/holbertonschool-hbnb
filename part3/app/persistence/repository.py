from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class defining the repository interface."""

    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object with new data."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value."""
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation using a dictionary."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add object to in-memory storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve object from in-memory storage by ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects from in-memory storage."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update object in in-memory storage."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete object from in-memory storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Find first object matching attribute value."""
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None,
        )


class SQLAlchemyRepository(Repository):
    """
    Database repository implementation using SQLAlchemy ORM.

    This repository provides persistent storage using SQLAlchemy,
    supporting various database backends (SQLite, MySQL, PostgreSQL).
    """

    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model class.

        Args:
            model: SQLAlchemy model class (e.g., User, Place, Review)
        """
        self.model = model

    def add(self, obj):
        """
        Add a new object to the database.

        Args:
            obj: Model instance to persist

        Raises:
            SQLAlchemyError: If database operation fails
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id: Primary key of the object

        Returns:
            Model instance or None if not found
        """
        return db.session.get(self.model, obj_id)

    def get_all(self):
        """
        Retrieve all objects of this model type.

        Returns:
            List of all model instances
        """
        return db.session.query(self.model).all()

    def update(self, obj_id, data):
        """
        Update an object with new data.

        Args:
            obj_id: Primary key of the object
            data: Dictionary of attributes to update

        Raises:
            SQLAlchemyError: If database operation fails
        """
        obj = self.get(obj_id)
        if obj:
            # Call the model's update method
            # (handles special cases like password hashing)
            obj.update(data)
            db.session.commit()

    def delete(self, obj_id):
        """
        Delete an object from the database.

        Args:
            obj_id: Primary key of the object

        Raises:
            SQLAlchemyError: If database operation fails
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Find first object matching a specific attribute value.

        Args:
            attr_name: Name of the attribute to search
            attr_value: Value to match

        Returns:
            Model instance or None if not found
        """
        return db.session.query(self.model).filter(
            getattr(self.model, attr_name) == attr_value
        ).first()
