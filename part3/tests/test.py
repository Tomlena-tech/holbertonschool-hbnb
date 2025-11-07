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
"""

import sys
import os

# Add parent directory to Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models.user import User
from app.services import facade


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

    # Print summary
    runner.print_summary()
