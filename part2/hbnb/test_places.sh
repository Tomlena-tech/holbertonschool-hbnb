#!/usr/bin/env python3
"""Complete test suite for Places API endpoints"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from app import create_app
from app.models.user import User


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def test_places_api():
    """Test all Places API endpoints"""
    print_section("TESTING PLACES API ENDPOINTS")
    
    # Clear emails for clean testing
    User.emails.clear()
    
    # Create Flask test client
    app = create_app()
    client = app.test_client()
    
    # ==================== SETUP: Create Users and Amenities ====================
    print("\n📋 SETUP: Creating test data...")
    
    # Create owner user
    owner_response = client.post(
        '/api/v1/users/',
        data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'owner@test.com'
        }),
        content_type='application/json'
    )
    assert owner_response.status_code == 201, f"Failed to create owner: {owner_response.data}"
    owner_data = json.loads(owner_response.data)
    owner_id = owner_data['id']
    print(f"   ✓ Owner created: {owner_id}")
    
    # Create amenities
    wifi_response = client.post(
        '/api/v1/amenities/',
        data=json.dumps({'name': 'WiFi'}),
        content_type='application/json'
    )
    assert wifi_response.status_code == 201, f"Failed to create WiFi: {wifi_response.data}"
    wifi_data = json.loads(wifi_response.data)
    wifi_id = wifi_data['id']
    print(f"   ✓ WiFi amenity created: {wifi_id}")
    
    pool_response = client.post(
        '/api/v1/amenities/',
        data=json.dumps({'name': 'Pool'}),
        content_type='application/json'
    )
    assert pool_response.status_code == 201, f"Failed to create Pool: {pool_response.data}"
    pool_data = json.loads(pool_response.data)
    pool_id = pool_data['id']
    print(f"   ✓ Pool amenity created: {pool_id}")
    
    # ==================== TEST 1: POST - Create Place (SUCCESS) ====================
    print_section("TEST 1: POST /api/v1/places/ - Create Place (SUCCESS)")
    
    place_payload = {
        'title': 'Beach House',
        'description': 'Beautiful beach house with ocean view',
        'price': 150.0,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': owner_id,
        'amenities': [wifi_id, pool_id]
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(place_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.data.decode()}")
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"
    data = json.loads(response.data)
    
    assert 'id' in data, "Missing 'id' in response"
    assert data['title'] == 'Beach House', "Wrong title"
    assert data['price'] == 150.0, "Wrong price"
    
    place_id = data['id']
    print(f"✅ TEST 1 PASSED")
    print(f"   ID: {place_id}")
    print(f"   Title: {data['title']}")
    print(f"   Price: ${data['price']}")
    
    # ==================== TEST 2: POST - Missing Required Fields (400) ====================
    print_section("TEST 2: POST /api/v1/places/ - Missing Fields (400)")
    
    invalid_payload = {
        'title': 'Incomplete House'
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(invalid_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ TEST 2 PASSED - Missing fields rejected correctly")
    
    # ==================== TEST 3: POST - Invalid Owner (404) ====================
    print_section("TEST 3: POST /api/v1/places/ - Invalid Owner (404)")
    
    invalid_owner_payload = {
        'title': 'No Owner House',
        'description': 'House without valid owner',
        'price': 100.0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': 'invalid-owner-id-12345',
        'amenities': []
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(invalid_owner_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Missing error message"
    print(f"✅ TEST 3 PASSED - Invalid owner rejected: {data['error']}")
    
    # ==================== TEST 4: POST - Invalid Amenity (404) ====================
    print_section("TEST 4: POST /api/v1/places/ - Invalid Amenity (404)")
    
    invalid_amenity_payload = {
        'title': 'Invalid Amenity House',
        'description': 'House with invalid amenity',
        'price': 100.0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': owner_id,
        'amenities': ['invalid-amenity-id-12345']
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(invalid_amenity_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Missing error message"
    print(f"✅ TEST 4 PASSED - Invalid amenity rejected: {data['error']}")
    
    # ==================== TEST 5: POST - Invalid Price (400) ====================
    print_section("TEST 5: POST /api/v1/places/ - Invalid Price (400)")
    
    invalid_price_payload = {
        'title': 'Free House',
        'description': 'House with zero price',
        'price': 0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': owner_id,
        'amenities': []
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(invalid_price_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ TEST 5 PASSED - Invalid price (0) rejected")
    
    # ==================== TEST 6: POST - Invalid Coordinates (400) ====================
    print_section("TEST 6: POST /api/v1/places/ - Invalid Coordinates (400)")
    
    invalid_coords_payload = {
        'title': 'Invalid Location House',
        'description': 'House with invalid coordinates',
        'price': 100.0,
        'latitude': 95.0,
        'longitude': -118.0,
        'owner_id': owner_id,
        'amenities': []
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(invalid_coords_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ TEST 6 PASSED - Invalid latitude (95) rejected")
    
    # ==================== TEST 7: GET - Retrieve All Places (200) ====================
    print_section("TEST 7: GET /api/v1/places/ - List All Places (200)")
    
    # Create another place
    place2_payload = {
        'title': 'Mountain Cabin',
        'description': 'Cozy cabin in the mountains',
        'price': 120.0,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'owner_id': owner_id,
        'amenities': [wifi_id]
    }
    
    client.post(
        '/api/v1/places/',
        data=json.dumps(place2_payload),
        content_type='application/json'
    )
    
    response = client.get('/api/v1/places/')
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 2, f"Expected at least 2 places, got {len(data)}"
    print(f"✅ TEST 7 PASSED - Retrieved {len(data)} places")
    
    for place in data:
        print(f"   - {place['title']}: ${place['price']}")
    
    # ==================== TEST 8: GET - Retrieve Place by ID (200) ====================
    print_section("TEST 8: GET /api/v1/places/<place_id> - Get by ID (200)")
    
    response = client.get(f'/api/v1/places/{place_id}')
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    assert data['id'] == place_id, "Wrong place ID"
    assert data['title'] == 'Beach House', "Wrong title"
    
    print(f"✅ TEST 8 PASSED")
    print(f"   Title: {data['title']}")
    print(f"   Price: ${data['price']}")
    
    # ==================== TEST 9: GET - Place Not Found (404) ====================
    print_section("TEST 9: GET /api/v1/places/<place_id> - Not Found (404)")
    
    response = client.get('/api/v1/places/invalid-place-id-12345')
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Missing error message"
    print(f"✅ TEST 9 PASSED - Place not found handled: {data['error']}")
    
    # ==================== TEST 10: PUT - Update Place (200) ====================
    print_section("TEST 10: PUT /api/v1/places/<place_id> - Update (200)")
    
    update_payload = {
        'title': 'Luxury Beach House',
        'description': 'Updated luxury beach house',
        'price': 200.0,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': owner_id,
        'amenities': [wifi_id]
    }
    
    response = client.put(
        f'/api/v1/places/{place_id}',
        data=json.dumps(update_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = json.loads(response.data)
    
    assert data['title'] == 'Luxury Beach House', "Title not updated"
    assert data['price'] == 200.0, "Price not updated"
    
    print(f"✅ TEST 10 PASSED")
    print(f"   New title: {data['title']}")
    print(f"   New price: ${data['price']}")
    
    # ==================== TEST 11: PUT - Update with Invalid Owner (404) ====================
    print_section("TEST 11: PUT /api/v1/places/<place_id> - Invalid Owner (404)")
    
    invalid_update_payload = {
        'title': 'Beach House',
        'description': 'Beach house',
        'price': 150.0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': 'invalid-owner-id-12345',
        'amenities': []
    }
    
    response = client.put(
        f'/api/v1/places/{place_id}',
        data=json.dumps(invalid_update_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Missing error message"
    print(f"✅ TEST 11 PASSED - Invalid owner in update rejected: {data['error']}")
    
    # ==================== TEST 12: PUT - Update Non-Existent Place (404) ====================
    print_section("TEST 12: PUT /api/v1/places/<place_id> - Place Not Found (404)")
    
    response = client.put(
        '/api/v1/places/invalid-place-id-12345',
        data=json.dumps(update_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = json.loads(response.data)
    assert 'error' in data, "Missing error message"
    print(f"✅ TEST 12 PASSED - Update non-existent place rejected: {data['error']}")
    
    # ==================== TEST 13: PUT - Invalid Price (400) ====================
    print_section("TEST 13: PUT /api/v1/places/<place_id> - Invalid Price (400)")
    
    invalid_price_update = {
        'title': 'Beach House',
        'description': 'Beach house',
        'price': -50.0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': owner_id,
        'amenities': []
    }
    
    response = client.put(
        f'/api/v1/places/{place_id}',
        data=json.dumps(invalid_price_update),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ TEST 13 PASSED - Invalid price in update rejected")
    
    # ==================== TEST 14: Empty Title (400) ====================
    print_section("TEST 14: POST /api/v1/places/ - Empty Title (400)")
    
    empty_title_payload = {
        'title': '',
        'description': 'House',
        'price': 100.0,
        'latitude': 34.0,
        'longitude': -118.0,
        'owner_id': owner_id,
        'amenities': []
    }
    
    response = client.post(
        '/api/v1/places/',
        data=json.dumps(empty_title_payload),
        content_type='application/json'
    )
    
    print(f"   Status Code: {response.status_code}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("✅ TEST 14 PASSED - Empty title rejected")
    
    print_section("✅ ALL 14 TESTS PASSED! 🎉")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  PLACES API - COMPLETE TEST SUITE")
    print("  14 Tests Total")
    print("="*70)
    
    try:
        result = test_places_api()
        if result:
            print("\n" + "="*70)
            print("  🎉 SUCCESS: All Places API tests passed!")
            print("="*70 + "\n")
            return 0
        else:
            print("\n" + "="*70)
            print("  ❌ FAILURE: Some tests failed")
            print("="*70 + "\n")
            return 1
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        User.emails.clear()


if __name__ == "__main__":
    sys.exit(main())
