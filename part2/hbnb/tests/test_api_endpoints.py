import unittest
import time
from app import create_app
from app.models.user import User


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User endpoints"""

    @classmethod
    def setUpClass(cls):
        """Clear User emails before running tests"""
        User.emails.clear()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.timestamp = str(int(time.time() * 1000))

    def test_create_user(self):
        """Test creating a user with valid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f"jane.doe{self.timestamp}@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email"""
        email = f"duplicate{self.timestamp}@example.com"
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": email
        })
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": email
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.user{self.timestamp}@example.com"
        })
        user_id = create_response.get_json()['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user"""
        email = f"original{self.timestamp}@example.com"
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Original",
            "last_name": "Name",
            "email": email
        })
        user_id = create_response.get_json()['id']
        
        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated",
            "last_name": "Name",
            "email": email
        })
        self.assertEqual(response.status_code, 200)


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity endpoints"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating an amenity"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Swimming Pool')

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_amenity_by_id(self):
        """Test retrieving an amenity by ID"""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Gym"
        })
        amenity_id = create_response.get_json()['id']
        
        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_amenity(self):
        """Test updating an amenity"""
        # Create an amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Original Amenity"
        })
        amenity_id = create_response.get_json()['id']
        
        # Update the amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Updated Amenity"
        })
        self.assertEqual(response.status_code, 200)


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place endpoints"""

    @classmethod
    def setUpClass(cls):
        """Clear User emails before running tests"""
        User.emails.clear()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.timestamp = str(int(time.time() * 1000))
        # Create a user to be the owner
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": f"owner{self.timestamp}@example.com"
        })
        self.owner_id = user_response.get_json()['id']

    def test_create_place(self):
        """Test creating a place"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Apartment",
            "description": "A lovely place to stay",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Apartment')

    def test_create_place_invalid_owner(self):
        """Test creating a place with non-existent owner"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Test",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "nonexistent-id",
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a place by ID"""
        # Create a place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Test",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id,
            "amenities": []
        })
        place_id = create_response.get_json()['id']
        
        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('owner', data)
        self.assertIn('amenities', data)


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review endpoints"""

    @classmethod
    def setUpClass(cls):
        """Clear User emails before running tests"""
        User.emails.clear()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.timestamp = str(int(time.time() * 1000))
        # Create a user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": f"reviewer{self.timestamp}@example.com"
        })
        self.user_id = user_response.get_json()['id']
        
        # Create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Place to Review",
            "description": "Test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.place_id = place_response.get_json()['id']

    def test_create_review(self):
        """Test creating a review"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_user(self):
        """Test creating a review with non-existent user"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Test review",
            "rating": 4,
            "user_id": "nonexistent-id",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieving a review by ID"""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Test review",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']
        
        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_review(self):
        """Test updating a review"""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Original review",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']
        
        # Update the review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Test deleting a review"""
        # Create a review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Review to delete",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']
        
        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test retrieving all reviews for a specific place"""
        # Create a review
        self.client.post('/api/v1/reviews/', json={
            "text": "Review for place",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        
        # Get reviews for the place
        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()
