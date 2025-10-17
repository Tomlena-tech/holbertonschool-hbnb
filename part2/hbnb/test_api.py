"""
Unit Tests for HBnB Evolution API
Tests all endpoints with positive and negative test cases
"""

import unittest
import json
from app import create_app
from app.persistence.repository import InMemoryRepository


class TestHBnBAPI(unittest.TestCase):
    """Test suite for HBnB API endpoints"""

    def setUp(self):
        """Set up test client and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Clear repository before each test
        InMemoryRepository._storage.clear()
        
        # Test data
        self.valid_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        
        self.valid_amenity = {
            "name": "WiFi"
        }
        
    def tearDown(self):
        """Clean up after each test"""
        InMemoryRepository._storage.clear()

    # ==========================================
    # USER ENDPOINT TESTS
    # ==========================================
    
    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertIn('id', data)

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        invalid_user = self.valid_user.copy()
        invalid_user['email'] = 'invalid-email'
        
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields"""
        incomplete_user = {"first_name": "John"}
        
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(incomplete_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create a user first
        self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by ID"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        """Test successful user update"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        
        # Update the user
        update_data = {"first_name": "Jane", "last_name": "Smith"}
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_update_user_invalid_email(self):
        """Test user update with invalid email"""
        # Create a user
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(create_response.data)['id']
        
        # Try to update with invalid email
        update_data = {"email": "invalid-email"}
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    # ==========================================
    # AMENITY ENDPOINT TESTS
    # ==========================================
    
    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.valid_amenity),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')
        self.assertIn('id', data)

    def test_create_amenity_missing_name(self):
        """Test amenity creation without name"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create an amenity first
        self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.valid_amenity),
            content_type='application/json'
        )
        
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_amenity_by_id(self):
        """Test retrieving a specific amenity by ID"""
        # Create an amenity
        create_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.valid_amenity),
            content_type='application/json'
        )
        amenity_id = json.loads(create_response.data)['id']
        
        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)

    def test_update_amenity_success(self):
        """Test successful amenity update"""
        # Create an amenity
        create_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.valid_amenity),
            content_type='application/json'
        )
        amenity_id = json.loads(create_response.data)['id']
        
        # Update the amenity
        update_data = {"name": "Swimming Pool"}
        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Swimming Pool')

    # ==========================================
    # PLACE ENDPOINT TESTS
    # ==========================================
    
    def test_create_place_success(self):
        """Test successful place creation"""
        # Create owner first
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        # Create place
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Cozy Apartment')
        self.assertEqual(data['price'], 100.0)

    def test_create_place_negative_price(self):
        """Test place creation with negative price"""
        # Create owner first
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        # Try to create place with negative price
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": -50.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_coordinates(self):
        """Test place creation with invalid coordinates"""
        # Create owner first
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        # Invalid latitude
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 95.0,  # Invalid: > 90
            "longitude": -122.4194,
            "owner_id": owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a specific place by ID"""
        # Create owner and place
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id
        }
        
        create_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(create_response.data)['id']
        
        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)

    def test_update_place_success(self):
        """Test successful place update"""
        # Create owner and place
        owner_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        owner_id = json.loads(owner_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id
        }
        
        create_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(create_response.data)['id']
        
        # Update the place
        update_data = {"title": "Luxury Apartment", "price": 200.0}
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Luxury Apartment')
        self.assertEqual(data['price'], 200.0)

    # ==========================================
    # REVIEW ENDPOINT TESTS
    # ==========================================
    
    def test_create_review_success(self):
        """Test successful review creation"""
        # Create user and place first
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        # Create review
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        # Create user and place first
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        # Try to create review with invalid rating
        review_data = {
            "text": "Great place!",
            "rating": 6,  # Invalid: > 5
            "user_id": user_id,
            "place_id": place_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID"""
        # Create user, place, and review
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        
        create_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        review_id = json.loads(create_response.data)['id']
        
        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], review_id)

    def test_update_review_success(self):
        """Test successful review update"""
        # Create user, place, and review
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        
        create_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        review_id = json.loads(create_response.data)['id']
        
        # Update the review
        update_data = {"text": "Amazing place!", "rating": 5}
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Amazing place!')

    def test_delete_review_success(self):
        """Test successful review deletion"""
        # Create user, place, and review
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user),
            content_type='application/json'
        )
        user_id = json.loads(user_response.data)['id']
        
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id
        }
        
        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )
        place_id = json.loads(place_response.data)['id']
        
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        
        create_response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )
        review_id = json.loads(create_response.data)['id']
        
        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
