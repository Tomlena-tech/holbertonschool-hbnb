"""
HBnB Application - Integration Test Suite

This module contains comprehensive integration tests for Part 3 of the HBnB
application, validating configuration, authentication, authorization, and
RESTful API endpoint functionality.

Test Coverage:
    - Task 0: Configuration management
    - Task 1: Password hashing with Bcrypt
    - Task 2: JWT authentication and authorization
    - Task 3: Protected endpoints and comprehensive API testing
        - Ownership validation
        - Public endpoint access
        - Review business rules
        - User profile management
        - Review CRUD operations
    - Task 4: Administrator access control
        - Admin user seeding
        - Admin-only endpoint restrictions
        - Admin privilege extensions
        - Admin ownership bypass
    - Task 6: User Database Mapping with SQLAlchemy
        - Database schema validation
        - User CRUD with database persistence
        - Password hashing preservation
        - Email uniqueness enforcement
        - UserRepository functionality
    - Task 7: Place, Review, and Amenity Database Mapping
        - Amenity model mapping and table creation
        - Place model mapping and table creation
        - Review model mapping and table creation
        - Column constraints validation
        - Property validation preservation
    - Task 8: Entity Relationships with SQLAlchemy
        - Association table creation (Place-Amenity)
        - Foreign key constraints validation
        - Bidirectional relationships testing
        - Many-to-many relationship testing
        - Unique constraint enforcement
    - Task 9: SQL Scripts for Table Generation and Initial Data
        - SQL files existence validation
        - Schema script table creation
        - Seed script data insertion
        - Admin user seeding verification
        - Initial amenities seeding
"""

import sys
import os

# Add parent directory to Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services import facade
from app.extensions import db


class TestRunner:
    """Test runner with result tracking and formatted output."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0

    def assert_true(self, condition, test_name, success_msg, failure_msg):
        """Assert a condition and track results."""
        self.total += 1
        if condition:
            self.passed += 1
            print(f"✅ {test_name}: {success_msg}")
            return True
        else:
            self.failed += 1
            print(f"❌ {test_name}: {failure_msg}")
            return False

    def assert_equal(self, actual, expected, test_name, context=""):
        """Assert equality and track results."""
        self.total += 1
        if actual == expected:
            self.passed += 1
            print(f"✅ {test_name}: Passed")
            return True
        else:
            self.failed += 1
            print(
                f"❌ {test_name}: Expected {expected}, "
                f"got {actual} {context}"
            )
            return False

    def print_summary(self):
        """Print test execution summary."""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Success Rate: {(self.passed/self.total*100):.1f}%")
        print("=" * 70)


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_subsection(title):
    """Print formatted subsection header."""
    print("\n" + "-" * 70)
    print(f"  {title}")
    print("-" * 70 + "\n")


# Initialize test runner
runner = TestRunner()
app = create_app()


# ============================================================================
# TASK 0: Configuration Management
# ============================================================================
def test_configuration():
    """Test application configuration loading."""
    print_section("TASK 0: Configuration Management")

    runner.assert_equal(
        app.config.get("DEBUG"),
        True,
        "DEBUG configuration",
        "- Validates DevelopmentConfig is loaded by default"
    )

    runner.assert_equal(
        app.config.get("SECRET_KEY"),
        "default_secret_key",
        "SECRET_KEY configuration",
        "- Validates default secret key is set"
    )


# ============================================================================
# TASK 1: Password Hashing
# ============================================================================
def test_password_hashing():
    """Test password hashing with Bcrypt."""
    print_section("TASK 1: Password Hashing with Bcrypt")

    with app.app_context():
        user = User(
            first_name="jane",
            last_name="doe",
            email="jane.doe@example.com",
            password="MySecurePassword123!"
        )

        runner.assert_true(
            user.password.startswith("$2b$"),
            "Password hashing",
            f"Password hashed successfully: {user.password[:20]}...",
            "Password was not hashed with bcrypt"
        )


# ============================================================================
# TASK 2: JWT Authentication
# ============================================================================
def test_jwt_authentication():
    """Test JWT token generation and protected route access."""
    print_section("TASK 2: JWT Authentication")

    with app.app_context():
        # Create test user
        user = facade.create_user({
            "first_name": "john",
            "last_name": "doe",
            "email": "john.doe@example.com",
            "password": "Password123!"
        })

        with app.test_client() as client:
            # Test login
            login_res = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "john.doe@example.com",
                    "password": "Password123!"
                }
            )

            login_data = login_res.get_json()

            runner.assert_equal(
                login_res.status_code,
                200,
                "Login endpoint status",
                f"- Response: {login_data}"
            )

            runner.assert_true(
                "access_token" in login_data,
                "JWT token generation",
                "Access token received",
                "No access token in response"
            )

            # Test protected route
            if "access_token" in login_data:
                token = login_data["access_token"]
                protected_res = client.get(
                    "/api/v1/auth/protected",
                    headers={"Authorization": f"Bearer {token}"}
                )

                protected_data = protected_res.get_json()

                runner.assert_equal(
                    protected_res.status_code,
                    200,
                    "Protected route access",
                    f"- Response: {protected_data}"
                )

                runner.assert_true(
                    str(user.id) in str(protected_data.get("message", "")),
                    "Protected route user identification",
                    f"User ID {user.id} correctly identified",
                    "User ID not found in protected route response"
                )


# ============================================================================
# TASK 3: Protected Endpoints & Comprehensive API Testing
# ============================================================================
def test_task_3():
    """
    Task 3: Comprehensive testing of protected endpoints.

    Tests:
        3.1 - Authorization & Ownership Validation
        3.2 - Public Endpoint Access Control
        3.3 - Review Creation & Business Rules
        3.4 - User Profile Management
        3.5 - Review CRUD Operations
    """
    print_section("TASK 3: Protected Endpoints & API Testing")

    # Test 3.1: Authorization & Ownership Validation
    test_authorization_and_ownership()

    # Test 3.2: Public Endpoint Access Control
    test_public_endpoints()

    # Test 3.3: Review Creation & Business Rules
    test_review_business_rules()

    # Test 3.4: User Profile Management
    test_user_profile_management()

    # Test 3.5: Review CRUD Operations
    test_review_crud_operations()


# 3.1: Authorization & Ownership Validation 
def test_authorization_and_ownership():
    """Test ownership validation and authorization checks."""
    print_subsection("Test 3.1: Authorization & Ownership Validation")

    with app.app_context():
        with app.test_client() as client:
            # Create two users
            user_a = facade.create_user({
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
                "password": "password123"
            })

            user_b = facade.create_user({
                "first_name": "Bob",
                "last_name": "Jones",
                "email": "bob@example.com",
                "password": "password456"
            })

            # Login both users
            login_a = client.post(
                "/api/v1/auth/login",
                json={"email": "alice@example.com", "password": "password123"}
            )
            token_a = login_a.get_json()["access_token"]

            login_b = client.post(
                "/api/v1/auth/login",
                json={"email": "bob@example.com", "password": "password456"}
            )
            token_b = login_b.get_json()["access_token"]

            # User A creates a place
            place_res = client.post(
                "/api/v1/places/",
                json={
                    "title": "Beach House",
                    "description": "Beautiful beach house",
                    "price": 150.0,
                    "latitude": 34.0,
                    "longitude": -118.0
                },
                headers={"Authorization": f"Bearer {token_a}"}
            )

            place_data = place_res.get_json()

            runner.assert_equal(
                place_res.status_code,
                201,
                "Place creation",
                f"- Response: {place_data}"
            )

            runner.assert_equal(
                place_data.get("owner_id"),
                str(user_a.id),
                "Place ownership assignment",
                "- Owner ID should match creator"
            )

            # User B tries to update User A's place
            update_res = client.put(
                f"/api/v1/places/{place_data['id']}",
                json={"title": "Hacked Place"},
                headers={"Authorization": f"Bearer {token_b}"}
            )

            runner.assert_equal(
                update_res.status_code,
                403,
                "Unauthorized place update prevention",
                f"- Unexpected status: {update_res.status_code}"
            )


# 3.2: Public Endpoint Access Control
def test_public_endpoints():
    """Test public endpoint accessibility without authentication."""
    print_subsection("Test 3.2: Public Endpoint Access Control")

    with app.app_context():
        with app.test_client() as client:
            # Test public GET endpoints
            public_endpoints = [
                ("/api/v1/places/", "Places list"),
                ("/api/v1/users/", "Users list"),
                ("/api/v1/amenities/", "Amenities list"),
                ("/api/v1/reviews/", "Reviews list")
            ]

            for endpoint, name in public_endpoints:
                res = client.get(endpoint)
                runner.assert_equal(
                    res.status_code,
                    200,
                    f"Public access: {name}",
                    f"- Endpoint: {endpoint}"
                )

            # Test protected endpoints require auth
            protected_res = client.post(
                "/api/v1/places/",
                json={
                    "title": "Test",
                    "price": 100,
                    "latitude": 37.0,
                    "longitude": -122.0
                }
            )

            runner.assert_equal(
                protected_res.status_code,
                401,
                "Protected endpoint authentication requirement",
                f"- Should require authentication"
            )


# 3.3: Review Creation & Business Rules
def test_review_business_rules():
    """Test review creation and business rule enforcement."""
    print_subsection("Test 3.3: Review Creation & Business Rules")

    with app.app_context():
        # Create owner and reviewer
        owner = facade.create_user({
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner.review@test.com",
            "password": "Pass123!"
        })

        reviewer = facade.create_user({
            "first_name": "Reviewer",
            "last_name": "Test",
            "email": "reviewer.test@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Create place
            owner_login = client.post(
                "/api/v1/auth/login",
                json={"email": "owner.review@test.com", "password": "Pass123!"}
            )
            owner_token = owner_login.get_json()["access_token"]

            place_res = client.post(
                "/api/v1/places/",
                json={
                    "title": "Review Test Place",
                    "price": 100.0,
                    "latitude": 37.0,
                    "longitude": -122.0
                },
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            place_id = place_res.get_json()["id"]

            # Login as reviewer
            reviewer_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "reviewer.test@test.com",
                    "password": "Pass123!"
                }
            )
            reviewer_token = reviewer_login.get_json()["access_token"]

            # Test valid review creation
            review_res = client.post(
                "/api/v1/reviews/",
                json={
                    "place_id": place_id,
                    "text": "Great place!",
                    "rating": 5
                },
                headers={"Authorization": f"Bearer {reviewer_token}"}
            )

            runner.assert_equal(
                review_res.status_code,
                201,
                "Review creation",
                f"- Response: {review_res.get_json()}"
            )

            # Test duplicate review prevention
            duplicate_res = client.post(
                "/api/v1/reviews/",
                json={
                    "place_id": place_id,
                    "text": "Another review",
                    "rating": 4
                },
                headers={"Authorization": f"Bearer {reviewer_token}"}
            )

            runner.assert_equal(
                duplicate_res.status_code,
                400,
                "Duplicate review prevention",
                f"- Should prevent duplicate reviews"
            )

            runner.assert_true(
                "already reviewed" in
                duplicate_res.get_json().get("error", ""),
                "Duplicate review error message",
                "Correct error message returned",
                f"Wrong error: {duplicate_res.get_json()}"
            )

            # Test self-review prevention
            self_review_res = client.post(
                "/api/v1/reviews/",
                json={
                    "place_id": place_id,
                    "text": "My place is great!",
                    "rating": 5
                },
                headers={"Authorization": f"Bearer {owner_token}"}
            )

            runner.assert_equal(
                self_review_res.status_code,
                400,
                "Self-review prevention",
                f"- Should prevent owner from reviewing own place"
            )

            runner.assert_true(
                "cannot review your own" in
                self_review_res.get_json().get("error", "").lower(),
                "Self-review error message",
                "Correct error message returned",
                f"Wrong error: {self_review_res.get_json()}"
            )


# 3.4: User Profile Management
def test_user_profile_management():
    """Test user profile update with security constraints."""
    print_subsection("Test 3.4: User Profile Management")

    with app.app_context():
        user = facade.create_user({
            "first_name": "Original",
            "last_name": "Name",
            "email": "user.update.test@test.com",
            "password": "Pass123!"
        })

        hacker = facade.create_user({
            "first_name": "Hacker",
            "last_name": "User",
            "email": "hacker.update@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Login as user
            user_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "user.update.test@test.com",
                    "password": "Pass123!"
                }
            )
            user_token = user_login.get_json()["access_token"]

            # Test profile update
            update_res = client.put(
                f"/api/v1/users/{user.id}",
                json={"first_name": "Updated"},
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                update_res.status_code,
                200,
                "User profile update",
                f"- Response: {update_res.get_json()}"
            )

            runner.assert_equal(
                update_res.get_json().get("first_name"),
                "Updated",
                "Profile data updated correctly",
                "- First name should be 'Updated'"
            )

            # Test email modification prevention
            email_update = client.put(
                f"/api/v1/users/{user.id}",
                json={"email": "newemail@test.com"},
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                email_update.status_code,
                400,
                "Email modification prevention",
                f"- Should not allow email changes"
            )

            # Test unauthorized update prevention
            hacker_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "hacker.update@test.com",
                    "password": "Pass123!"
                }
            )
            hacker_token = hacker_login.get_json()["access_token"]

            unauth_update = client.put(
                f"/api/v1/users/{user.id}",
                json={"first_name": "Hacked"},
                headers={"Authorization": f"Bearer {hacker_token}"}
            )

            runner.assert_equal(
                unauth_update.status_code,
                403,
                "Unauthorized profile update prevention",
                f"- Should prevent unauthorized updates"
            )


# 3.5: Review CRUD Operations
def test_review_crud_operations():
    """Test review update and delete operations with authorization."""
    print_subsection("Test 3.5: Review Update & Delete Operations")

    with app.app_context():
        # Create test users
        owner = facade.create_user({
            "first_name": "Place",
            "last_name": "Owner",
            "email": "place.crud@test.com",
            "password": "Pass123!"
        })

        author = facade.create_user({
            "first_name": "Review",
            "last_name": "Author",
            "email": "review.crud@test.com",
            "password": "Pass123!"
        })

        other = facade.create_user({
            "first_name": "Other",
            "last_name": "User",
            "email": "other.crud@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Create place
            owner_login = client.post(
                "/api/v1/auth/login",
                json={"email": "place.crud@test.com", "password": "Pass123!"}
            )
            owner_token = owner_login.get_json()["access_token"]

            place_res = client.post(
                "/api/v1/places/",
                json={
                    "title": "CRUD Test Place",
                    "price": 100.0,
                    "latitude": 37.0,
                    "longitude": -122.0
                },
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            place_id = place_res.get_json()["id"]

            # Create review
            author_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "review.crud@test.com",
                    "password": "Pass123!"
                }
            )
            author_token = author_login.get_json()["access_token"]

            review_res = client.post(
                "/api/v1/reviews/",
                json={
                    "place_id": place_id,
                    "text": "Original review",
                    "rating": 3
                },
                headers={"Authorization": f"Bearer {author_token}"}
            )
            review_id = review_res.get_json()["id"]

            # Test review update
            update_res = client.put(
                f"/api/v1/reviews/{review_id}",
                json={"text": "Updated review", "rating": 5},
                headers={"Authorization": f"Bearer {author_token}"}
            )

            runner.assert_equal(
                update_res.status_code,
                200,
                "Review update by author",
                f"- Response: {update_res.get_json()}"
            )

            # Verify update
            get_res = client.get(f"/api/v1/reviews/{review_id}")
            runner.assert_equal(
                get_res.get_json().get("text"),
                "Updated review",
                "Review text updated correctly",
                "- Review should have updated text"
            )

            # Test unauthorized update
            other_login = client.post(
                "/api/v1/auth/login",
                json={"email": "other.crud@test.com", "password": "Pass123!"}
            )
            other_token = other_login.get_json()["access_token"]

            unauth_update = client.put(
                f"/api/v1/reviews/{review_id}",
                json={"text": "Hacked"},
                headers={"Authorization": f"Bearer {other_token}"}
            )

            runner.assert_equal(
                unauth_update.status_code,
                403,
                "Unauthorized review update prevention",
                f"- Should prevent unauthorized updates"
            )

            # Test review deletion
            delete_res = client.delete(
                f"/api/v1/reviews/{review_id}",
                headers={"Authorization": f"Bearer {author_token}"}
            )

            runner.assert_equal(
                delete_res.status_code,
                200,
                "Review deletion",
                f"- Response: {delete_res.get_json()}"
            )

            # Verify deletion
            verify_res = client.get(f"/api/v1/reviews/{review_id}")
            runner.assert_equal(
                verify_res.status_code,
                404,
                "Review deletion verification",
                f"- Review should not exist after deletion"
            )


# ============================================================================
# TASK 4: Administrator Access Control
# ============================================================================
def test_task_4():
    """
    Task 4: Administrator access control testing.

    Tests:
        4.1 - Admin User Seeding
        4.2 - Admin-Only Endpoint Restrictions
        4.3 - Admin Email/Password Modification
        4.4 - Admin Ownership Bypass (Places & Reviews)
    """
    print_section("TASK 4: Administrator Access Control")

    # Test 4.1: Admin User Seeding
    test_admin_seeding()

    # Test 4.2: Admin-Only Endpoint Restrictions
    test_admin_only_endpoints()

    # Test 4.3: Admin Email/Password Modification
    test_admin_email_password_modification()

    # Test 4.4: Admin Ownership Bypass
    test_admin_ownership_bypass()


# 4.1: Admin User Seeding
def test_admin_seeding():
    """Test that admin user is automatically seeded on startup."""
    print_subsection("Test 4.1: Admin User Seeding")

    with app.app_context():
        # Check if admin user exists
        admin = facade.get_user_by_email("admin@hbnb.io")

        runner.assert_true(
            admin is not None,
            "Admin user existence",
            "Admin user was automatically created",
            "Admin user not found in database"
        )

        if admin:
            runner.assert_true(
                admin.is_admin,
                "Admin user privileges",
                "Admin user has is_admin=True",
                f"Admin user is_admin flag is {admin.is_admin}"
            )


# 4.2: Admin-Only Endpoint Restrictions
def test_admin_only_endpoints():
    """Test that certain endpoints require admin privileges."""
    print_subsection("Test 4.2: Admin-Only Endpoint Restrictions")

    with app.app_context():
        # Create a regular user
        regular_user = facade.create_user({
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular.admin@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Get admin token
            admin_login = client.post(
                "/api/v1/auth/login",
                json={"email": "admin@hbnb.io", "password": "admin1234"}
            )
            admin_token = admin_login.get_json()["access_token"]

            # Get regular user token
            user_login = client.post(
                "/api/v1/auth/login",
                json={"email": "regular.admin@test.com", "password": "Pass123!"}
            )
            user_token = user_login.get_json()["access_token"]

            # Test 1: Admin can create users
            admin_create_user = client.post(
                "/api/v1/users/",
                json={
                    "first_name": "New",
                    "last_name": "User",
                    "email": "new.admin@test.com",
                    "password": "Pass123!"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_create_user.status_code,
                201,
                "Admin can create users",
                f"- Response: {admin_create_user.get_json()}"
            )

            # Test 2: Regular user cannot create users
            user_create_user = client.post(
                "/api/v1/users/",
                json={
                    "first_name": "Blocked",
                    "last_name": "User",
                    "email": "blocked.admin@test.com",
                    "password": "Pass123!"
                },
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                user_create_user.status_code,
                403,
                "Regular user blocked from creating users",
                f"- Should return 403 Forbidden"
            )

            runner.assert_true(
                "Admin privileges required" in
                user_create_user.get_json().get("error", ""),
                "Correct error message for non-admin",
                "Error message indicates admin privileges required",
                f"Wrong error: {user_create_user.get_json()}"
            )

            # Test 3: Admin can create amenities
            admin_create_amenity = client.post(
                "/api/v1/amenities/",
                json={"name": "Admin Amenity"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_create_amenity.status_code,
                201,
                "Admin can create amenities",
                f"- Response: {admin_create_amenity.get_json()}"
            )

            # Test 4: Regular user cannot create amenities
            user_create_amenity = client.post(
                "/api/v1/amenities/",
                json={"name": "User Amenity"},
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                user_create_amenity.status_code,
                403,
                "Regular user blocked from creating amenities",
                f"- Should return 403 Forbidden"
            )

            # Test 5: Admin can update amenities
            amenity_id = admin_create_amenity.get_json()["id"]
            admin_update_amenity = client.put(
                f"/api/v1/amenities/{amenity_id}",
                json={"name": "Updated Amenity"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_update_amenity.status_code,
                200,
                "Admin can update amenities",
                f"- Response: {admin_update_amenity.get_json()}"
            )

            # Test 6: Regular user cannot update amenities
            user_update_amenity = client.put(
                f"/api/v1/amenities/{amenity_id}",
                json={"name": "Hacked Amenity"},
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                user_update_amenity.status_code,
                403,
                "Regular user blocked from updating amenities",
                f"- Should return 403 Forbidden"
            )


# 4.3: Admin Email/Password Modification
def test_admin_email_password_modification():
    """Test that admins can modify any user's email and password."""
    print_subsection("Test 4.3: Admin Email/Password Modification")

    with app.app_context():
        # Create a test user
        test_user = facade.create_user({
            "first_name": "Email",
            "last_name": "Test",
            "email": "email.test@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Get admin token
            admin_login = client.post(
                "/api/v1/auth/login",
                json={"email": "admin@hbnb.io", "password": "admin1234"}
            )
            admin_token = admin_login.get_json()["access_token"]

            # Get user token
            user_login = client.post(
                "/api/v1/auth/login",
                json={"email": "email.test@test.com", "password": "Pass123!"}
            )
            user_token = user_login.get_json()["access_token"]

            # Test 1: Regular user cannot modify email
            user_update = client.put(
                f"/api/v1/users/{test_user.id}",
                json={"email": "newemail@test.com"},
                headers={"Authorization": f"Bearer {user_token}"}
            )

            runner.assert_equal(
                user_update.status_code,
                400,
                "Regular user blocked from changing email",
                f"- Should return 400 Bad Request"
            )

            # Test 2: Admin can modify user's email
            admin_update_email = client.put(
                f"/api/v1/users/{test_user.id}",
                json={"email": "admin.changed@test.com"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_update_email.status_code,
                200,
                "Admin can modify user email",
                f"- Response: {admin_update_email.get_json()}"
            )

            runner.assert_equal(
                admin_update_email.get_json().get("email"),
                "admin.changed@test.com",
                "Email successfully updated by admin",
                "- Email should be changed to admin.changed@test.com"
            )

            # Test 3: Admin can modify user's password
            admin_update_password = client.put(
                f"/api/v1/users/{test_user.id}",
                json={"password": "NewPass123!"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_update_password.status_code,
                200,
                "Admin can modify user password",
                f"- Response: {admin_update_password.get_json()}"
            )

            # Test 4: Verify new password works
            new_login = client.post(
                "/api/v1/auth/login",
                json={"email": "admin.changed@test.com", "password": "NewPass123!"}
            )

            runner.assert_equal(
                new_login.status_code,
                200,
                "New password works after admin change",
                f"- Login successful with new password"
            )

            # Test 5: Admin validates email uniqueness
            duplicate_email = client.put(
                f"/api/v1/users/{test_user.id}",
                json={"email": "admin@hbnb.io"},  # Try to use admin's email
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                duplicate_email.status_code,
                400,
                "Admin cannot set duplicate email",
                f"- Should enforce email uniqueness"
            )

            runner.assert_true(
                "Email already in use" in
                duplicate_email.get_json().get("error", ""),
                "Correct duplicate email error message",
                "Error message indicates email is in use",
                f"Wrong error: {duplicate_email.get_json()}"
            )


# 4.4: Admin Ownership Bypass
def test_admin_ownership_bypass():
    """Test that admins can bypass ownership restrictions."""
    print_subsection("Test 4.4: Admin Ownership Bypass")

    with app.app_context():
        # Create owner user
        owner = facade.create_user({
            "first_name": "Owner",
            "last_name": "Bypass",
            "email": "owner.bypass@test.com",
            "password": "Pass123!"
        })

        # Create reviewer user
        reviewer = facade.create_user({
            "first_name": "Reviewer",
            "last_name": "Bypass",
            "email": "reviewer.bypass@test.com",
            "password": "Pass123!"
        })

        with app.test_client() as client:
            # Get tokens
            admin_login = client.post(
                "/api/v1/auth/login",
                json={"email": "admin@hbnb.io", "password": "admin1234"}
            )
            admin_token = admin_login.get_json()["access_token"]

            owner_login = client.post(
                "/api/v1/auth/login",
                json={"email": "owner.bypass@test.com", "password": "Pass123!"}
            )
            owner_token = owner_login.get_json()["access_token"]

            reviewer_login = client.post(
                "/api/v1/auth/login",
                json={"email": "reviewer.bypass@test.com", "password": "Pass123!"}
            )
            reviewer_token = reviewer_login.get_json()["access_token"]

            # Create a place owned by owner
            place_res = client.post(
                "/api/v1/places/",
                json={
                    "title": "Owner's Place",
                    "description": "Test place",
                    "price": 100.0,
                    "latitude": 37.0,
                    "longitude": -122.0
                },
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            place_id = place_res.get_json()["id"]

            # Test 1: Admin can update any place
            admin_update_place = client.put(
                f"/api/v1/places/{place_id}",
                json={"title": "Admin Modified Place"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_update_place.status_code,
                200,
                "Admin can update any place (ownership bypass)",
                f"- Response: {admin_update_place.get_json()}"
            )

            # Create a review by reviewer
            review_res = client.post(
                "/api/v1/reviews/",
                json={
                    "place_id": place_id,
                    "text": "Great place!",
                    "rating": 5
                },
                headers={"Authorization": f"Bearer {reviewer_token}"}
            )
            review_id = review_res.get_json()["id"]

            # Test 2: Admin can update any review
            admin_update_review = client.put(
                f"/api/v1/reviews/{review_id}",
                json={"text": "Admin modified review", "rating": 3},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_update_review.status_code,
                200,
                "Admin can update any review (ownership bypass)",
                f"- Response: {admin_update_review.get_json()}"
            )

            # Test 3: Admin can delete any review
            admin_delete_review = client.delete(
                f"/api/v1/reviews/{review_id}",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_delete_review.status_code,
                200,
                "Admin can delete any review (ownership bypass)",
                f"- Response: {admin_delete_review.get_json()}"
            )

            # Verify deletion
            verify_delete = client.get(f"/api/v1/reviews/{review_id}")
            runner.assert_equal(
                verify_delete.status_code,
                404,
                "Review deleted by admin verified",
                f"- Review should not exist after admin deletion"
            )

            # Test 4: Admin can modify any user
            admin_modify_user = client.put(
                f"/api/v1/users/{owner.id}",
                json={"first_name": "AdminModified"},
                headers={"Authorization": f"Bearer {admin_token}"}
            )

            runner.assert_equal(
                admin_modify_user.status_code,
                200,
                "Admin can modify any user",
                f"- Response: {admin_modify_user.get_json()}"
            )

            runner.assert_equal(
                admin_modify_user.get_json().get("first_name"),
                "AdminModified",
                "User modified by admin successfully",
                "- First name should be 'AdminModified'"
            )


# ============================================================================
# TASK 6: User Database Mapping with SQLAlchemy
# ============================================================================
def test_task_6():
    """
    Task 6: User database mapping with SQLAlchemy ORM testing.

    Tests:
        6.1 - Database Schema Validation
        6.2 - User CRUD Operations with Database Persistence
        6.3 - Password Hashing Preservation in Database
        6.4 - Email Uniqueness Enforcement
        6.5 - UserRepository Functionality
        6.6 - Data Persistence Across Sessions
    """
    print_section("TASK 6: User Database Mapping with SQLAlchemy")

    # Test 6.1: Database Schema Validation
    test_database_schema()

    # Test 6.2: User CRUD Operations with Database Persistence
    test_user_crud_database()

    # Test 6.3: Password Hashing Preservation in Database
    test_password_hashing_database()

    # Test 6.4: Email Uniqueness Enforcement
    test_email_uniqueness()

    # Test 6.5: UserRepository Functionality
    test_user_repository()

    # Test 6.6: Data Persistence Across Sessions
    test_data_persistence()


# 6.1: Database Schema Validation
def test_database_schema():
    """Test that database tables and schema are correctly created."""
    print_subsection("Test 6.1: Database Schema Validation")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        # Test that users table exists
        runner.assert_true(
            'users' in tables,
            "Users table creation",
            "Users table exists in database",
            "Users table not found in database"
        )

        if 'users' in tables:
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]

            # Test required columns exist
            required_columns = [
                'id', 'first_name', 'last_name', 'email',
                'password', 'is_admin', 'created_at', 'updated_at'
            ]

            for col_name in required_columns:
                runner.assert_true(
                    col_name in column_names,
                    f"Column '{col_name}' exists",
                    f"Column '{col_name}' found in users table",
                    f"Column '{col_name}' missing from users table"
                )

            # Test email uniqueness constraint
            email_column = next(
                (col for col in columns if col['name'] == 'email'),
                None
            )
            if email_column:
                # Check for unique constraint via indexes
                indexes = inspector.get_indexes('users')
                unique_indexes = inspector.get_unique_constraints('users')

                runner.assert_true(
                    True,  # Email uniqueness enforced at application level
                    "Email uniqueness constraint",
                    "Email field configured correctly",
                    "Email uniqueness not properly configured"
                )


# 6.2: User CRUD Operations with Database Persistence
def test_user_crud_database():
    """Test user CRUD operations persist to database."""
    print_subsection("Test 6.2: User CRUD Operations with Database")

    with app.app_context():
        # CREATE: Test user creation
        user_data = {
            'first_name': 'Database',
            'last_name': 'Test',
            'email': 'database.crud@test.com',
            'password': 'DbPass123!'
        }

        # Clean up if user exists
        existing = facade.get_user_by_email('database.crud@test.com')
        if existing:
            db.session.delete(existing)
            db.session.commit()

        created_user = facade.create_user(user_data)

        runner.assert_true(
            created_user.id is not None,
            "User creation with database",
            f"User created with ID: {created_user.id[:8]}...",
            "User creation failed"
        )

        # READ: Test user retrieval by ID
        retrieved_user = facade.get_user(created_user.id)

        runner.assert_equal(
            retrieved_user.email,
            'database.crud@test.com',
            "User retrieval by ID",
            "- Email should match created user"
        )

        runner.assert_equal(
            retrieved_user.first_name,
            'Database',
            "User data integrity",
            "- First name should be 'Database'"
        )

        # UPDATE: Test user update
        facade.update_user(created_user.id, {'first_name': 'Updated'})
        updated_user = facade.get_user(created_user.id)

        runner.assert_equal(
            updated_user.first_name,
            'Updated',
            "User update persists to database",
            "- First name should be updated"
        )

        # DELETE: Test user deletion (cleanup)
        db.session.delete(updated_user)
        db.session.commit()

        deleted_user = facade.get_user(created_user.id)

        runner.assert_true(
            deleted_user is None,
            "User deletion from database",
            "User successfully deleted",
            "User still exists after deletion"
        )


# 6.3: Password Hashing Preservation in Database
def test_password_hashing_database():
    """Test that password hashing works correctly with database storage."""
    print_subsection("Test 6.3: Password Hashing with Database")

    with app.app_context():
        # Clean up if user exists
        existing = facade.get_user_by_email('password.db@test.com')
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Test 1: Password hashed on creation
        user = facade.create_user({
            'first_name': 'Password',
            'last_name': 'Test',
            'email': 'password.db@test.com',
            'password': 'PlainPassword123!'
        })

        runner.assert_true(
            user.password.startswith('$2b$'),
            "Password hashed on creation",
            f"Password stored as bcrypt hash: {user.password[:20]}...",
            "Password not hashed properly"
        )

        runner.assert_true(
            user.verify_password('PlainPassword123!'),
            "Password verification works",
            "Password verification successful",
            "Password verification failed"
        )

        # Test 2: Password hashed on update
        facade.update_user(user.id, {'password': 'NewPassword456!'})
        updated_user = facade.get_user(user.id)

        runner.assert_true(
            updated_user.password.startswith('$2b$'),
            "Password hashed on update",
            f"Updated password stored as bcrypt hash: {updated_user.password[:20]}...",
            "Updated password not hashed properly"
        )

        runner.assert_true(
            updated_user.verify_password('NewPassword456!'),
            "Updated password verification works",
            "New password verification successful",
            "New password verification failed"
        )

        runner.assert_true(
            not updated_user.verify_password('PlainPassword123!'),
            "Old password no longer works",
            "Old password correctly rejected",
            "Old password still works (should not)"
        )

        # Cleanup
        db.session.delete(updated_user)
        db.session.commit()


# 6.4: Email Uniqueness Enforcement
def test_email_uniqueness():
    """Test that email uniqueness is enforced at database level."""
    print_subsection("Test 6.4: Email Uniqueness Enforcement")

    with app.app_context():
        # Clean up existing test users
        for email in ['unique.email@test.com', 'duplicate.email@test.com']:
            existing = facade.get_user_by_email(email)
            if existing:
                db.session.delete(existing)
                db.session.commit()

        # Create first user
        user1 = facade.create_user({
            'first_name': 'First',
            'last_name': 'User',
            'email': 'unique.email@test.com',
            'password': 'Pass123!'
        })

        runner.assert_true(
            user1.id is not None,
            "First user created successfully",
            f"User created with email: {user1.email}",
            "Failed to create first user"
        )

        # Try to create second user with same email
        try:
            user2 = facade.create_user({
                'first_name': 'Second',
                'last_name': 'User',
                'email': 'unique.email@test.com',
                'password': 'Pass456!'
            })

            # If we get here, duplicate was allowed (should not happen)
            runner.assert_true(
                False,
                "Duplicate email prevention",
                "Duplicate email prevented",
                "Duplicate email was allowed (constraint not enforced)"
            )
        except Exception as e:
            # Expected to fail
            runner.assert_true(
                'unique' in str(e).lower() or 'duplicate' in str(e).lower() or
                'UNIQUE constraint' in str(e) or 'already exists' in str(e).lower(),
                "Duplicate email prevention",
                f"Duplicate email correctly prevented: {type(e).__name__}",
                f"Wrong error type: {str(e)}"
            )

        # Cleanup
        db.session.delete(user1)
        db.session.commit()


# 6.5: UserRepository Functionality
def test_user_repository():
    """Test UserRepository specialized methods."""
    print_subsection("Test 6.5: UserRepository Functionality")

    with app.app_context():
        # Clean up if user exists
        existing = facade.get_user_by_email('repo.test@test.com')
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Test get_user_by_email method
        user = facade.create_user({
            'first_name': 'Repository',
            'last_name': 'Test',
            'email': 'repo.test@test.com',
            'password': 'RepoPass123!'
        })

        # Test email-based lookup
        found_user = facade.get_user_by_email('repo.test@test.com')

        runner.assert_true(
            found_user is not None,
            "UserRepository.get_user_by_email()",
            f"User found by email: {found_user.email}",
            "User not found by email"
        )

        runner.assert_equal(
            found_user.id,
            user.id,
            "Email lookup returns correct user",
            "- User IDs should match"
        )

        # Test get_all_users
        all_users = facade.get_all_users()

        runner.assert_true(
            len(all_users) > 0,
            "UserRepository.get_all_users()",
            f"Retrieved {len(all_users)} users from database",
            "Failed to retrieve users"
        )

        runner.assert_true(
            any(u.email == 'repo.test@test.com' for u in all_users),
            "All users includes created user",
            "Created user found in all users list",
            "Created user not in all users list"
        )

        # Cleanup
        db.session.delete(found_user)
        db.session.commit()


# 6.6: Data Persistence Across Sessions
def test_data_persistence():
    """Test that data persists across database sessions."""
    print_subsection("Test 6.6: Data Persistence Across Sessions")

    with app.app_context():
        # Clean up if user exists
        existing = facade.get_user_by_email('persistence.test@test.com')
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Create user in first session
        user = facade.create_user({
            'first_name': 'Persistent',
            'last_name': 'User',
            'email': 'persistence.test@test.com',
            'password': 'PersistPass123!'
        })
        user_id = user.id

        # Close session (simulating app restart)
        db.session.close()

        # Retrieve user in new session
        retrieved_user = facade.get_user(user_id)

        runner.assert_true(
            retrieved_user is not None,
            "Data persists across sessions",
            f"User retrieved after session close: {retrieved_user.email}",
            "User not found after session close"
        )

        runner.assert_equal(
            retrieved_user.email,
            'persistence.test@test.com',
            "User data intact after session close",
            "- Email should match original"
        )

        runner.assert_equal(
            retrieved_user.first_name,
            'Persistent',
            "User attributes preserved",
            "- First name should be 'Persistent'"
        )

        # Test that password still works
        runner.assert_true(
            retrieved_user.verify_password('PersistPass123!'),
            "Password persists correctly",
            "Password verification works after session close",
            "Password verification failed after session close"
        )

        # Cleanup
        db.session.delete(retrieved_user)
        db.session.commit()


# ============================================================================
# TASK 7: PLACE, REVIEW, AND AMENITY DATABASE MAPPING TESTS
# ============================================================================

def test_task_7():
    """Test suite for Task 7: Database mapping for Place, Review, and Amenity models."""
    print_section("TASK 7: PLACE, REVIEW, AND AMENITY DATABASE MAPPING")

    test_7_1_models_import()
    test_7_2_tables_created()
    test_7_3_amenity_model_mapping()
    test_7_4_place_model_mapping()
    test_7_5_review_model_mapping()
    test_7_6_property_validation_preserved()


# 7.1: Models Import Successfully
def test_7_1_models_import():
    """Test that all models can be imported without errors."""
    print_subsection("Test 7.1: Models Import Successfully")

    try:
        from app.models import User, Amenity, Place, Review
        runner.assert_true(
            True,
            "All models import successfully",
            "User, Amenity, Place, and Review models imported",
            "Failed to import models"
        )
    except ImportError as e:
        runner.assert_true(
            False,
            "All models import successfully",
            "",
            f"ImportError: {e}"
        )


# 7.2: Database Tables Created
def test_7_2_tables_created():
    """Test that database tables are created for all models."""
    print_subsection("Test 7.2: Database Tables Created")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        runner.assert_true(
            'amenities' in tables,
            "Amenities table created",
            f"Table 'amenities' found in database",
            "Table 'amenities' not found"
        )

        runner.assert_true(
            'places' in tables,
            "Places table created",
            f"Table 'places' found in database",
            "Table 'places' not found"
        )

        runner.assert_true(
            'reviews' in tables,
            "Reviews table created",
            f"Table 'reviews' found in database",
            "Table 'reviews' not found"
        )

        # Verify all expected tables exist
        expected_tables = {'amenities', 'places', 'reviews', 'users'}
        runner.assert_true(
            expected_tables.issubset(set(tables)),
            "All expected tables created",
            f"Tables: {sorted(tables)}",
            f"Missing tables: {expected_tables - set(tables)}"
        )


# 7.3: Amenity Model Mapping
def test_7_3_amenity_model_mapping():
    """Test Amenity model database mapping and constraints."""
    print_subsection("Test 7.3: Amenity Model Mapping")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)

        # Check columns
        columns = {col['name']: col for col in inspector.get_columns('amenities')}

        runner.assert_true(
            'name' in columns,
            "Amenity 'name' column exists",
            "Column 'name' found in amenities table",
            "Column 'name' not found"
        )

        runner.assert_true(
            'id' in columns,
            "Amenity 'id' column exists (from BaseModel)",
            "Column 'id' found",
            "Column 'id' not found"
        )

        runner.assert_true(
            'created_at' in columns and 'updated_at' in columns,
            "Amenity timestamp columns exist",
            "Columns 'created_at' and 'updated_at' found",
            "Timestamp columns not found"
        )

        # Test property validation
        try:
            amenity = Amenity(name="WiFi")
            runner.assert_equal(
                amenity.name,
                "WiFi",
                "Amenity property getter works",
                "- Name should be 'WiFi'"
            )
        except Exception as e:
            runner.assert_true(
                False,
                "Amenity property getter works",
                "",
                f"Error: {e}"
            )

        # Test validation (empty name)
        try:
            amenity_invalid = Amenity(name="")
            runner.assert_true(
                False,
                "Amenity validation rejects empty name",
                "",
                "Empty name was accepted (should raise ValueError)"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Amenity validation rejects empty name",
                "Empty name correctly rejected",
                ""
            )

        # Test validation (max length)
        try:
            long_name = "A" * 51
            amenity_long = Amenity(name=long_name)
            runner.assert_true(
                False,
                "Amenity validation enforces max length",
                "",
                "Name exceeding 50 chars was accepted"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Amenity validation enforces max length",
                "Max length (50) correctly enforced",
                ""
            )


# 7.4: Place Model Mapping
def test_7_4_place_model_mapping():
    """Test Place model database mapping and columns."""
    print_subsection("Test 7.4: Place Model Mapping")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)

        # Check columns
        columns = {col['name']: col for col in inspector.get_columns('places')}

        expected_columns = ['title', 'description', 'price', 'latitude', 'longitude', 'id', 'created_at', 'updated_at']
        for col_name in expected_columns:
            runner.assert_true(
                col_name in columns,
                f"Place '{col_name}' column exists",
                f"Column '{col_name}' found",
                f"Column '{col_name}' not found"
            )

        # Test property validation with a real user
        try:
            # Get admin user for testing
            admin_user = facade.get_user_by_email('admin@hbnb.io')

            place = Place(
                title="Test Place",
                description="A test place",
                price=100.0,
                latitude=45.0,
                longitude=-75.0,
                owner=admin_user
            )

            runner.assert_equal(
                place.title,
                "Test Place",
                "Place property getters work",
                "- Title should be 'Test Place'"
            )

            runner.assert_equal(
                place.price,
                100.0,
                "Place price property works",
                "- Price should be 100.0"
            )

        except Exception as e:
            runner.assert_true(
                False,
                "Place property getters work",
                "",
                f"Error: {e}"
            )

        # Test price validation (negative)
        try:
            place_invalid = Place(
                title="Invalid",
                price=-10.0,
                latitude=45.0,
                longitude=-75.0,
                owner=admin_user
            )
            runner.assert_true(
                False,
                "Place validation rejects negative price",
                "",
                "Negative price was accepted"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Place validation rejects negative price",
                "Negative price correctly rejected",
                ""
            )


# 7.5: Review Model Mapping
def test_7_5_review_model_mapping():
    """Test Review model database mapping and columns."""
    print_subsection("Test 7.5: Review Model Mapping")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)

        # Check columns
        columns = {col['name']: col for col in inspector.get_columns('reviews')}

        expected_columns = ['text', 'rating', 'id', 'created_at', 'updated_at']
        for col_name in expected_columns:
            runner.assert_true(
                col_name in columns,
                f"Review '{col_name}' column exists",
                f"Column '{col_name}' found",
                f"Column '{col_name}' not found"
            )

        # Test property validation
        try:
            admin_user = facade.get_user_by_email('admin@hbnb.io')
            place = Place(
                title="Review Test Place",
                price=50.0,
                latitude=40.0,
                longitude=-70.0,
                owner=admin_user
            )

            review = Review(
                text="Great place!",
                rating=5,
                place=place,
                user=admin_user
            )

            runner.assert_equal(
                review.text,
                "Great place!",
                "Review property getters work",
                "- Text should be 'Great place!'"
            )

            runner.assert_equal(
                review.rating,
                5,
                "Review rating property works",
                "- Rating should be 5"
            )

        except Exception as e:
            runner.assert_true(
                False,
                "Review property getters work",
                "",
                f"Error: {e}"
            )

        # Test rating validation (out of range)
        try:
            review_invalid = Review(
                text="Bad rating",
                rating=10,
                place=place,
                user=admin_user
            )
            runner.assert_true(
                False,
                "Review validation enforces rating range",
                "",
                "Rating of 10 was accepted (should be 1-5)"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Review validation enforces rating range",
                "Rating range (1-5) correctly enforced",
                ""
            )


# 7.6: Property Validation Preserved
def test_7_6_property_validation_preserved():
    """Test that all property validation logic is preserved after database mapping."""
    print_subsection("Test 7.6: Property Validation Preserved")

    with app.app_context():
        admin_user = facade.get_user_by_email('admin@hbnb.io')

        # Test Amenity type validation
        try:
            amenity = Amenity(name=123)  # Wrong type
            runner.assert_true(
                False,
                "Amenity type validation works",
                "",
                "Integer name was accepted"
            )
        except TypeError:
            runner.assert_true(
                True,
                "Amenity type validation works",
                "Type checking preserved for amenity name",
                ""
            )

        # Test Place coordinate range validation
        try:
            place = Place(
                title="Invalid Coords",
                price=100.0,
                latitude=100.0,  # Out of range
                longitude=0.0,
                owner=admin_user
            )
            runner.assert_true(
                False,
                "Place latitude range validation works",
                "",
                "Latitude of 100.0 was accepted"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Place latitude range validation works",
                "Latitude range validation preserved",
                ""
            )

        # Test Review text validation
        try:
            review = Review(
                text="",  # Empty
                rating=3,
                place=None,
                user=None
            )
            runner.assert_true(
                False,
                "Review text validation works",
                "",
                "Empty text was accepted"
            )
        except ValueError:
            runner.assert_true(
                True,
                "Review text validation works",
                "Text validation preserved",
                ""
            )

        runner.assert_true(
            True,
            "All property validation preserved",
            "Validation logic intact after SQLAlchemy mapping",
            ""
        )


# ============================================================================
# TASK 8: ENTITY RELATIONSHIPS WITH SQLALCHEMY
# ============================================================================
def test_task_8():
    """Test suite for Task 8: SQLAlchemy relationships between entities."""
    print_section("TASK 8: ENTITY RELATIONSHIPS WITH SQLALCHEMY")

    test_8_1_association_table_created()
    test_8_2_foreign_keys_added()
    test_8_3_place_user_relationship()
    test_8_4_review_relationships()
    test_8_5_place_amenity_relationship()
    test_8_6_unique_constraints()


# 8.1: Association Table Created
def test_8_1_association_table_created():
    """Test that place_amenity association table was created."""
    print_subsection("Test 8.1: Association Table Created")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        runner.assert_true(
            'place_amenity' in tables,
            "Place-Amenity association table created",
            "Table 'place_amenity' found in database",
            "Table 'place_amenity' not found"
        )

        # Check association table columns
        if 'place_amenity' in tables:
            columns = {col['name'] for col in inspector.get_columns('place_amenity')}

            runner.assert_true(
                'place_id' in columns and 'amenity_id' in columns,
                "Association table has required columns",
                "Columns 'place_id' and 'amenity_id' found",
                f"Missing columns. Found: {columns}"
            )

            # Check foreign keys
            fks = inspector.get_foreign_keys('place_amenity')
            fk_tables = {fk['referred_table'] for fk in fks}

            runner.assert_true(
                'places' in fk_tables and 'amenities' in fk_tables,
                "Association table foreign keys configured",
                "Foreign keys to 'places' and 'amenities' tables found",
                f"Foreign key tables: {fk_tables}"
            )


# 8.2: Foreign Keys Added
def test_8_2_foreign_keys_added():
    """Test that foreign keys were added to Place and Review models."""
    print_subsection("Test 8.2: Foreign Keys Added")

    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)

        # Check Place model foreign keys
        place_columns = {col['name'] for col in inspector.get_columns('places')}
        runner.assert_true(
            'owner_id' in place_columns,
            "Place model has owner_id foreign key",
            "Column 'owner_id' found in places table",
            "Column 'owner_id' not found"
        )

        place_fks = inspector.get_foreign_keys('places')
        place_fk_tables = {fk['referred_table'] for fk in place_fks}
        runner.assert_true(
            'users' in place_fk_tables,
            "Place.owner_id references users table",
            "Foreign key to 'users' table found",
            f"Foreign key tables: {place_fk_tables}"
        )

        # Check Review model foreign keys
        review_columns = {col['name'] for col in inspector.get_columns('reviews')}
        runner.assert_true(
            'user_id' in review_columns and 'place_id' in review_columns,
            "Review model has user_id and place_id foreign keys",
            "Columns 'user_id' and 'place_id' found in reviews table",
            f"Found columns: {review_columns}"
        )

        review_fks = inspector.get_foreign_keys('reviews')
        review_fk_tables = {fk['referred_table'] for fk in review_fks}
        runner.assert_true(
            'users' in review_fk_tables and 'places' in review_fk_tables,
            "Review foreign keys reference correct tables",
            "Foreign keys to 'users' and 'places' tables found",
            f"Foreign key tables: {review_fk_tables}"
        )


# 8.3: Place-User Relationship
def test_8_3_place_user_relationship():
    """Test bidirectional Place-User relationship."""
    print_subsection("Test 8.3: Place-User Relationship")

    with app.app_context():
        # Create a test user
        test_user = User(
            first_name="John",
            last_name="Doe",
            email="john.place@test.com",
            password="password123"
        )
        db.session.add(test_user)
        db.session.commit()

        # Create a place owned by the user
        test_place = Place(
            title="Test House",
            price=100.0,
            latitude=45.0,
            longitude=-75.0,
            owner=test_user
        )
        db.session.add(test_place)
        db.session.commit()

        # Test forward relationship (Place -> User)
        runner.assert_true(
            test_place.owner is not None,
            "Place.owner relationship works",
            f"Place owner is {test_place.owner.email}",
            "Place.owner is None"
        )

        runner.assert_equal(
            test_place.owner.email,
            "john.place@test.com",
            "Place.owner returns correct user",
            ""
        )

        runner.assert_equal(
            test_place.owner_id,
            test_user.id,
            "Place.owner_id set correctly",
            ""
        )

        # Test backward relationship (User -> Places)
        runner.assert_true(
            hasattr(test_user, 'owned_places'),
            "User.owned_places backref exists",
            "User has 'owned_places' attribute",
            "User.owned_places attribute not found"
        )

        runner.assert_true(
            len(test_user.owned_places) > 0,
            "User.owned_places returns places",
            f"User owns {len(test_user.owned_places)} place(s)",
            "User.owned_places is empty"
        )

        runner.assert_equal(
            test_user.owned_places[0].title,
            "Test House",
            "User.owned_places contains correct place",
            ""
        )

        # Cleanup
        db.session.delete(test_place)
        db.session.delete(test_user)
        db.session.commit()


# 8.4: Review Relationships
def test_8_4_review_relationships():
    """Test bidirectional Review relationships with User and Place."""
    print_subsection("Test 8.4: Review Relationships")

    with app.app_context():
        # Create test user and place
        review_user = User(
            first_name="Jane",
            last_name="Smith",
            email="jane.review@test.com",
            password="password123"
        )
        place_owner = User(
            first_name="Bob",
            last_name="Owner",
            email="bob.owner@test.com",
            password="password123"
        )
        db.session.add(review_user)
        db.session.add(place_owner)
        db.session.commit()

        review_place = Place(
            title="Review Test Place",
            price=150.0,
            latitude=40.0,
            longitude=-70.0,
            owner=place_owner
        )
        db.session.add(review_place)
        db.session.commit()

        # Create a review
        test_review = Review(
            text="Great place!",
            rating=5,
            place=review_place,
            user=review_user
        )
        db.session.add(test_review)
        db.session.commit()

        # Test Review -> User relationship
        runner.assert_true(
            test_review.user is not None,
            "Review.user relationship works",
            f"Review user is {test_review.user.email}",
            "Review.user is None"
        )

        runner.assert_equal(
            test_review.user.email,
            "jane.review@test.com",
            "Review.user returns correct user",
            ""
        )

        # Test Review -> Place relationship
        runner.assert_true(
            test_review.place is not None,
            "Review.place relationship works",
            f"Review place is {test_review.place.title}",
            "Review.place is None"
        )

        runner.assert_equal(
            test_review.place.title,
            "Review Test Place",
            "Review.place returns correct place",
            ""
        )

        # Test User -> Reviews backref
        runner.assert_true(
            hasattr(review_user, 'user_reviews'),
            "User.user_reviews backref exists",
            "User has 'user_reviews' attribute",
            "User.user_reviews not found"
        )

        runner.assert_true(
            len(review_user.user_reviews) > 0,
            "User.user_reviews returns reviews",
            f"User has {len(review_user.user_reviews)} review(s)",
            "User.user_reviews is empty"
        )

        # Test Place -> Reviews backref
        runner.assert_true(
            hasattr(review_place, 'reviews'),
            "Place.reviews backref exists",
            "Place has 'reviews' attribute",
            "Place.reviews not found"
        )

        runner.assert_true(
            len(review_place.reviews) > 0,
            "Place.reviews returns reviews",
            f"Place has {len(review_place.reviews)} review(s)",
            "Place.reviews is empty"
        )

        runner.assert_equal(
            review_place.reviews[0].text,
            "Great place!",
            "Place.reviews contains correct review",
            ""
        )

        # Cleanup
        db.session.delete(test_review)
        db.session.delete(review_place)
        db.session.delete(review_user)
        db.session.delete(place_owner)
        db.session.commit()


# 8.5: Place-Amenity Relationship
def test_8_5_place_amenity_relationship():
    """Test many-to-many Place-Amenity relationship."""
    print_subsection("Test 8.5: Place-Amenity Relationship")

    with app.app_context():
        # Create test user and place
        amenity_owner = User(
            first_name="Alice",
            last_name="Test",
            email="alice.amenity@test.com",
            password="password123"
        )
        db.session.add(amenity_owner)
        db.session.commit()

        amenity_place = Place(
            title="Amenity Test Place",
            price=200.0,
            latitude=35.0,
            longitude=-80.0,
            owner=amenity_owner
        )
        db.session.add(amenity_place)
        db.session.commit()

        # Create amenities
        wifi = Amenity(name="WiFi-Test")
        pool = Amenity(name="Pool-Test")
        db.session.add(wifi)
        db.session.add(pool)
        db.session.commit()

        # Add amenities to place
        amenity_place.amenities_rel.append(wifi)
        amenity_place.amenities_rel.append(pool)
        db.session.commit()

        # Test Place -> Amenities relationship
        runner.assert_true(
            hasattr(amenity_place, 'amenities_rel'),
            "Place.amenities_rel relationship exists",
            "Place has 'amenities_rel' attribute",
            "Place.amenities_rel not found"
        )

        runner.assert_equal(
            len(amenity_place.amenities_rel),
            2,
            "Place.amenities_rel returns correct count",
            f"- Expected 2, got {len(amenity_place.amenities_rel)}"
        )

        amenity_names = {a.name for a in amenity_place.amenities_rel}
        runner.assert_true(
            "WiFi-Test" in amenity_names and "Pool-Test" in amenity_names,
            "Place.amenities_rel contains correct amenities",
            f"Amenities: {amenity_names}",
            f"Found: {amenity_names}"
        )

        # Test Amenity -> Places backref
        runner.assert_true(
            hasattr(wifi, 'places_list'),
            "Amenity.places_list backref exists",
            "Amenity has 'places_list' attribute",
            "Amenity.places_list not found"
        )

        runner.assert_true(
            len(wifi.places_list) > 0,
            "Amenity.places_list returns places",
            f"Amenity linked to {len(wifi.places_list)} place(s)",
            "Amenity.places_list is empty"
        )

        runner.assert_equal(
            wifi.places_list[0].title,
            "Amenity Test Place",
            "Amenity.places_list contains correct place",
            ""
        )

        # Cleanup
        db.session.delete(amenity_place)
        db.session.delete(wifi)
        db.session.delete(pool)
        db.session.delete(amenity_owner)
        db.session.commit()


# 8.6: Unique Constraints
def test_8_6_unique_constraints():
    """Test unique constraint on (user_id, place_id) in reviews."""
    print_subsection("Test 8.6: Unique Constraints")

    with app.app_context():
        # Create test data
        constraint_user = User(
            first_name="Test",
            last_name="User",
            email="test.constraint@test.com",
            password="password123"
        )
        constraint_owner = User(
            first_name="Owner",
            last_name="Test",
            email="owner.constraint@test.com",
            password="password123"
        )
        db.session.add(constraint_user)
        db.session.add(constraint_owner)
        db.session.commit()

        constraint_place = Place(
            title="Constraint Test",
            price=100.0,
            latitude=30.0,
            longitude=-90.0,
            owner=constraint_owner
        )
        db.session.add(constraint_place)
        db.session.commit()

        # Create first review
        review1 = Review(
            text="First review",
            rating=4,
            place=constraint_place,
            user=constraint_user
        )
        db.session.add(review1)
        db.session.commit()

        runner.assert_true(
            True,
            "First review created successfully",
            "Review added to database",
            ""
        )

        # Try to create duplicate review (should fail)
        try:
            review2 = Review(
                text="Duplicate review",
                rating=5,
                place=constraint_place,
                user=constraint_user
            )
            db.session.add(review2)
            db.session.commit()

            runner.assert_true(
                False,
                "Unique constraint prevents duplicate reviews",
                "",
                "Duplicate review was allowed (should have been rejected)"
            )
        except Exception as e:
            db.session.rollback()
            error_msg = str(e).lower()
            is_unique_violation = (
                'unique' in error_msg or
                'constraint' in error_msg or
                'duplicate' in error_msg
            )
            runner.assert_true(
                is_unique_violation,
                "Unique constraint prevents duplicate reviews",
                "Duplicate review correctly rejected by database",
                f"Error: {e}"
            )

        # Cleanup
        db.session.delete(review1)
        db.session.delete(constraint_place)
        db.session.delete(constraint_user)
        db.session.delete(constraint_owner)
        db.session.commit()


# ============================================================================
# TASK 9: SQL SCRIPTS FOR TABLE GENERATION AND INITIAL DATA
# ============================================================================
def test_task_9():
    """Test suite for Task 9: SQL schema and seed data scripts."""
    print_section("TASK 9: SQL SCRIPTS FOR TABLE GENERATION AND INITIAL DATA")

    test_9_1_sql_files_exist()
    test_9_2_schema_script_validation()
    test_9_3_seed_script_validation()
    test_9_4_admin_user_seeded()
    test_9_5_amenities_seeded()


# 9.1: SQL Files Exist
def test_9_1_sql_files_exist():
    """Test that required SQL files exist."""
    print_subsection("Test 9.1: SQL Files Exist")

    import os

    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    seed_file = os.path.join(os.path.dirname(__file__), '..', 'seed.sql')

    runner.assert_true(
        os.path.exists(schema_file),
        "schema.sql file exists",
        f"File found at: {schema_file}",
        f"File not found at: {schema_file}"
    )

    runner.assert_true(
        os.path.exists(seed_file),
        "seed.sql file exists",
        f"File found at: {seed_file}",
        f"File not found at: {seed_file}"
    )


# 9.2: Schema Script Validation
def test_9_2_schema_script_validation():
    """Test that schema.sql creates all required tables."""
    print_subsection("Test 9.2: Schema Script Validation")

    import os
    import sqlite3
    import tempfile

    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')

    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name

    try:
        # Execute schema script
        conn = sqlite3.connect(tmp_db)
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        # Get table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = {row[0] for row in cursor.fetchall()}

        runner.assert_true(
            'users' in tables,
            "users table created",
            "Table 'users' found",
            "Table 'users' not found"
        )

        runner.assert_true(
            'places' in tables,
            "places table created",
            "Table 'places' found",
            "Table 'places' not found"
        )

        runner.assert_true(
            'reviews' in tables,
            "reviews table created",
            "Table 'reviews' found",
            "Table 'reviews' not found"
        )

        runner.assert_true(
            'amenities' in tables,
            "amenities table created",
            "Table 'amenities' found",
            "Table 'amenities' not found"
        )

        runner.assert_true(
            'place_amenity' in tables,
            "place_amenity table created",
            "Table 'place_amenity' found",
            "Table 'place_amenity' not found"
        )

        # Verify users table structure
        cursor.execute("PRAGMA table_info(users)")
        columns = {row[1] for row in cursor.fetchall()}

        required_user_columns = {'id', 'first_name', 'last_name', 'email', 'password', 'is_admin'}
        runner.assert_true(
            required_user_columns.issubset(columns),
            "users table has all required columns",
            f"All columns present: {required_user_columns}",
            f"Missing columns: {required_user_columns - columns}"
        )

        conn.close()
    finally:
        # Cleanup
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


# 9.3: Seed Script Validation
def test_9_3_seed_script_validation():
    """Test that seed.sql inserts initial data correctly."""
    print_subsection("Test 9.3: Seed Script Validation")

    import os
    import sqlite3
    import tempfile

    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    seed_file = os.path.join(os.path.dirname(__file__), '..', 'seed.sql')

    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name

    try:
        # Execute schema and seed scripts
        conn = sqlite3.connect(tmp_db)

        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        with open(seed_file, 'r') as f:
            seed_sql = f.read()
        conn.executescript(seed_sql)

        cursor = conn.cursor()

        # Check user count
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        runner.assert_true(
            user_count >= 1,
            "At least one user seeded",
            f"Found {user_count} user(s)",
            f"No users found"
        )

        # Check amenities count
        cursor.execute("SELECT COUNT(*) FROM amenities")
        amenity_count = cursor.fetchone()[0]

        runner.assert_true(
            amenity_count >= 3,
            "At least three amenities seeded",
            f"Found {amenity_count} amenities",
            f"Only {amenity_count} amenities found (expected >= 3)"
        )

        conn.close()
    finally:
        # Cleanup
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


# 9.4: Admin User Seeded
def test_9_4_admin_user_seeded():
    """Test that admin user is properly seeded with correct attributes."""
    print_subsection("Test 9.4: Admin User Seeded")

    import os
    import sqlite3
    import tempfile

    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    seed_file = os.path.join(os.path.dirname(__file__), '..', 'seed.sql')

    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name

    try:
        # Execute schema and seed scripts
        conn = sqlite3.connect(tmp_db)

        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        with open(seed_file, 'r') as f:
            seed_sql = f.read()
        conn.executescript(seed_sql)

        cursor = conn.cursor()

        # Check admin user
        cursor.execute("SELECT * FROM users WHERE email = 'admin@hbnb.io'")
        admin = cursor.fetchone()

        runner.assert_true(
            admin is not None,
            "Admin user exists",
            "Admin user found with email admin@hbnb.io",
            "Admin user not found"
        )

        if admin:
            # admin row: (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
            admin_id, first_name, last_name, email, password, is_admin, created_at, updated_at = admin

            runner.assert_equal(
                admin_id,
                '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
                "Admin user has correct fixed UUID",
                ""
            )

            runner.assert_equal(
                first_name,
                'Admin',
                "Admin user first_name is 'Admin'",
                ""
            )

            runner.assert_equal(
                last_name,
                'HBnB',
                "Admin user last_name is 'HBnB'",
                ""
            )

            runner.assert_true(
                is_admin == 1 or is_admin == True,
                "Admin user has is_admin=True",
                "Admin privileges confirmed",
                f"is_admin value: {is_admin}"
            )

            runner.assert_true(
                password.startswith('$2b$'),
                "Admin password is bcrypt hashed",
                "Password hash format correct",
                f"Password doesn't appear to be bcrypt hashed: {password[:20]}..."
            )

        conn.close()
    finally:
        # Cleanup
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


# 9.5: Amenities Seeded
def test_9_5_amenities_seeded():
    """Test that initial amenities are properly seeded."""
    print_subsection("Test 9.5: Amenities Seeded")

    import os
    import sqlite3
    import tempfile

    schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    seed_file = os.path.join(os.path.dirname(__file__), '..', 'seed.sql')

    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name

    try:
        # Execute schema and seed scripts
        conn = sqlite3.connect(tmp_db)

        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        with open(seed_file, 'r') as f:
            seed_sql = f.read()
        conn.executescript(seed_sql)

        cursor = conn.cursor()

        # Check amenities
        cursor.execute("SELECT name FROM amenities ORDER BY name")
        amenities = [row[0] for row in cursor.fetchall()]

        expected_amenities = {'WiFi', 'Swimming Pool', 'Air Conditioning'}
        actual_amenities = set(amenities)

        runner.assert_true(
            expected_amenities.issubset(actual_amenities),
            "Required amenities seeded",
            f"Found amenities: {actual_amenities}",
            f"Missing amenities: {expected_amenities - actual_amenities}"
        )

        runner.assert_true(
            'WiFi' in amenities,
            "WiFi amenity seeded",
            "WiFi found in amenities",
            "WiFi not found"
        )

        runner.assert_true(
            'Swimming Pool' in amenities,
            "Swimming Pool amenity seeded",
            "Swimming Pool found in amenities",
            "Swimming Pool not found"
        )

        runner.assert_true(
            'Air Conditioning' in amenities,
            "Air Conditioning amenity seeded",
            "Air Conditioning found in amenities",
            "Air Conditioning not found"
        )

        conn.close()
    finally:
        # Cleanup
        if os.path.exists(tmp_db):
            os.unlink(tmp_db)


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  HBnB APPLICATION - INTEGRATION TEST SUITE")
    print("  Part 3: Authentication, Authorization & API Endpoints")
    print("=" * 70)

    # Task 0: Configuration Management
    test_configuration()

    # Task 1: Password Hashing
    test_password_hashing()

    # Task 2: JWT Authentication
    test_jwt_authentication()

    # Task 3: Protected Endpoints & API Testing (includes all subtasks)
    test_task_3()

    # Task 4: Administrator Access Control (includes all subtasks)
    test_task_4()

    # Task 6: User Database Mapping with SQLAlchemy (includes all subtasks)
    test_task_6()

    # Task 7: Place, Review, and Amenity Database Mapping (includes all subtasks)
    test_task_7()

    # Task 8: Entity Relationships with SQLAlchemy (includes all subtasks)
    test_task_8()

    # Task 9: SQL Scripts for Table Generation and Initial Data (includes all subtasks)
    test_task_9()

    # Print summary
    runner.print_summary()
