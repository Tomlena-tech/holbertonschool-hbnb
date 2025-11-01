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
"""

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

    # Print summary
    runner.print_summary()
