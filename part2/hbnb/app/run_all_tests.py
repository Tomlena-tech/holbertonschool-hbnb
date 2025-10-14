#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

print("Testing...")

user = User(first_name="John", last_name="Doe", email="john@test.com")
print(f"✅ User: {user.first_name}")

place = Place(title="House", description="Nice", price=100.0, latitude=34.0, longitude=-118.0, owner=user)
print(f"✅ Place: {place.title}")
print(f"✅ User has {len(user.places)} place")

wifi = Amenity(name="WiFi")
place.add_amenity(wifi)
print(f"✅ Amenity: {wifi.name}")

review = Review(text="Great!", rating=5, place=place, user=user)
print(f"✅ Review rating: {review.rating}")

print("\n🎉 ALL TESTS PASSED!")
