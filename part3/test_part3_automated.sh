#!/bin/bash

# 🧪 Script de Test Automatisé - HBnB Part 3
# Usage: ./test_part3_automated.sh

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Base URL
BASE_URL="http://localhost:5000/api/v1"

# Test function
test_case() {
    local test_name="$1"
    local expected_status="$2"
    local response="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Extract status code from response
    status=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$status" -eq "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $test_name (Status: $status)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} - $test_name (Expected: $expected_status, Got: $status)"
        echo "   Response: $body"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🧪 HBnB Part 3 - Automated Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if server is running
echo -e "${YELLOW}🔍 Checking if server is running...${NC}"
if ! curl -s http://localhost:5000/ > /dev/null; then
    echo -e "${RED}❌ Server is not running!${NC}"
    echo "Please start the server with: cd part3/hbnb && python run.py"
    exit 1
fi
echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# ============================================
# AUTHENTICATION TESTS
# ============================================
echo -e "${BLUE}🔐 AUTHENTICATION TESTS${NC}"
echo ""

# TEST 1: Login with admin
echo -e "${YELLOW}TEST 1: Login with admin credentials${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@hbnb.com",
        "password": "admin123"
    }')

test_case "Admin login" 200 "$RESPONSE"

# Extract admin token
ADMIN_TOKEN=$(echo "$RESPONSE" | head -n -1 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}❌ Failed to get admin token${NC}"
    exit 1
fi
echo -e "${GREEN}   Token obtained: ${ADMIN_TOKEN:0:20}...${NC}"
echo ""

# TEST 2: Login with wrong password
echo -e "${YELLOW}TEST 2: Login with wrong password${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@hbnb.com",
        "password": "wrongpassword"
    }')

test_case "Wrong password rejection" 401 "$RESPONSE"
echo ""

# TEST 3: Login with non-existent email
echo -e "${YELLOW}TEST 3: Login with non-existent email${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "notexist@test.com",
        "password": "anything"
    }')

test_case "Non-existent email rejection" 401 "$RESPONSE"
echo ""

# ============================================
# AUTHORIZATION TESTS
# ============================================
echo -e "${BLUE}🛡️  AUTHORIZATION TESTS${NC}"
echo ""

# TEST 4: Create user without token (should fail)
echo -e "${YELLOW}TEST 4: Create user without authentication${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Test",
        "last_name": "NoAuth",
        "email": "noauth@test.com",
        "password": "password123"
    }')

test_case "Reject user creation without auth" 401 "$RESPONSE"
echo ""

# TEST 5: Create user with admin token (should succeed)
echo -e "${YELLOW}TEST 5: Create user with admin token${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe.test@test.com",
        "password": "password123",
        "is_admin": false
    }')

test_case "Admin creates user" 201 "$RESPONSE"

# Extract user ID
USER_ID=$(echo "$RESPONSE" | head -n -1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   User created with ID: $USER_ID${NC}"
echo ""

# TEST 6: Login with newly created user
echo -e "${YELLOW}TEST 6: Login with new user${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "john.doe.test@test.com",
        "password": "password123"
    }')

test_case "New user login" 200 "$RESPONSE"

# Extract user token
USER_TOKEN=$(echo "$RESPONSE" | head -n -1 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   User token obtained${NC}"
echo ""

# TEST 7: Regular user tries to create another user (should fail)
echo -e "${YELLOW}TEST 7: Regular user tries to create user${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@test.com",
        "password": "password123"
    }')

test_case "Reject non-admin user creation" 403 "$RESPONSE"
echo ""

# ============================================
# CRUD TESTS - PLACES
# ============================================
echo -e "${BLUE}🏠 CRUD TESTS - PLACES${NC}"
echo ""

# TEST 8: Create place
echo -e "${YELLOW}TEST 8: Create a place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Test Apartment Paris",
        "description": "Beautiful apartment in Paris",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Create place" 201 "$RESPONSE"

# Extract place ID
PLACE_ID=$(echo "$RESPONSE" | head -n -1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   Place created with ID: $PLACE_ID${NC}"
echo ""

# TEST 9: Get place by ID
echo -e "${YELLOW}TEST 9: Get place by ID${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/places/$PLACE_ID)

test_case "Get place by ID" 200 "$RESPONSE"
echo ""

# TEST 10: List all places
echo -e "${YELLOW}TEST 10: List all places${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/places/)

test_case "List all places" 200 "$RESPONSE"
echo ""

# TEST 11: Update place
echo -e "${YELLOW}TEST 11: Update place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/places/$PLACE_ID \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Updated Paris Apartment",
        "description": "Renovated apartment",
        "price": 150.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Update place" 200 "$RESPONSE"
echo ""

# ============================================
# CRUD TESTS - AMENITIES
# ============================================
echo -e "${BLUE}🛋️  CRUD TESTS - AMENITIES${NC}"
echo ""

# TEST 12: Create amenity
echo -e "${YELLOW}TEST 12: Create amenity (WiFi)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/amenities/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "WiFi Test"
    }')

test_case "Create amenity" 201 "$RESPONSE"

# Extract amenity ID
AMENITY_ID=$(echo "$RESPONSE" | head -n -1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   Amenity created with ID: $AMENITY_ID${NC}"
echo ""

# TEST 13: List amenities
echo -e "${YELLOW}TEST 13: List all amenities${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/amenities/)

test_case "List amenities" 200 "$RESPONSE"
echo ""

# ============================================
# CRUD TESTS - REVIEWS
# ============================================
echo -e "${BLUE}⭐ CRUD TESTS - REVIEWS${NC}"
echo ""

# Create second user for review (owner can't review own place)
echo -e "${YELLOW}Creating second user for review tests...${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Alice",
        "last_name": "Reviewer",
        "email": "alice.reviewer@test.com",
        "password": "password123",
        "is_admin": false
    }')

USER2_ID=$(echo "$RESPONSE" | head -n -1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)

# Login with second user
RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "alice.reviewer@test.com",
        "password": "password123"
    }')

USER2_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   Second user created and logged in${NC}"
echo ""

# TEST 14: Create review
echo -e "${YELLOW}TEST 14: Create review${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Great place, highly recommended!",
        "rating": 5,
        "place_id": "'$PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Create review" 201 "$RESPONSE"

REVIEW_ID=$(echo "$RESPONSE" | head -n -1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "${GREEN}   Review created with ID: $REVIEW_ID${NC}"
echo ""

# ============================================
# BUSINESS RULES TESTS
# ============================================
echo -e "${BLUE}📏 BUSINESS RULES TESTS${NC}"
echo ""

# TEST 15: Owner cannot review own place
echo -e "${YELLOW}TEST 15: Owner tries to review own place (should fail)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "text": "My own place is great!",
        "rating": 5,
        "place_id": "'$PLACE_ID'",
        "user_id": "'$USER_ID'"
    }')

test_case "Reject owner self-review" 400 "$RESPONSE"
echo ""

# TEST 16: Cannot review same place twice
echo -e "${YELLOW}TEST 16: User tries to review same place twice (should fail)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Another review for same place",
        "rating": 4,
        "place_id": "'$PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject duplicate review" 400 "$RESPONSE"
echo ""

# ============================================
# VALIDATION TESTS
# ============================================
echo -e "${BLUE}✅ VALIDATION TESTS${NC}"
echo ""

# TEST 17: Invalid email format
echo -e "${YELLOW}TEST 17: Create user with invalid email${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Invalid",
        "last_name": "Email",
        "email": "not-an-email",
        "password": "password123"
    }')

test_case "Reject invalid email" 400 "$RESPONSE"
echo ""

# TEST 18: Rating out of range
echo -e "${YELLOW}TEST 18: Create review with rating > 5${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Review with invalid rating",
        "rating": 10,
        "place_id": "'$PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject rating > 5" 400 "$RESPONSE"
echo ""

# TEST 19: Negative price
echo -e "${YELLOW}TEST 19: Create place with negative price${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Negative Price Place",
        "price": -50,
        "latitude": 48.0,
        "longitude": 2.0,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject negative price" 400 "$RESPONSE"
echo ""

# ============================================
# CLEANUP TESTS (DELETE)
# ============================================
echo -e "${BLUE}🗑️  DELETE TESTS${NC}"
echo ""

# TEST 20: Delete review
echo -e "${YELLOW}TEST 20: Delete review${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/reviews/$REVIEW_ID \
    -H "Authorization: Bearer $USER2_TOKEN")

test_case "Delete review" 200 "$RESPONSE"
echo ""

# TEST 21: Delete place
echo -e "${YELLOW}TEST 21: Delete place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/places/$PLACE_ID \
    -H "Authorization: Bearer $USER_TOKEN")

test_case "Delete place" 200 "$RESPONSE"
echo ""

# ============================================
# SUMMARY
# ============================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 TEST SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total Tests:  ${TOTAL_TESTS}"
echo -e "${GREEN}Passed:       ${PASSED_TESTS}${NC}"
echo -e "${RED}Failed:       ${FAILED_TESTS}${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Part 3 is fully functional!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
