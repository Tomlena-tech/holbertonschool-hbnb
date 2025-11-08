"""
Models package.

This module imports all models to ensure they are registered with SQLAlchemy.
"""

from app.models.user import User

# TODO: Import other models when they are migrated to SQLAlchemy
# from app.models.amenity import Amenity
# from app.models.place import Place
# from app.models.review import Review

__all__ = ['User']
