from .base_model import BaseModel
from .user import User


class Place(BaseModel):
    """
    Represents a place / accommodation.

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
        self.owner = owner

        # Relationship containers
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """str: The title of the place (<= 100 characters)."""
        return self.__title

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
        self.__title = value

    @property
    def description(self):
        """str: Long-form description of the place."""
        return self.__description

    @description.setter
    def description(self, value):
        """
        Validate and set the description.
        """
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string")
        self.__description = value

    @property
    def price(self):
        """float: Price per night (non-negative)."""
        return self.__price

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
        self.__price = float(value)

    @property
    def latitude(self):
        """float: Latitude coordinate (-90.0, 90.0 exclusive)."""
        return self.__latitude

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
        self.__latitude = float(value)

    @property
    def longitude(self):
        """float: Longitude coordinate (-180.0, 180.0 exclusive)."""
        return self.__longitude

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
        self.__longitude = float(value)

    @property
    def owner(self):
        """User: Owner of the place (must be a User instance)."""
        return self.__owner

    @owner.setter
    def owner(self, value):
        """
        Validate and set owner.

        Raises:
            TypeError: if value is not a User instance.
        """
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
        self.__owner = value

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
            'owner_id': self.owner.id
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
