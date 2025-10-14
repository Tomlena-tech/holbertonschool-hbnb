#!/usr/bin/python3
"""Complete test suite for all HBnB models"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_base_model():
    """Test BaseModel functionality"""
    print_section("TESTING BASE MODEL")
    try:
        user = User(first_name="John", last_name="Doe", email="john@test.com")
        
        # Test base attributes
        assert hasattr(user, 'id'), "❌ Missing id"
        assert hasattr(user, 'created_at'), "❌ Missing created_at"
        assert hasattr(user, 'updated_at'), "❌ Missing updated_at"
        print("✅ Base attributes present")
        
        # Test to_dict()
        user_dict = user.to_dict()
        assert 'id' in user_dict, "❌ id not in to_dict()"
        assert 'first_name' in user_dict, "❌ first_name not in to_dict()"
        assert 'created_at' in user_dict, "❌ created_at not in to_dict()"
        print("✅ to_dict() works correctly")
        
        # Test save()
        old_updated = user.updated_at
        import time
        time.sleep(0.01)
        user.save()
        assert user.updated_at != old_updated, "❌ save() doesn't update timestamp"
        print("✅ save() updates timestamp")
        
        # Test update()
        user.update({'first_name': 'Jane'})
        assert user.first_name == 'Jane', "❌ update() doesn't work"
        print("✅ update() works correctly")
        
        print("✅ BASE MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ BASE MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user():
    """Test User model"""
    print_section("TESTING USER MODEL")
    try:
        # Valid creation
        user = User(first_name="John", last_name="Doe", email="john@test.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@test.com"
        assert user.is_admin == False
        assert isinstance(user.places, list)
        print("✅ Valid user creation")
        
        # Admin user
        admin = User(first_name="Admin", last_name="User", 
                    email="admin@test.com", is_admin=True)
        assert admin.is_admin == True
        print("✅ Admin user creation")
        
        # Test first_name validations
        try:
            User(first_name="", last_name="Doe", email="john@test.com")
            print("❌ Empty first_name accepted")
            return False
        except ValueError:
            print("✅ Empty first_name rejected")
        
        try:
            User(first_name="a"*51, last_name="Doe", email="john@test.com")
            print("❌ Long first_name (>50) accepted")
            return False
        except ValueError:
            print("✅ Long first_name rejected")
        
        # Test last_name validations
        try:
            User(first_name="John", last_name="", email="john@test.com")
            print("❌ Empty last_name accepted")
            return False
        except ValueError:
            print("✅ Empty last_name rejected")
        
        try:
            User(first_name="John", last_name="a"*51, email="john@test.com")
            print("❌ Long last_name (>50) accepted")
            return False
        except ValueError:
            print("✅ Long last_name rejected")
        
        # Test email validations
        try:
            User(first_name="John", last_name="Doe", email="")
            print("❌ Empty email accepted")
            return False
        except ValueError:
            print("✅ Empty email rejected")
        
        try:
            User(first_name="John", last_name="Doe", email="invalid@")
            print("❌ Invalid email (no domain) accepted")
            return False
        except ValueError:
            print("✅ Invalid email rejected")
        
        try:
            User(first_name="John", last_name="Doe", email="invalid.com")
            print("❌ Invalid email (no @) accepted")
            return False
        except ValueError:
            print("✅ Invalid email (no @) rejected")
        
        # Test to_dict includes places (not _owned_places)
        user_dict = user.to_dict()
        assert 'places' in user_dict, "❌ 'places' not in to_dict()"
        assert '_owned_places' not in user_dict, "❌ '_owned_places' in to_dict()"
        print("✅ to_dict() has 'places' (not '_owned_places')")
        
        print("✅ USER MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ USER MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_place():
    """Test Place model"""
    print_section("TESTING PLACE MODEL")
    try:
        owner = User(first_name="John", last_name="Doe", email="john@test.com")
        
        # Valid creation
        place = Place(
            title="Beach House",
            description="Nice beach house",
            price=100.0,
            latitude=34.0,
            longitude=-118.0,
            owner=owner
        )
        assert place.title == "Beach House"
        assert place.price == 100.0
        assert place.owner == owner
        print("✅ Valid place creation")
        
        # Test bidirectional relationship
        assert place in owner.places, "❌ Place not added to owner.places"
        print("✅ Bidirectional relationship works")
        
        # Test title validations
        try:
            Place(title="", description="Nice", price=100.0,
                  latitude=34.0, longitude=-118.0, owner=owner)
            print("❌ Empty title accepted")
            return False
        except ValueError:
            print("✅ Empty title rejected")
        
        try:
            Place(title="a"*101, description="Nice", price=100.0,
                  latitude=34.0, longitude=-118.0, owner=owner)
            print("❌ Long title (>100) accepted")
            return False
        except ValueError:
            print("✅ Long title rejected")
        
        # Test price validations
        try:
            Place(title="House", description="Nice", price=0,
                  latitude=34.0, longitude=-118.0, owner=owner)
            print("❌ Zero price accepted")
            return False
        except ValueError:
            print("✅ Zero price rejected")
        
        try:
            Place(title="House", description="Nice", price=-50.0,
                  latitude=34.0, longitude=-118.0, owner=owner)
            print("❌ Negative price accepted")
            return False
        except ValueError:
            print("✅ Negative price rejected")
        
        # Test latitude validations
        try:
            Place(title="House", description="Nice", price=100.0,
                  latitude=-91.0, longitude=-118.0, owner=owner)
            print("❌ Invalid latitude (<-90) accepted")
            return False
        except ValueError:
            print("✅ Invalid latitude (<-90) rejected")
        
        try:
            Place(title="House", description="Nice", price=100.0,
                  latitude=91.0, longitude=-118.0, owner=owner)
            print("❌ Invalid latitude (>90) accepted")
            return False
        except ValueError:
            print("✅ Invalid latitude (>90) rejected")
        
        # Test longitude validations
        try:
            Place(title="House", description="Nice", price=100.0,
                  latitude=34.0, longitude=-181.0, owner=owner)
            print("❌ Invalid longitude (<-180) accepted")
            return False
        except ValueError:
            print("✅ Invalid longitude (<-180) rejected")
        
        try:
            Place(title="House", description="Nice", price=100.0,
                  latitude=34.0, longitude=181.0, owner=owner)
            print("❌ Invalid longitude (>180) accepted")
            return False
        except ValueError:
            print("✅ Invalid longitude (>180) rejected")
        
        # Test empty description allowed
        place2 = Place(title="House2", description="", price=100.0,
                      latitude=34.0, longitude=-118.0, owner=owner)
        assert place2.description == "", "❌ Empty description not handled"
        print("✅ Empty description allowed")
        
        # Test average_rating
        assert place.average_rating() == 0.0, "❌ average_rating() with no reviews"
        print("✅ average_rating() returns 0.0 with no reviews")
        
        # Test is_available
        assert place.is_available("2025-10-20", "2025-10-25") == True
        print("✅ is_available() works")
        
        print("✅ PLACE MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ PLACE MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_amenity():
    """Test Amenity model"""
    print_section("TESTING AMENITY MODEL")
    try:
        # Valid creation
        amenity = Amenity(name="WiFi")
        assert amenity.name == "WiFi"
        print("✅ Valid amenity creation")
        
        # Test name validations
        try:
            Amenity(name="")
            print("❌ Empty name accepted")
            return False
        except ValueError:
            print("✅ Empty name rejected")
        
        try:
            Amenity(name="a"*51)
            print("❌ Long name (>50) accepted")
            return False
        except ValueError:
            print("✅ Long name rejected")
        
        # Test to_dict
        amenity_dict = amenity.to_dict()
        assert 'name' in amenity_dict
        assert 'id' in amenity_dict
        print("✅ to_dict() works")
        
        print("✅ AMENITY MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ AMENITY MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_review():
    """Test Review model"""
    print_section("TESTING REVIEW MODEL")
    try:
        user = User(first_name="John", last_name="Doe", email="john@test.com")
        place = Place(
            title="Beach House",
            description="Nice",
            price=100.0,
            latitude=34.0,
            longitude=-118.0,
            owner=user
        )
        
        # Valid creation
        review = Review(
            text="Great place!",
            rating=5,
            place=place,
            user=user
        )
        assert review.text == "Great place!"
        assert review.rating == 5
        assert review.place == place
        assert review.user == user
        print("✅ Valid review creation")
        
        # Test bidirectional relationship
        assert review in place.reviews, "❌ Review not added to place.reviews"
        print("✅ Bidirectional relationship works")
        
        # Test text validations
        try:
            Review(text="", rating=5, place=place, user=user)
            print("❌ Empty text accepted")
            return False
        except ValueError:
            print("✅ Empty text rejected")
        
        try:
            Review(text="   ", rating=5, place=place, user=user)
            print("❌ Whitespace-only text accepted")
            return False
        except ValueError:
            print("✅ Whitespace-only text rejected")
        
        # Test rating validations
        try:
            Review(text="Good", rating=4.5, place=place, user=user)
            print("❌ Float rating accepted")
            return False
        except ValueError:
            print("✅ Float rating rejected")
        
        try:
            Review(text="Bad", rating=0, place=place, user=user)
            print("❌ Rating 0 accepted")
            return False
        except ValueError:
            print("✅ Rating 0 rejected")
        
        try:
            Review(text="Too good", rating=6, place=place, user=user)
            print("❌ Rating 6 accepted")
            return False
        except ValueError:
            print("✅ Rating 6 rejected")
        
        # Test all valid ratings (1-5)
        for rating in range(1, 6):
            r = Review(text=f"Rating {rating}", rating=rating, 
                      place=place, user=user)
            assert r.rating == rating
        print("✅ All valid ratings (1-5) work")
        
        # Test average_rating calculation
        assert place.average_rating() > 0, "❌ average_rating calculation"
        print(f"✅ average_rating() calculates correctly: {place.average_rating()}")
        
        print("✅ REVIEW MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ REVIEW MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between all models"""
    print_section("TESTING INTEGRATION")
    try:
        # Create full scenario
        user = User(first_name="John", last_name="Doe", email="john@test.com")
        
        place = Place(
            title="Beach House",
            description="Beautiful beach house",
            price=150.0,
            latitude=34.0,
            longitude=-118.0,
            owner=user
        )
        
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Pool")
        place.add_amenity(wifi)
        place.add_amenity(pool)
        
        review1 = Review(text="Amazing!", rating=5, place=place, user=user)
        review2 = Review(text="Good", rating=4, place=place, user=user)
        
        # Test relationships
        assert len(user.places) == 1, "❌ User should have 1 place"
        assert len(place.reviews) == 2, "❌ Place should have 2 reviews"
        assert len(place.amenities) == 2, "❌ Place should have 2 amenities"
        print("✅ All relationships work")
        
        # Test average rating
        avg = place.average_rating()
        expected = 4.5
        assert avg == expected, f"❌ Average rating should be {expected}, got {avg}"
        print(f"✅ Average rating calculated correctly: {avg}")
        
        # Test to_dict() with relationships
        place_dict = place.to_dict()
        assert 'owner' in place_dict, "❌ owner not in place to_dict()"
        assert place_dict['owner'] == user.id, "❌ owner should be user.id"
        print("✅ to_dict() handles owner relationship")
        
        assert 'reviews' in place_dict, "❌ reviews not in place to_dict()"
        assert len(place_dict['reviews']) == 2, "❌ Should have 2 review ids"
        print("✅ to_dict() handles reviews relationship")
        
        assert 'amenities' in place_dict, "❌ amenities not in place to_dict()"
        assert len(place_dict['amenities']) == 2, "❌ Should have 2 amenity ids"
        print("✅ to_dict() handles amenities relationship")
        
        print("✅ INTEGRATION: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"❌ INTEGRATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  HBnB MODELS - COMPLETE TEST SUITE")
    print("="*60)
    
    results = {
        "BaseModel": test_base_model(),
        "User": test_user(),
        "Place": test_place(),
        "Amenity": test_amenity(),
        "Review": test_review(),
        "Integration": test_integration()
    }
    
    # Final report
    print_section("FINAL REPORT")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for model, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{model:20} {status}")
    
    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} tests passed")
    print('='*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your models are ready for Holberton checker! 🎉\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
