import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        """Set up a new BaseModel instance for testing"""
        self.base_model = BaseModel()

    def test_attributes(self):
        """Test if the BaseModel instance has the correct attributes"""
        self.assertTrue(hasattr(self.base_model, 'id'))
        self.assertTrue(hasattr(self.base_model, 'created_at'))
        self.assertTrue(hasattr(self.base_model, 'updated_at'))
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_unique_id(self):
        """Test if each BaseModel instance has a unique id"""
        another_model = BaseModel()
        self.assertNotEqual(self.base_model.id, another_model.id)


if __name__ == '__main__':
    unittest.main()
