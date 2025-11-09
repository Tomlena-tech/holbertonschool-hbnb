from .base_model import BaseModel
from .user import User
from app.extensions import db

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """
    Represents a place / accommodation with SQLAlchemy ORM mapping.

    Inherits from:
        BaseModel: provides `id`, `created_at`, `updated_at`, `save()` and
        validation helpers.

    Instance attributes:
        title (str): short title for the place (max 100 characters).
        description (str): longer, free-text description of the place.
        price (float): price per night; must be non-negative.
        latitude (float): geographic latitude, must be within (-90.0, 90.0).
        longitude (float): geographic longitude, must be within
            (-180.0, 180.0).
        owner (User): User instance who owns this
            place.
        reviews (list): list of review objects/identifiers
            related to this place.
        amenities (list): list of amenities related to this place.
    """

    __tablename__ = 'places'

    # SQLAlchemy column mappings
    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.Text, nullable=True)
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)

    # Foreign key for User relationship (one-to-many: User -> Place)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', backref='owned_places', foreign_keys=[owner_id])
    # Note: reviews relationship is defined via backref in Review model
    # amenities relationship for many-to-many
    amenities_rel = db.relationship('Amenity', secondary='place_amenity', backref='places_list', lazy=True)

    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner,
        description=None
    ):
        """
        Initialize a new Place instance.

        Args:
            title (str): Place title (non-empty, <= 100 chars).
            price (float | int): Price for the place (non-negative).
            latitude (float | int): Latitude coordinate.
            longitude (float | int): Longitude coordinate.
            owner (User): Owner of the place; must be a User instance.
            description (str, optional): Optional description text.

        Raises:
            TypeError / ValueError: See individual property setters for
            validation rules.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        # Set owner (SQLAlchemy will handle owner_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")
        self.owner = owner

        # Note: reviews and amenities_rel are managed by SQLAlchemy relationships
        # Keeping amenities for backward compatibility with in-memory list
        self.amenities = []

    @property
    def title(self):
        """str: The title of the place (<= 100 characters)."""
        return self._title

    @title.setter
    def title(self, value):
        """
        Validate and set the title.

        - Must be a non-empty string.
        - Maximum length enforced via BaseModel.is_max_length.
        """
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        self._title = value

    @property
    def description(self):
        """str: Long-form description of the place."""
        return self._description

    @description.setter
    def description(self, value):
        """
        Validate and set the description.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value

    @property
    def price(self):
        """float: Price per night (non-negative)."""
        return self._price

    @price.setter
    def price(self, value):
        """
        Validate and set the price.

        Accepts int or float. Raises TypeError for non-numeric values
        and ValueError for negative prices.
        """
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
        self._price = float(value)

    @property
    def latitude(self):
        """float: Latitude coordinate (-90.0, 90.0 exclusive)."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        Validate and set latitude.

        Must be a float (or convertible to float) and within the exclusive range
        (-90.0, 90.0).
        """
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        super().is_in_range("latitude", value, -90.0, 90.0)
        self._latitude = float(value)

    @property
    def longitude(self):
        """float: Longitude coordinate (-180.0, 180.0 exclusive)."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        Validate and set longitude.

        Must be a float (or convertible to float) and within the exclusive range
        (-180.0, 180.0).
        """
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        super().is_in_range("longitude", value, -180.0, 180.0)
        self._longitude = float(value)


    # --- relationship helpers ---
    def add_review(self, review):
        """Add a review to the place's reviews list."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Remove a review from the place's reviews list."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place's amenities list."""
        self.amenities.append(amenity)

    # --- serialization helpers ---
    def to_dict(self):
        """
        Return a compact dict representation of the place suitable for
        lightweight responses or persistence references.

        The owner is represented by `owner_id` rather than the full owner payload.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }

    def to_dict_list(self):
        """
        Return an expanded dict representation including nested owner data,
        amenities and reviews. Useful for detailed endpoints or UI payloads.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': self.amenities,
            'reviews': self.reviews
        }
