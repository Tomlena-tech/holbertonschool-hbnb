#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

API_URL="http://localhost:5000/api/v1/amenities"
TESTS_PASSED=0
TESTS_FAILED=0

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

# Fonction pour extraire l'ID du JSON
extract_id() {
    echo "$1" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null
}

print_header "TESTS AMENITIES API"
echo "URL: $API_URL"

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

WIFI_ID=$(extract_id "$WIFI_RESPONSE")

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

POOL_ID=$(extract_id "$POOL_RESPONSE")

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

PARKING_ID=$(extract_id "$PARKING_RESPONSE")

if [ -n "$PARKING_ID" ]; then
    print_success "Parking cree avec ID: $PARKING_ID"
else
    print_failure "Pas d'ID retourne"
fi

# ============================================
# SECTION 2: ERREURS CREATE
# ============================================

print_header "SECTION 2: TESTS ERREURS CREATE"

# TEST 4
print_test "4" "POST - Creer sans nom (devrait echouer)"
ERROR_NO_NAME=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{}')

if echo "$ERROR_NO_NAME" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# TEST 5
print_test "5" "POST - Creer avec nom vide (devrait echouer)"
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

# TEST 6
print_test "6" "GET - Lister toutes les amenities"
ALL_AMENITIES=$(curl -s -X GET $API_URL/)

if echo "$ALL_AMENITIES" | grep -q '"id"'; then
    COUNT=$(echo "$ALL_AMENITIES" | grep -o '"id"' | wc -l | tr -d ' ')
    print_success "Liste recuperee - $COUNT amenities"
else
    print_failure "Pas d'amenities retournees"
fi

# ============================================
# SECTION 4: READ ONE
# ============================================

print_header "SECTION 4: READ ONE GET by ID"

# TEST 7
if [ -n "$WIFI_ID" ]; then
    print_test "7" "GET - Recuperer Wi-Fi par ID: $WIFI_ID"
    WIFI_DETAILS=$(curl -s -X GET $API_URL/$WIFI_ID)
    
    if echo "$WIFI_DETAILS" | grep -q "Wi-Fi"; then
        print_success "Wi-Fi recupere"
    else
        print_failure "Wi-Fi non recupere"
    fi
else
    print_test "7" "GET - Recuperer Wi-Fi"
    print_failure "Pas d'ID Wi-Fi pour ce test"
fi

# TEST 8
if [ -n "$POOL_ID" ]; then
    print_test "8" "GET - Recuperer Swimming Pool par ID: $POOL_ID"
    POOL_DETAILS=$(curl -s -X GET $API_URL/$POOL_ID)
    
    if echo "$POOL_DETAILS" | grep -q "Swimming Pool"; then
        print_success "Swimming Pool recupere"
    else
        print_failure "Swimming Pool non recupere"
    fi
else
    print_test "8" "GET - Recuperer Swimming Pool"
    print_failure "Pas d'ID Pool pour ce test"
fi

# ============================================
# SECTION 5: ERREURS READ
# ============================================

print_header "SECTION 5: TESTS ERREURS READ"

# TEST 9
print_test "9" "GET - Amenity inexistante (devrait retourner 404)"
NOT_FOUND=$(curl -i -s -X GET $API_URL/fake-id-12345)

if echo "$NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

# ============================================
# SECTION 6: UPDATE
# ============================================

print_header "SECTION 6: UPDATE PUT"

# TEST 10
if [ -n "$WIFI_ID" ]; then
    print_test "10" "PUT - Modifier Wi-Fi en High-Speed Wi-Fi"
    UPDATE_WIFI=$(curl -s -X PUT $API_URL/$WIFI_ID \
      -H "Content-Type: application/json" \
      -d '{"name": "High-Speed Wi-Fi"}')
    
    if echo "$UPDATE_WIFI" | grep -q "High-Speed Wi-Fi"; then
        print_success "Wi-Fi mis a jour"
    else
        print_failure "Wi-Fi non mis a jour"
    fi
else
    print_test "10" "PUT - Modifier Wi-Fi"
    print_failure "Pas d'ID Wi-Fi pour ce test"
fi

# TEST 11
if [ -n "$WIFI_ID" ]; then
    print_test "11" "GET - Verifier la modification"
    VERIFY=$(curl -s -X GET $API_URL/$WIFI_ID)
    
    if echo "$VERIFY" | grep -q "High-Speed Wi-Fi"; then
        print_success "Modification persistee"
    else
        print_failure "Modification non persistee"
    fi
else
    print_test "11" "GET - Verifier modification"
    print_failure "Pas d'ID Wi-Fi pour ce test"
fi

# ============================================
# SECTION 7: ERREURS UPDATE
# ============================================

print_header "SECTION 7: TESTS ERREURS UPDATE"

# TEST 12
print_test "12" "PUT - Amenity inexistante (devrait retourner 404)"
UPDATE_NOT_FOUND=$(curl -i -s -X PUT $API_URL/fake-id-12345 \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}')

if echo "$UPDATE_NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

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
echo "========================================"
echo "TESTS TERMINES"
echo "========================================"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi
