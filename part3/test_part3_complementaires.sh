#!/bin/bash

# ============================================
# HBnB Part 3 - Tests Complémentaires
# ============================================
# Tests avancés pour cas limites, validation,
# règles métier complexes et intégrité des données

BASE_URL="http://127.0.0.1:5000/api/v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Helper function to test responses
test_case() {
    local description=$1
    local expected_status=$2
    local response=$3

    local status_code=$(echo "$response" | tail -n 1)
    local body=$(echo "$response" | sed '$d')

    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} - $description (Status: $status_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} - $description (Expected: $expected_status, Got: $status_code)"
        echo "   Response: $body"
        ((FAILED++))
        return 1
    fi
}

# Check if server is running
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🧪 HBnB Part 3 - Tests Complémentaires${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}🔍 Checking if server is running...${NC}"
if ! curl -s http://127.0.0.1:5000/ > /dev/null 2>&1; then
    echo -e "${RED}❌ Server is not running!${NC}"
    echo "Please start the server with: cd part3/hbnb && python run.py"
    exit 1
fi
echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# ============================================
# SETUP: Login as admin and create test data
# ============================================
echo -e "${BLUE}⚙️  SETUP: Creating test environment${NC}"
echo ""

# Login as admin
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@hbnb.com",
        "password": "admin123"
    }')

ADMIN_TOKEN=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"access_token" *: *"\([^"]*\)".*/\1/p')

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}❌ Failed to get admin token${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Admin authenticated${NC}"

# Create test user
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Test",
        "last_name": "User",
        "email": "test.complementaire@test.com",
        "password": "test123"
    }')

USER_ID=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"id" *: *"\([^"]*\)".*/\1/p')

# Login as test user
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "test.complementaire@test.com",
        "password": "test123"
    }')

USER_TOKEN=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"access_token" *: *"\([^"]*\)".*/\1/p')

echo -e "${GREEN}✅ Test user created and authenticated${NC}"

# Create second test user
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Another",
        "last_name": "User",
        "email": "another.user@test.com",
        "password": "test456"
    }')

USER2_ID=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"id" *: *"\([^"]*\)".*/\1/p')

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "another.user@test.com",
        "password": "test456"
    }')

USER2_TOKEN=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"access_token" *: *"\([^"]*\)".*/\1/p')

echo -e "${GREEN}✅ Second test user created${NC}"
echo ""

# ============================================
# VALIDATION TESTS - EDGE CASES
# ============================================
echo -e "${BLUE}📋 VALIDATION TESTS - CAS LIMITES${NC}"
echo ""

# TEST 1: Create user with empty first name
echo -e "${YELLOW}TEST 1: Create user with empty first name${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "",
        "last_name": "Test",
        "email": "empty.first@test.com",
        "password": "test123"
    }')

test_case "Reject empty first name" 400 "$RESPONSE"
echo ""

# TEST 2: Create user with too short password
echo -e "${YELLOW}TEST 2: Create user with password too short${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Test",
        "last_name": "User",
        "email": "short.pass@test.com",
        "password": "123"
    }')

test_case "Reject password < 6 characters" 400 "$RESPONSE"
echo ""

# TEST 3: Create user with very long name
echo -e "${YELLOW}TEST 3: Create user with very long first name${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "ThisIsAVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongName",
        "last_name": "Test",
        "email": "long.name@test.com",
        "password": "test123"
    }')

test_case "Reject name > 50 characters" 400 "$RESPONSE"
echo ""

# TEST 4: Create place with negative price
echo -e "${YELLOW}TEST 4: Create place with negative price${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Test Place",
        "description": "Test",
        "price": -50.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject negative price" 400 "$RESPONSE"
echo ""

# TEST 5: Create place with invalid latitude
echo -e "${YELLOW}TEST 5: Create place with invalid latitude (> 90)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Invalid Coords",
        "description": "Test",
        "price": 100.0,
        "latitude": 95.0,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject latitude > 90" 400 "$RESPONSE"
echo ""

# TEST 6: Create place with invalid longitude
echo -e "${YELLOW}TEST 6: Create place with invalid longitude (< -180)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Invalid Coords",
        "description": "Test",
        "price": 100.0,
        "latitude": 45.0,
        "longitude": -190.0,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject longitude < -180" 400 "$RESPONSE"
echo ""

# TEST 7: Create review with rating > 5
echo -e "${YELLOW}TEST 7: Create review with rating > 5${NC}"

# First create a place for testing reviews
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Review Test Place",
        "description": "For testing reviews",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

TEST_PLACE_ID=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"id" *: *"\([^"]*\)".*/\1/p')

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Great place!",
        "rating": 6,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject rating > 5" 400 "$RESPONSE"
echo ""

# TEST 8: Create review with rating < 1
echo -e "${YELLOW}TEST 8: Create review with rating < 1${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Bad place!",
        "rating": 0,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject rating < 1" 400 "$RESPONSE"
echo ""

# TEST 9: Create review with empty text
echo -e "${YELLOW}TEST 9: Create review with empty text${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "",
        "rating": 5,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject empty review text" 400 "$RESPONSE"
echo ""

# ============================================
# BUSINESS RULES TESTS
# ============================================
echo -e "${BLUE}🏛️  BUSINESS RULES TESTS${NC}"
echo ""

# TEST 10: Owner tries to review own place
echo -e "${YELLOW}TEST 10: Owner reviews their own place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "text": "My own place is great!",
        "rating": 5,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER_ID'"
    }')

test_case "Reject owner reviewing own place" 400 "$RESPONSE"
echo ""

# TEST 11: Create valid review first time
echo -e "${YELLOW}TEST 11: Create valid review (first time)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Nice place, enjoyed my stay!",
        "rating": 4,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Create valid review" 201 "$RESPONSE"

REVIEW_ID=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"id" *: *"\([^"]*\)".*/\1/p')
echo ""

# TEST 12: Try to create duplicate review
echo -e "${YELLOW}TEST 12: User tries to review same place twice${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "text": "Another review for same place",
        "rating": 3,
        "place_id": "'$TEST_PLACE_ID'",
        "user_id": "'$USER2_ID'"
    }')

test_case "Reject duplicate review" 400 "$RESPONSE"
echo ""

# ============================================
# AUTHORIZATION TESTS - ADVANCED
# ============================================
echo -e "${BLUE}🔐 AUTHORIZATION TESTS - AVANCÉS${NC}"
echo ""

# TEST 13: User tries to update another user's place
echo -e "${YELLOW}TEST 13: User tries to update another user's place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/places/$TEST_PLACE_ID \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER2_TOKEN" \
    -d '{
        "title": "Hacked Place",
        "description": "I modified your place!",
        "price": 1.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject non-owner place update" 403 "$RESPONSE"
echo ""

# TEST 14: User tries to delete another user's review
echo -e "${YELLOW}TEST 14: User tries to delete another user's review${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/reviews/$REVIEW_ID \
    -H "Authorization: Bearer $USER_TOKEN")

test_case "Reject non-owner review deletion" 403 "$RESPONSE"
echo ""

# TEST 15: Request without token
echo -e "${YELLOW}TEST 15: Create place without authentication token${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Unauthorized Place",
        "description": "Test",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject place creation without token" 401 "$RESPONSE"
echo ""

# TEST 16: Request with invalid token
echo -e "${YELLOW}TEST 16: Request with invalid/malformed token${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer INVALID_TOKEN_12345" \
    -d '{
        "title": "Test Place",
        "description": "Test",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Reject request with invalid token" 422 "$RESPONSE"
echo ""

# ============================================
# DATA INTEGRITY TESTS
# ============================================
echo -e "${BLUE}🔗 DATA INTEGRITY TESTS${NC}"
echo ""

# TEST 17: Create place with non-existent owner_id
echo -e "${YELLOW}TEST 17: Create place with non-existent owner${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Orphan Place",
        "description": "Place with fake owner",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "00000000-0000-0000-0000-000000000000"
    }')

test_case "Reject place with non-existent owner" 404 "$RESPONSE"
echo ""

# TEST 18: Create review for non-existent place
echo -e "${YELLOW}TEST 18: Create review for non-existent place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/reviews/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "text": "Review for ghost place",
        "rating": 5,
        "place_id": "00000000-0000-0000-0000-000000000000",
        "user_id": "'$USER_ID'"
    }')

test_case "Reject review for non-existent place" 404 "$RESPONSE"
echo ""

# TEST 19: Get non-existent user
echo -e "${YELLOW}TEST 19: Get non-existent user by ID${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/users/00000000-0000-0000-0000-000000000000)

test_case "Return 404 for non-existent user" 404 "$RESPONSE"
echo ""

# TEST 20: Get non-existent place
echo -e "${YELLOW}TEST 20: Get non-existent place by ID${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/places/00000000-0000-0000-0000-000000000000)

test_case "Return 404 for non-existent place" 404 "$RESPONSE"
echo ""

# TEST 21: Update non-existent place
echo -e "${YELLOW}TEST 21: Update non-existent place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/places/00000000-0000-0000-0000-000000000000 \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Updated Ghost",
        "description": "Test",
        "price": 100.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "'$USER_ID'"
    }')

test_case "Return 404 for updating non-existent place" 404 "$RESPONSE"
echo ""

# ============================================
# AMENITIES TESTS
# ============================================
echo -e "${BLUE}🛋️  AMENITIES TESTS${NC}"
echo ""

# TEST 22: Create amenity with empty name
echo -e "${YELLOW}TEST 22: Create amenity with empty name${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/amenities/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "name": ""
    }')

test_case "Reject empty amenity name" 400 "$RESPONSE"
echo ""

# TEST 23: Create valid amenity
echo -e "${YELLOW}TEST 23: Create valid amenity${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/amenities/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "name": "Swimming Pool"
    }')

test_case "Create valid amenity" 201 "$RESPONSE"

AMENITY_ID=$(echo "$RESPONSE" | sed '$d' | sed -n 's/.*"id" *: *"\([^"]*\)".*/\1/p')
echo ""

# TEST 24: Try to create duplicate amenity
echo -e "${YELLOW}TEST 24: Create duplicate amenity${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/amenities/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "name": "Swimming Pool"
    }')

test_case "Reject duplicate amenity name" 400 "$RESPONSE"
echo ""

# TEST 25: Regular user tries to create amenity
echo -e "${YELLOW}TEST 25: Regular user tries to create amenity${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/amenities/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "name": "Unauthorized Amenity"
    }')

test_case "Reject non-admin amenity creation" 403 "$RESPONSE"
echo ""

# ============================================
# COMPLEX SCENARIOS
# ============================================
echo -e "${BLUE}🔀 COMPLEX SCENARIOS${NC}"
echo ""

# TEST 26: Create place with multiple amenities (if supported)
echo -e "${YELLOW}TEST 26: Create place and link to amenity${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/places/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "title": "Luxury Villa",
        "description": "Villa with pool",
        "price": 500.0,
        "latitude": 43.7102,
        "longitude": 7.2620,
        "owner_id": "'$USER_ID'",
        "amenities": ["'$AMENITY_ID'"]
    }')

# This test might return 201 or 400 depending on implementation
STATUS=$(echo "$RESPONSE" | tail -n 1)
if [ "$STATUS" -eq 201 ] || [ "$STATUS" -eq 400 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Place with amenities (Status: $STATUS)"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL${NC} - Unexpected status: $STATUS"
    ((FAILED++))
fi
echo ""

# TEST 27: Get reviews for a place
echo -e "${YELLOW}TEST 27: Get all reviews for a place${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/places/$TEST_PLACE_ID/reviews)

test_case "Get place reviews" 200 "$RESPONSE"
echo ""

# TEST 28: User updates their own profile
echo -e "${YELLOW}TEST 28: User updates their own profile${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/users/$USER_ID \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "first_name": "Updated",
        "last_name": "Name",
        "email": "test.complementaire@test.com",
        "password": "test123"
    }')

test_case "User updates own profile" 200 "$RESPONSE"
echo ""

# TEST 29: User tries to update another user's profile
echo -e "${YELLOW}TEST 29: User tries to update another user's profile${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/users/$USER2_ID \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "first_name": "Hacked",
        "last_name": "User",
        "email": "another.user@test.com",
        "password": "test456"
    }')

test_case "Reject user updating another user" 403 "$RESPONSE"
echo ""

# TEST 30: Admin updates any user
echo -e "${YELLOW}TEST 30: Admin updates any user's profile${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT $BASE_URL/users/$USER2_ID \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "first_name": "Admin",
        "last_name": "Updated",
        "email": "another.user@test.com",
        "password": "newpass123"
    }')

test_case "Admin updates any user" 200 "$RESPONSE"
echo ""

# ============================================
# FINAL RESULTS
# ============================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 TEST RESULTS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
echo ""

TOTAL=$((PASSED + FAILED))
if [ $TOTAL -gt 0 ]; then
    PERCENTAGE=$((PASSED * 100 / TOTAL))
    echo -e "Success Rate: ${PERCENTAGE}%"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. Review the output above.${NC}"
    exit 1
fi
