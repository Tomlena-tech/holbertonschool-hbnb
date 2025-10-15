import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel is a base class providing common attributes and methods for all
    data models.

    It provides:
    - Unique identification for each instance (`id`).
    - Automatic tracking of creation and modification timestamps.
    - Utility methods for updating attributes and validating values.
    """
    def __init__(self):
        """
        Initialize a new instance of BaseModel.

        Attributes:
            id (str): A unique UUID string identifying the instance.
            created_at (datetime): The timestamp when the instance was created.
            updated_at (datetime): The timestamp when the instance was last
                modified.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the `updated_at` timestamp to the current datetime.

        This method should be called whenever the object is modified to ensure
        that modification times are tracked accurately.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the instance's attributes based on the provided dictionary.

        Args:
            data (dict): A dictionary containing attribute names and their new
                values (key-value pairs).
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def is_max_length(self, name, value, max_length):
        """
        Validate that the given string value does not exceed a maximum length.

        Args:
            name (str): The name of the attribute being validated
            value (str): The string value to check.
            max_length (int): The maximum allowed length.

        Raises:
            ValueError: If the value's length exceeds the maximum allowed
                length.
        """
        if len(value) > max_length:
            raise ValueError(f"{name} exceeds maximum length of {max_length}")

    def is_in_range(self, name, value, min, max):
        """
        Validate that a numeric value falls within a specified exclusive range.

        Args:
            name (str): The name of the attribute being validated.
            value (float): The numeric value to check.
            min (float): The minimum allowed value (exclusive).
            max (float): The maximum allowed value (exclusive).

        Raises:
            ValueError: If the value is not within the specified range.
        """
        if not (min < value < max):
            raise ValueError(f"{name} must be between {min} and {max}")
