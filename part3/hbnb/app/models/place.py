from .base_model import BaseModel
from .user import User
from app import db


class Place(BaseModel):
    """
    Represents a place / accommodation.

    Inherits from:
        BaseModel: provides `id`, `created_at`, `updated_at`, `save()` and
        validation helpers.

    SQLAlchemy Columns:
        title (str): short title for the place (max 100 characters).
        description (str): longer, free-text description of the place.
        price (float): price per night; must be non-negative.
        latitude (float): geographic latitude, must be within (-90.0, 90.0).
        longitude (float): geographic longitude, must be within (-180.0, 180.0).
        owner_id (str): UUID of the owner (User) - Foreign key will be added in Task 8

    """
    __tablename__ = 'places'
    
    #SQLAlchemy Columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # owner = créé automatiquement via backref dans User.places
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary='place_amenity', backref='places', lazy='dynamic')


    def __init__(self, title, price, latitude, longitude, owner_id, description=None):

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
        #Validation before assigning
        
        self.validate_title(title)
        self.validate_price(price)
        self.validate_latitude(latitude)
        self.validate_longitude(longitude)
        
        #SQLAlchemy columns
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        

        
    def validate_title(self, value):
        """Validate title."""
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title exceeds maximum length of 100")
        
    def validate_price(self, value):
        """Validate price."""
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price must be positive.")
    
    def validate_latitude(self, value):
        """Validate latitude."""
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be a float")
        if not (-90.0 < value < 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
    
    def validate_longitude(self, value):
        """Validate longitude."""
        if not isinstance(value, (float, int)):
            raise TypeError("Longitude must be a float")
        if not (-180.0 < value < 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
    
    def to_dict(self):
        """
        Return a dict representation of the place.
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
