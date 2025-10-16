#!/bin/bash

# ============================================
#  SCRIPT DE TEST COMPLET - AMENITIES API
# ============================================

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
API_URL="http://localhost:5000/api/v1/amenities"
TESTS_PASSED=0
TESTS_FAILED=0

# Fonctions
print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_test() {
    echo ""
    echo "[TEST $1] $2"
}

print_success() {
    echo -e "${GREEN}SUCCES${NC} - $1"
    ((TESTS_PASSED++))
}

print_failure() {
    echo -e "${RED}ECHEC${NC} - $1"
    ((TESTS_FAILED++))
}

# ============================================
# DEBUT DES TESTS
# ============================================

print_header "TESTS COMPLETS AMENITIES API"
echo "URL: $API_URL"
echo "Date: $(date)"

# ============================================
# SECTION 1: CREATE
# ============================================

print_header "SECTION 1: CREATE POST"

# TEST 1
print_test "1" "POST - Creer Wi-Fi"
WIFI_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')

echo "$WIFI_RESPONSE"

WIFI_ID=$(echo "$WIFI_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$WIFI_ID" ]; then
    print_success "Wi-Fi cree avec ID: $WIFI_ID"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 2
print_test "2" "POST - Creer Swimming Pool"
POOL_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Swimming Pool"}')

echo "$POOL_RESPONSE"

POOL_ID=$(echo "$POOL_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$POOL_ID" ]; then
    print_success "Swimming Pool cree avec ID: $POOL_ID"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 3
print_test "3" "POST - Creer Parking"
PARKING_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Parking"}')

echo "$PARKING_RESPONSE"

PARKING_ID=$(echo "$PARKING_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$PARKING_ID" ]; then
    print_success "Parking cree avec ID: $PARKING_ID"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 4
print_test "4" "POST - Creer Air Conditioning"
AC_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}')

echo "$AC_RESPONSE"

if echo "$AC_RESPONSE" | grep -q '"id"'; then
    print_success "Air Conditioning cree"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 5
print_test "5" "POST - Creer Gym"
GYM_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Gym"}')

echo "$GYM_RESPONSE"

if echo "$GYM_RESPONSE" | grep -q '"id"'; then
    print_success "Gym cree"
else
    print_failure "Pas d'ID retourne"
fi

# ============================================
# SECTION 2: ERREURS CREATE
# ============================================

print_header "SECTION 2: TESTS ERREURS CREATE"

# TEST 6
print_test "6" "POST - Creer sans nom (devrait echouer)"
ERROR_NO_NAME=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{}')

echo "$ERROR_NO_NAME" | head -n 15

if echo "$ERROR_NO_NAME" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# TEST 7
print_test "7" "POST - Creer avec nom vide (devrait echouer)"
ERROR_EMPTY=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}')

if echo "$ERROR_EMPTY" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# ============================================
# SECTION 3: READ ALL
# ============================================

print_header "SECTION 3: READ ALL GET"

# TEST 8
print_test "8" "GET - Lister toutes les amenities"
ALL_AMENITIES=$(curl -s -X GET $API_URL/)

echo "$ALL_AMENITIES" | python3 -m json.tool 2>/dev/null || echo "$ALL_AMENITIES"

if echo "$ALL_AMENITIES" | grep -q '"id"'; then
    COUNT=$(echo "$ALL_AMENITIES" | grep -o '"id"' | wc -l | tr -d ' ')
    print_success "Liste recuperee - $COUNT amenities"
else
    print_failure "Pas d'amenities retournees"
fi

# TEST 9
print_test "9" "GET - Verifier que Wi-Fi est dans la liste"
if echo "$ALL_AMENITIES" | grep -q "Wi-Fi"; then
    print_success "Wi-Fi trouve"
else
    print_failure "Wi-Fi non trouve"
fi

# ============================================
# SECTION 4: READ ONE
# ============================================

print_header "SECTION 4: READ ONE GET by ID"

# TEST 10
if [ -n "$WIFI_ID" ]; then
    print_test "10" "GET - Recuperer Wi-Fi par ID"
    WIFI_DETAILS=$(curl -s -X GET $API_URL/$WIFI_ID)
    
    echo "$WIFI_DETAILS" | python3 -m json.tool 2>/dev/null || echo "$WIFI_DETAILS"
    
    if echo "$WIFI_DETAILS" | grep -q "Wi-Fi"; then
        print_success "Wi-Fi recupere"
    else
        print_failure "Wi-Fi non recupere"
    fi
else
    print_failure "Pas d'ID Wi-Fi pour ce test"
fi

# TEST 11
if [ -n "$POOL_ID" ]; then
    print_test "11" "GET - Recuperer Swimming Pool par ID"
    POOL_DETAILS=$(curl -s -X GET $API_URL/$POOL_ID)
    
    if echo "$POOL_DETAILS" | grep -q "Swimming Pool"; then
        print_success "Swimming Pool recupere"
    else
        print_failure "Swimming Pool non recupere"
    fi
fi

# ============================================
# SECTION 5: ERREURS READ
# ============================================

print_header "SECTION 5: TESTS ERREURS READ"

# TEST 12
print_test "12" "GET - Amenity inexistante (devrait retourner 404)"
NOT_FOUND=$(curl -i -s -X GET $API_URL/fake-id-12345)

echo "$NOT_FOUND" | head -n 15

if echo "$NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

# ============================================
# SECTION 6: UPDATE
# ============================================

print_header "SECTION 6: UPDATE PUT"

# TEST 13
if [ -n "$WIFI_ID" ]; then
    print_test "13" "PUT - Modifier Wi-Fi en High-Speed Wi-Fi"
    UPDATE_WIFI=$(curl -s -X PUT $API_URL/$WIFI_ID \
      -H "Content-Type: application/json" \
      -d '{"name": "High-Speed Wi-Fi"}')
    
    echo "$UPDATE_WIFI" | python3 -m json.tool 2>/dev/null || echo "$UPDATE_WIFI"
    
    if echo "$UPDATE_WIFI" | grep -q "High-Speed Wi-Fi"; then
        print_success "Wi-Fi mis a jour"
    else
        print_failure "Wi-Fi non mis a jour"
    fi
fi

# TEST 14
if [ -n "$WIFI_ID" ]; then
    print_test "14" "GET - Verifier la modification"
    VERIFY=$(curl -s -X GET $API_URL/$WIFI_ID)
    
    if echo "$VERIFY" | grep -q "High-Speed Wi-Fi"; then
        print_success "Modification persistee"
    else
        print_failure "Modification non persistee"
    fi
fi

# TEST 15
if [ -n "$POOL_ID" ]; then
    print_test "15" "PUT - Modifier Swimming Pool"
    UPDATE_POOL=$(curl -s -X PUT $API_URL/$POOL_ID \
      -H "Content-Type: application/json" \
      -d '{"name": "Olympic Pool"}')
    
    if echo "$UPDATE_POOL" | grep -q "Olympic"; then
        print_success "Swimming Pool mis a jour"
    else
        print_failure "Swimming Pool non mis a jour"
    fi
fi

# ============================================
# SECTION 7: ERREURS UPDATE
# ============================================

print_header "SECTION 7: TESTS ERREURS UPDATE"

# TEST 16
print_test "16" "PUT - Amenity inexistante (devrait retourner 404)"
UPDATE_NOT_FOUND=$(curl -i -s -X PUT $API_URL/fake-id-12345 \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}')

echo "$UPDATE_NOT_FOUND" | head -n 15

if echo "$UPDATE_NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

# ============================================
# SECTION 8: ETAT FINAL
# ============================================

print_header "SECTION 8: ETAT FINAL"

print_test "17" "Liste finale des amenities"
FINAL=$(curl -s -X GET $API_URL/)
echo "$FINAL" | python3 -m json.tool 2>/dev/null || echo "$FINAL"

# ============================================
# RESUME
# ============================================

print_header "RESUME DES TESTS"

TOTAL=$((TESTS_PASSED + TESTS_FAILED))

echo ""
echo "========================================"
echo "Tests reussis: $TESTS_PASSED / $TOTAL"
echo "Tests echoues: $TESTS_FAILED / $TOTAL"
echo "========================================"

if [ $TOTAL -gt 0 ]; then
    PERCENTAGE=$((TESTS_PASSED * 100 / TOTAL))
    echo ""
    echo "Taux de reussite: ${PERCENTAGE}%"
fi

echo ""
echo "Sections testees:"
echo "  - CREATE POST: 5 creations"
echo "  - CREATE errors: 2 tests d'erreurs"
echo "  - READ ALL GET: Liste et verification"
echo "  - READ ONE GET: Recuperation par ID"
echo "  - READ errors: Tests 404"
echo "  - UPDATE PUT: Modifications"
echo "  - UPDATE errors: Tests 404"
echo "  - Etat final du systeme"

echo ""
echo "========================================"
echo "TESTS TERMINES"
echo "========================================"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi
