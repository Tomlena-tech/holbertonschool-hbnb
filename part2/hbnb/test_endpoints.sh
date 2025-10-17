#!/bin/bash

# HBnB API - Complete Endpoint Test Suite (Bash/curl version)
# Tests all CRUD operations for Users, Places, Amenities, and Reviews

BASE_URL="http://127.0.0.1:5000/api/v1"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  HBnB API - ENDPOINT TEST SUITE (Bash)${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# =============================================================================
# USER ENDPOINTS
# =============================================================================

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}TESTING USER ENDPOINTS${NC}"
echo -e "${BLUE}============================================================${NC}"

echo -e "\n${YELLOW}Test 1: Create User (POST /users)${NC}"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }')
echo "$USER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo -e "${GREEN}✓ User ID: $USER_ID${NC}"

echo -e "\n${YELLOW}Test 2: Get All Users (GET /users)${NC}"
curl -s -X GET "$BASE_URL/users/" | python3 -m json.tool

echo -e "\n${YELLOW}Test 3: Get User by ID (GET /users/$USER_ID)${NC}"
curl -s -X GET "$BASE_URL/users/$USER_ID" | python3 -m json.tool

echo -e "\n${YELLOW}Test 4: Update User (PUT /users/$USER_ID)${NC}"
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }' | python3 -m json.tool

echo -e "\n${YELLOW}Test 5: Try Duplicate Email (should fail)${NC}"
curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Duplicate",
    "last_name": "User",
    "email": "john.doe@example.com"
  }' | python3 -m json.tool

# =============================================================================
# AMENITY ENDPOINTS
# =============================================================================

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}TESTING AMENITY ENDPOINTS${NC}"
echo -e "${BLUE}============================================================${NC}"

echo -e "\n${YELLOW}Test 1: Create Amenity (POST /amenities)${NC}"
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WiFi"
  }')
echo "$AMENITY_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$AMENITY_RESPONSE"
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo -e "${GREEN}✓ Amenity ID: $AMENITY_ID${NC}"

echo -e "\n${YELLOW}Test 2: Get All Amenities (GET /amenities)${NC}"
curl -s -X GET "$BASE_URL/amenities/" | python3 -m json.tool

echo -e "\n${YELLOW}Test 3: Get Amenity by ID (GET /amenities/$AMENITY_ID)${NC}"
curl -s -X GET "$BASE_URL/amenities/$AMENITY_ID" | python3 -m json.tool

echo -e "\n${YELLOW}Test 4: Update Amenity (PUT /amenities/$AMENITY_ID)${NC}"
curl -s -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High-Speed WiFi"
  }' | python3 -m json.tool

# =============================================================================
# PLACE ENDPOINTS
# =============================================================================

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}TESTING PLACE ENDPOINTS${NC}"
echo -e "${BLUE}============================================================${NC}"

echo -e "\n${YELLOW}Test 1: Create Place (POST /places)${NC}"
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Beautiful Beach House\",
    \"description\": \"A stunning beachfront property\",
    \"price\": 150.00,
    \"latitude\": 34.0522,
    \"longitude\": -118.2437,
    \"owner_id\": \"$USER_ID\"
  }")
echo "$PLACE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo -e "${GREEN}✓ Place ID: $PLACE_ID${NC}"

echo -e "\n${YELLOW}Test 2: Get All Places (GET /places)${NC}"
curl -s -X GET "$BASE_URL/places/" | python3 -m json.tool

echo -e "\n${YELLOW}Test 3: Get Place by ID (GET /places/$PLACE_ID)${NC}"
curl -s -X GET "$BASE_URL/places/$PLACE_ID" | python3 -m json.tool

echo -e "\n${YELLOW}Test 4: Update Place (PUT /places/$PLACE_ID)${NC}"
curl -s -X PUT "$BASE_URL/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Luxury Beach Villa",
    "price": 250.00
  }' | python3 -m json.tool

echo -e "\n${YELLOW}Test 5: Try Invalid Price (should fail)${NC}"
curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Invalid Place\",
    \"description\": \"Should fail\",
    \"price\": -50.00,
    \"latitude\": 34.0522,
    \"longitude\": -118.2437,
    \"owner_id\": \"$USER_ID\"
  }" | python3 -m json.tool

# =============================================================================
# REVIEW ENDPOINTS
# =============================================================================

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}TESTING REVIEW ENDPOINTS${NC}"
echo -e "${BLUE}============================================================${NC}"

echo -e "\n${YELLOW}Test 1: Create Review (POST /reviews)${NC}"
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Amazing place! Highly recommended.\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")
echo "$REVIEW_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$REVIEW_RESPONSE"
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
echo -e "${GREEN}✓ Review ID: $REVIEW_ID${NC}"

echo -e "\n${YELLOW}Test 2: Get All Reviews (GET /reviews)${NC}"
curl -s -X GET "$BASE_URL/reviews/" | python3 -m json.tool

echo -e "\n${YELLOW}Test 3: Get Review by ID (GET /reviews/$REVIEW_ID)${NC}"
curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID" | python3 -m json.tool

echo -e "\n${YELLOW}Test 4: Update Review (PUT /reviews/$REVIEW_ID)${NC}"
curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated: Still amazing!",
    "rating": 5
  }' | python3 -m json.tool

echo -e "\n${YELLOW}Test 5: Delete Review (DELETE /reviews/$REVIEW_ID)${NC}"
curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID"

echo -e "\n${YELLOW}Test 6: Try to Get Deleted Review (should return 404)${NC}"
curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID" | python3 -m json.tool

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${GREEN}✓ TEST SUITE COMPLETED${NC}"
echo -e "${BLUE}============================================================${NC}"
