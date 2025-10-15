#!/usr/bin/python3
"""Complete test suite for all HBnB models with @property validation"""
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
        user = User("John", "Doe", "john@basetest.com")
        
        assert hasattr(user, 'id'), "Missing id"
        assert hasattr(user, 'created_at'), "Missing created_at"
        assert hasattr(user, 'updated_at'), "Missing updated_at"
        print("Base attributes present")
        
        user_dict = user.to_dict()
        assert 'id' in user_dict, "id not in to_dict()"
        assert 'first_name' in user_dict, "first_name not in to_dict()"
        assert 'created_at' in user_dict, "created_at not in to_dict()"
        print("to_dict() works correctly")
        
        old_updated = user.updated_at
        import time
        time.sleep(0.01)
        user.save()
        assert user.updated_at != old_updated, "save() doesn't update timestamp"
        print("save() updates timestamp")
        
        user.update({'first_name': 'Jane'})
        assert user.first_name == 'Jane', "update() doesn't work"
        print("update() works correctly")
        
        print("BASE MODEL: ALL TESTS PASSED")
        User.emails.discard("john@basetest.com")
        return True
        
    except Exception as e:
        print(f"BASE MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_user():
    """Test User model with @property validation"""
    print_section("TESTING USER MODEL")
    try:
        User.emails.clear()
        
        print("\nTest 1: Valid user creation")
        user1 = User("John", "Doe", "john@test.com")
        assert user1.first_name == "John"
        assert user1.last_name == "Doe"
        assert user1.email == "john@test.com"
        assert user1.is_admin == False
        assert isinstance(user1.places, list)
        assert isinstance(user1.reviews, list)
        print("   Valid user created")
        
        print("\nTest 2: Admin user creation")
        admin = User("Admin", "User", "admin@test.com", is_admin=True)
        assert admin.is_admin == True
        print("   Admin user created")
        
        print("\nTest 3: Email uniqueness")
        try:
            user2 = User("Jane", "Doe", "john@test.com")
            print("   FAILED: Duplicate email accepted")
            return False
        except ValueError as e:
            print(f"   Duplicate email rejected: {e}")
        
        print("\nTest 4: Different email")
        user3 = User("Jane", "Smith", "jane@test.com")
        assert user3.email == "jane@test.com"
        print("   Different email accepted")
        
        print("\nTest 5: First name type validation")
        try:
            user4 = User(123, "Doe", "test1@test.com")
            print("   FAILED: Integer first_name accepted")
            return False
        except TypeError as e:
            print(f"   Integer first_name rejected: {e}")
        
        print("\nTest 6: Empty first name")
        try:
            user5 = User("", "Doe", "test2@test.com")
            print("   FAILED: Empty first_name accepted")
            return False
        except ValueError as e:
            print(f"   Empty first_name rejected: {e}")
        
        print("\nTest 7: First name too long")
        try:
            user6 = User("a"*51, "Doe", "test3@test.com")
            print("   FAILED: Long first_name accepted")
            return False
        except ValueError as e:
            print(f"   Long first_name rejected: {e}")
        
        print("\nTest 8: Last name type validation")
        try:
            user7 = User("John", 456, "test4@test.com")
            print("   FAILED: Integer last_name accepted")
            return False
        except TypeError as e:
            print(f"   Integer last_name rejected: {e}")
        
        print("\nTest 9: Empty last name")
        try:
            user8 = User("John", "", "test5@test.com")
            print("   FAILED: Empty last_name accepted")
            return False
        except ValueError as e:
            print(f"   Empty last_name rejected: {e}")
        
        print("\nTest 10: Last name too long")
        try:
            user9 = User("John", "b"*51, "test6@test.com")
            print("   FAILED: Long last_name accepted")
            return False
        except ValueError as e:
            print(f"   Long last_name rejected: {e}")
        
        print("\nTest 11: Email type validation")
        try:
            user10 = User("John", "Doe", 789)
            print("   FAILED: Integer email accepted")
            return False
        except TypeError as e:
            print(f"   Integer email rejected: {e}")
        
        print("\nTest 12: Invalid email (no @)")
        try:
            user11 = User("John", "Doe", "invalidemail.com")
            print("   FAILED: Email without @ accepted")
            return False
        except ValueError as e:
            print(f"   Email without @ rejected: {e}")
        
        print("\nTest 13: Invalid email (no domain)")
        try:
            user12 = User("John", "Doe", "invalid@")
            print("   FAILED: Email without domain accepted")
            return False
        except ValueError as e:
            print(f"   Email without domain rejected: {e}")
        
        print("\nTest 14: is_admin type validation")
        try:
            user13 = User("John", "Doe", "test7@test.com", is_admin="yes")
            print("   FAILED: String is_admin accepted")
            return False
        except TypeError as e:
            print(f"   String is_admin rejected: {e}")
        
        print("\nTest 15: to_dict()")
        user_dict = user1.to_dict()
        assert 'first_name' in user_dict
        assert 'last_name' in user_dict
        assert 'email' in user_dict
        assert 'is_admin' in user_dict
        assert 'id' in user_dict
        print("   to_dict() contains all fields")
        
        print("\nTest 16: Property modification")
        user1.first_name = "Johnny"
        assert user1.first_name == "Johnny"
        print("   Property can be modified")
        
        print("\nTest 17: Property modification validation")
        try:
            user1.first_name = "x"*51
            print("   FAILED: Long name accepted on modification")
            return False
        except ValueError as e:
            print(f"   Long name rejected on modification: {e}")
        
        print("\nUSER MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\nUSER MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        User.emails.clear()


def test_place():
    """Test Place model with @property validation"""
    print_section("TESTING PLACE MODEL")
    try:
        User.emails.clear()
        
        owner = User("John", "Doe", "owner@test.com")
        
        print("\nTest 1: Valid place creation")
        place1 = Place("Beach House", "Nice house", 100.0, 34.0, -118.0, owner)
        assert place1.title == "Beach House"
        assert place1.description == "Nice house"
        assert place1.price == 100.0
        assert place1.latitude == 34.0
        assert place1.longitude == -118.0
        assert place1.owner == owner
        print("   Valid place created")
        
        print("\nTest 2: Bidirectional relationship")
        assert place1 in owner.places
        print("   Place added to owner.places")
        
        print("\nTest 3: Title type validation")
        try:
            place2 = Place(123, "Nice", 100.0, 34.0, -118.0, owner)
            print("   FAILED: Integer title accepted")
            return False
        except TypeError as e:
            print(f"   Integer title rejected: {e}")
        
        print("\nTest 4: Empty title")
        try:
            place3 = Place("", "Nice", 100.0, 34.0, -118.0, owner)
            print("   FAILED: Empty title accepted")
            return False
        except ValueError as e:
            print(f"   Empty title rejected: {e}")
        
        print("\nTest 5: Title too long")
        try:
            place4 = Place("a"*101, "Nice", 100.0, 34.0, -118.0, owner)
            print("   FAILED: Long title accepted")
            return False
        except ValueError as e:
            print(f"   Long title rejected: {e}")
        
        print("\nTest 6: Description type validation")
        try:
            place5 = Place("House", 456, 100.0, 34.0, -118.0, owner)
            print("   FAILED: Integer description accepted")
            return False
        except TypeError as e:
            print(f"   Integer description rejected: {e}")
        
        print("\nTest 7: Empty description allowed")
        place6 = Place("House", "", 100.0, 34.0, -118.0, owner)
        assert place6.description == ""
        print("   Empty description accepted")
        
        print("\nTest 8: Price type validation")
        try:
            place7 = Place("House", "Nice", "expensive", 34.0, -118.0, owner)
            print("   FAILED: String price accepted")
            return False
        except TypeError as e:
            print(f"   String price rejected: {e}")
        
        print("\nTest 9: Price zero")
        try:
            place8 = Place("House", "Nice", 0, 34.0, -118.0, owner)
            print("   FAILED: Zero price accepted")
            return False
        except ValueError as e:
            print(f"   Zero price rejected: {e}")
        
        print("\nTest 10: Price negative")
        try:
            place9 = Place("House", "Nice", -50.0, 34.0, -118.0, owner)
            print("   FAILED: Negative price accepted")
            return False
        except ValueError as e:
            print(f"   Negative price rejected: {e}")
        
        print("\nTest 11: Latitude type validation")
        try:
            place10 = Place("House", "Nice", 100.0, "north", -118.0, owner)
            print("   FAILED: String latitude accepted")
            return False
        except TypeError as e:
            print(f"   String latitude rejected: {e}")
        
        print("\nTest 12: Latitude < -90")
        try:
            place11 = Place("House", "Nice", 100.0, -91.0, -118.0, owner)
            print("   FAILED: Latitude < -90 accepted")
            return False
        except ValueError as e:
            print(f"   Latitude < -90 rejected: {e}")
        
        print("\nTest 13: Latitude > 90")
        try:
            place12 = Place("House", "Nice", 100.0, 91.0, -118.0, owner)
            print("   FAILED: Latitude > 90 accepted")
            return False
        except ValueError as e:
            print(f"   Latitude > 90 rejected: {e}")
        
        print("\nTest 14: Longitude type validation")
        try:
            place13 = Place("House", "Nice", 100.0, 34.0, "west", owner)
            print("   FAILED: String longitude accepted")
            return False
        except TypeError as e:
            print(f"   String longitude rejected: {e}")
        
        print("\nTest 15: Longitude < -180")
        try:
            place14 = Place("House", "Nice", 100.0, 34.0, -181.0, owner)
            print("   FAILED: Longitude < -180 accepted")
            return False
        except ValueError as e:
            print(f"   Longitude < -180 rejected: {e}")
        
        print("\nTest 16: Longitude > 180")
        try:
            place15 = Place("House", "Nice", 100.0, 34.0, 181.0, owner)
            print("   FAILED: Longitude > 180 accepted")
            return False
        except ValueError as e:
            print(f"   Longitude > 180 rejected: {e}")
        
        print("\nTest 17: Owner type validation")
        try:
            place16 = Place("House", "Nice", 100.0, 34.0, -118.0, "NotAUser")
            print("   FAILED: String owner accepted")
            return False
        except TypeError as e:
            print(f"   String owner rejected: {e}")
        
        print("\nTest 18: average_rating with no reviews")
        assert place1.average_rating() == 0.0
        print("   average_rating returns 0.0")
        
        print("\nTest 19: to_dict()")
        place_dict = place1.to_dict()
        assert 'title' in place_dict
        assert 'price' in place_dict
        assert 'owner' in place_dict
        assert place_dict['owner'] == owner.id
        print("   to_dict() contains all fields")
        
        print("\nPLACE MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\nPLACE MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        User.emails.clear()


def test_amenity():
    """Test Amenity model with @property validation"""
    print_section("TESTING AMENITY MODEL")
    try:
        print("\nTest 1: Valid amenity creation")
        amenity1 = Amenity("WiFi")
        assert amenity1.name == "WiFi"
        print("   Valid amenity created")
        
        print("\nTest 2: Name type validation")
        try:
            amenity2 = Amenity(123)
            print("   FAILED: Integer name accepted")
            return False
        except TypeError as e:
            print(f"   Integer name rejected: {e}")
        
        print("\nTest 3: Empty name")
        try:
            amenity3 = Amenity("")
            print("   FAILED: Empty name accepted")
            return False
        except ValueError as e:
            print(f"   Empty name rejected: {e}")
        
        print("\nTest 4: Name too long")
        try:
            amenity4 = Amenity("a"*51)
            print("   FAILED: Long name accepted")
            return False
        except ValueError as e:
            print(f"   Long name rejected: {e}")
        
        print("\nTest 5: to_dict()")
        amenity_dict = amenity1.to_dict()
        assert 'name' in amenity_dict
        assert 'id' in amenity_dict
        print("   to_dict() contains all fields")
        
        print("\nTest 6: Property modification")
        amenity1.name = "Pool"
        assert amenity1.name == "Pool"
        print("   Property can be modified")
        
        print("\nAMENITY MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\nAMENITY MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_review():
    """Test Review model with @property validation"""
    print_section("TESTING REVIEW MODEL")
    try:
        User.emails.clear()
        
        user = User("John", "Doe", "reviewer@test.com")
        place = Place("Beach House", "Nice", 100.0, 34.0, -118.0, user)
        
        print("\nTest 1: Valid review creation")
        review1 = Review("Great place!", 5, place, user)
        assert review1.text == "Great place!"
        assert review1.rating == 5
        assert review1.place == place
        assert review1.user == user
        print("   Valid review created")
        
        print("\nTest 2: Bidirectional relationships")
        assert review1 in place.reviews
        assert review1 in user.reviews
        print("   Review added to place.reviews and user.reviews")
        
        print("\nTest 3: Text type validation")
        try:
            review2 = Review(123, 5, place, user)
            print("   FAILED: Integer text accepted")
            return False
        except TypeError as e:
            print(f"   Integer text rejected: {e}")
        
        print("\nTest 4: Empty text")
        try:
            review3 = Review("", 5, place, user)
            print("   FAILED: Empty text accepted")
            return False
        except ValueError as e:
            print(f"   Empty text rejected: {e}")
        
        print("\nTest 5: Whitespace-only text")
        try:
            review4 = Review("   ", 5, place, user)
            print("   FAILED: Whitespace-only text accepted")
            return False
        except ValueError as e:
            print(f"   Whitespace-only text rejected: {e}")
        
        print("\nTest 6: Rating type validation")
        try:
            review5 = Review("Good", 4.5, place, user)
            print("   FAILED: Float rating accepted")
            return False
        except TypeError as e:
            print(f"   Float rating rejected: {e}")
        
        print("\nTest 7: Rating < 1")
        try:
            review6 = Review("Bad", 0, place, user)
            print("   FAILED: Rating 0 accepted")
            return False
        except ValueError as e:
            print(f"   Rating 0 rejected: {e}")
        
        print("\nTest 8: Rating > 5")
        try:
            review7 = Review("Too good", 6, place, user)
            print("   FAILED: Rating 6 accepted")
            return False
        except ValueError as e:
            print(f"   Rating 6 rejected: {e}")
        
        print("\nTest 9: All valid ratings (1-5)")
        for rating in range(1, 6):
            r = Review(f"Rating {rating}", rating, place, user)
            assert r.rating == rating
        print("   All ratings 1-5 accepted")
        
        print("\nTest 10: Place type validation")
        try:
            review8 = Review("Good", 5, "NotAPlace", user)
            print("   FAILED: String place accepted")
            return False
        except TypeError as e:
            print(f"   String place rejected: {e}")
        
        print("\nTest 11: User type validation")
        try:
            review9 = Review("Good", 5, place, "NotAUser")
            print("   FAILED: String user accepted")
            return False
        except TypeError as e:
            print(f"   String user rejected: {e}")
        
        print("\nTest 12: average_rating calculation")
        avg = place.average_rating()
        expected = (5 + 1 + 2 + 3 + 4 + 5) / 6
        assert avg == expected
        print(f"   average_rating calculated: {avg}")
        
        print("\nTest 13: to_dict()")
        review_dict = review1.to_dict()
        assert 'text' in review_dict
        assert 'rating' in review_dict
        assert 'place' in review_dict
        assert 'user' in review_dict
        assert review_dict['place'] == place.id
        assert review_dict['user'] == user.id
        print("   to_dict() contains all fields")
        
        print("\nREVIEW MODEL: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\nREVIEW MODEL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        User.emails.clear()


def test_integration():
    """Test integration between all models"""
    print_section("TESTING INTEGRATION")
    try:
        User.emails.clear()
        
        print("\nCreating complete scenario...")
        user = User("John", "Doe", "integration@test.com")
        
        place = Place("Beach House", "Beautiful house", 150.0, 34.0, -118.0, user)
        
        wifi = Amenity("WiFi")
        pool = Amenity("Pool")
        parking = Amenity("Parking")
        place.add_amenity(wifi)
        place.add_amenity(pool)
        place.add_amenity(parking)
        
        review1 = Review("Amazing!", 5, place, user)
        review2 = Review("Good", 4, place, user)
        review3 = Review("Perfect", 5, place, user)
        
        print("   Scenario created")
        
        print("\nTesting relationships...")
        assert len(user.places) == 1
        print(f"   User has {len(user.places)} place(s)")
        
        assert len(place.reviews) == 3
        print(f"   Place has {len(place.reviews)} reviews")
        
        assert len(user.reviews) == 3
        print(f"   User has {len(user.reviews)} reviews")
        
        assert len(place.amenities) == 3
        print(f"   Place has {len(place.amenities)} amenities")
        
        print("\nTesting average rating...")
        avg = place.average_rating()
        expected = (5 + 4 + 5) / 3
        assert abs(avg - expected) < 0.01
        print(f"   Average rating: {avg}")
        
        print("\nTesting to_dict() with relationships...")
        place_dict = place.to_dict()
        
        assert 'owner' in place_dict
        assert place_dict['owner'] == user.id
        print("   to_dict() handles owner relationship")
        
        assert 'reviews' in place_dict
        assert len(place_dict['reviews']) == 3
        print("   to_dict() handles reviews relationship")
        
        assert 'amenities' in place_dict
        assert len(place_dict['amenities']) == 3
        print("   to_dict() handles amenities relationship")
        
        print("\nTesting property modification...")
        place.title = "Luxury Beach House"
        assert place.title == "Luxury Beach House"
        print("   Place title modified")
        
        user.first_name = "Johnny"
        assert user.first_name == "Johnny"
        print("   User name modified")
        
        print("\nTesting email uniqueness...")
        user2 = User("Jane", "Smith", "jane@test.com")
        try:
            user3 = User("Bob", "Jones", "jane@test.com")
            print("   FAILED: Duplicate email accepted")
            return False
        except ValueError:
            print("   Duplicate email rejected across users")
        
        print("\nINTEGRATION: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\nINTEGRATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        User.emails.clear()


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  HBnB NEW MODELS - COMPLETE TEST SUITE")
    print("  (with @property validation)")
    print("="*60)
    
    results = {
        "BaseModel": test_base_model(),
        "User": test_user(),
        "Place": test_place(),
        "Amenity": test_amenity(),
        "Review": test_review(),
        "Integration": test_integration()
    }
    
    print_section("FINAL REPORT")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for model, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{model:20} {status}")
    
    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} tests passed")
    print('='*60)
    
    if passed == total:
        print("\nALL TESTS PASSED! New models with @property are ready!\n")
        return 0
    else:
        print(f"\n{total - passed} test(s) failed. Check errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
    