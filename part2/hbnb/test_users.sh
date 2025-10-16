#!/bin/bash

# ============================================
#  SCRIPT DE TEST COMPLET - USERS API
# ============================================

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

API_URL="http://localhost:5000/api/v1/users"
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

print_header "TESTS COMPLETS USERS API"
echo "URL: $API_URL"
echo "Date: $(date)"

# ============================================
# SECTION 1: CREATE (POST)
# ============================================

print_header "SECTION 1: CREATE POST"

# TEST 1
print_test "1" "POST - Creer utilisateur John Doe"
USER1_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }')

echo "$USER1_RESPONSE"

USER1_ID=$(extract_id "$USER1_RESPONSE")

if [ -n "$USER1_ID" ]; then
    print_success "John Doe cree avec ID: $USER1_ID"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 2
print_test "2" "POST - Creer utilisateur Jane Smith"
USER2_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com"
  }')

echo "$USER2_RESPONSE"

USER2_ID=$(extract_id "$USER2_RESPONSE")

if [ -n "$USER2_ID" ]; then
    print_success "Jane Smith cree avec ID: $USER2_ID"
else
    print_failure "Pas d'ID retourne"
fi

# TEST 3
print_test "3" "POST - Creer utilisateur Bob Martin"
USER3_RESPONSE=$(curl -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Bob",
    "last_name": "Martin",
    "email": "bob.martin@example.com"
  }')

echo "$USER3_RESPONSE"

USER3_ID=$(extract_id "$USER3_RESPONSE")

if [ -n "$USER3_ID" ]; then
    print_success "Bob Martin cree avec ID: $USER3_ID"
else
    print_failure "Pas d'ID retourne"
fi

# ============================================
# SECTION 2: TESTS D'ERREURS CREATE
# ============================================

print_header "SECTION 2: TESTS ERREURS CREATE"

# TEST 4 - Sans email
print_test "4" "POST - Creer sans email (devrait echouer)"
ERROR_NO_EMAIL=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User"
  }')

echo "$ERROR_NO_EMAIL" | head -n 15

if echo "$ERROR_NO_EMAIL" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# TEST 5 - Email invalide
print_test "5" "POST - Creer avec email invalide (devrait echouer)"
ERROR_INVALID_EMAIL=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "invalid-email"
  }')

if echo "$ERROR_INVALID_EMAIL" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# TEST 6 - Email duplique
print_test "6" "POST - Creer avec email duplique (devrait echouer)"
ERROR_DUPLICATE_EMAIL=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Another",
    "last_name": "User",
    "email": "john.doe@example.com"
  }')

if echo "$ERROR_DUPLICATE_EMAIL" | grep -q "409\|400"; then
    print_success "Erreur 400/409 retournee"
else
    print_failure "Devrait retourner 400 ou 409"
fi

# TEST 7 - Sans first_name
print_test "7" "POST - Creer sans first_name (devrait echouer)"
ERROR_NO_FIRSTNAME=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "User",
    "email": "test@example.com"
  }')

if echo "$ERROR_NO_FIRSTNAME" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# TEST 8 - Sans last_name
print_test "8" "POST - Creer sans last_name (devrait echouer)"
ERROR_NO_LASTNAME=$(curl -i -s -X POST $API_URL/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "email": "test2@example.com"
  }')

if echo "$ERROR_NO_LASTNAME" | grep -q "400"; then
    print_success "Erreur 400 retournee"
else
    print_failure "Devrait retourner 400"
fi

# ============================================
# SECTION 3: READ ALL (GET)
# ============================================

print_header "SECTION 3: READ ALL GET"

# TEST 9
print_test "9" "GET - Lister tous les utilisateurs"
ALL_USERS=$(curl -s -X GET $API_URL/)

if echo "$ALL_USERS" | grep -q '"id"'; then
    COUNT=$(echo "$ALL_USERS" | grep -o '"id"' | wc -l | tr -d ' ')
    print_success "Liste recuperee - $COUNT utilisateurs"
    echo "$ALL_USERS" | python3 -m json.tool 2>/dev/null | head -n 30
else
    print_failure "Pas d'utilisateurs retournes"
fi

# TEST 10
print_test "10" "GET - Verifier que John Doe est dans la liste"
if echo "$ALL_USERS" | grep -q "john.doe@example.com"; then
    print_success "John Doe trouve"
else
    print_failure "John Doe non trouve"
fi

# ============================================
# SECTION 4: READ ONE (GET by ID)
# ============================================

print_header "SECTION 4: READ ONE GET by ID"

# TEST 11
if [ -n "$USER1_ID" ]; then
    print_test "11" "GET - Recuperer John Doe par ID"
    USER1_DETAILS=$(curl -s -X GET $API_URL/$USER1_ID)
    
    echo "$USER1_DETAILS" | python3 -m json.tool 2>/dev/null
    
    if echo "$USER1_DETAILS" | grep -q "john.doe@example.com"; then
        print_success "John Doe recupere"
    else
        print_failure "John Doe non recupere"
    fi
else
    print_test "11" "GET - Recuperer John Doe"
    print_failure "Pas d'ID John Doe pour ce test"
fi

# TEST 12
if [ -n "$USER2_ID" ]; then
    print_test "12" "GET - Recuperer Jane Smith par ID"
    USER2_DETAILS=$(curl -s -X GET $API_URL/$USER2_ID)
    
    if echo "$USER2_DETAILS" | grep -q "jane.smith@example.com"; then
        print_success "Jane Smith recupere"
    else
        print_failure "Jane Smith non recupere"
    fi
else
    print_test "12" "GET - Recuperer Jane Smith"
    print_failure "Pas d'ID Jane Smith pour ce test"
fi

# ============================================
# SECTION 5: TESTS D'ERREURS READ
# ============================================

print_header "SECTION 5: TESTS ERREURS READ"

# TEST 13
print_test "13" "GET - Utilisateur inexistant (devrait retourner 404)"
NOT_FOUND=$(curl -i -s -X GET $API_URL/fake-id-12345)

echo "$NOT_FOUND" | head -n 15

if echo "$NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

# ============================================
# SECTION 6: UPDATE (PUT)
# ============================================

print_header "SECTION 6: UPDATE PUT"

# TEST 14
if [ -n "$USER1_ID" ]; then
    print_test "14" "PUT - Modifier John Doe"
    UPDATE_USER1=$(curl -s -X PUT $API_URL/$USER1_ID \
      -H "Content-Type: application/json" \
      -d '{
        "first_name": "Johnny",
        "last_name": "Doe",
        "email": "john.doe@example.com"
      }')
    
    echo "$UPDATE_USER1" | python3 -m json.tool 2>/dev/null
    
    if echo "$UPDATE_USER1" | grep -q "Johnny"; then
        print_success "John Doe mis a jour en Johnny"
    else
        print_failure "Mise a jour echouee"
    fi
else
    print_test "14" "PUT - Modifier John Doe"
    print_failure "Pas d'ID pour ce test"
fi

# TEST 15
if [ -n "$USER1_ID" ]; then
    print_test "15" "GET - Verifier la modification de John Doe"
    VERIFY_UPDATE=$(curl -s -X GET $API_URL/$USER1_ID)
    
    if echo "$VERIFY_UPDATE" | grep -q "Johnny"; then
        print_success "Modification persistee"
    else
        print_failure "Modification non persistee"
    fi
else
    print_test "15" "GET - Verifier modification"
    print_failure "Pas d'ID pour ce test"
fi

# TEST 16
if [ -n "$USER2_ID" ]; then
    print_test "16" "PUT - Modifier email de Jane Smith"
    UPDATE_USER2=$(curl -s -X PUT $API_URL/$USER2_ID \
      -H "Content-Type: application/json" \
      -d '{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.s@example.com"
      }')
    
    if echo "$UPDATE_USER2" | grep -q "jane.s@example.com"; then
        print_success "Email de Jane mis a jour"
    else
        print_failure "Mise a jour email echouee"
    fi
fi

# ============================================
# SECTION 7: TESTS D'ERREURS UPDATE
# ============================================

print_header "SECTION 7: TESTS ERREURS UPDATE"

# TEST 17
print_test "17" "PUT - Utilisateur inexistant (devrait retourner 404)"
UPDATE_NOT_FOUND=$(curl -i -s -X PUT $API_URL/fake-id-12345 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com"
  }')

echo "$UPDATE_NOT_FOUND" | head -n 15

if echo "$UPDATE_NOT_FOUND" | grep -q "404"; then
    print_success "Erreur 404 retournee"
else
    print_failure "Devrait retourner 404"
fi

# TEST 18
if [ -n "$USER1_ID" ]; then
    print_test "18" "PUT - Modifier avec email invalide (devrait echouer)"
    UPDATE_INVALID_EMAIL=$(curl -i -s -X PUT $API_URL/$USER1_ID \
      -H "Content-Type: application/json" \
      -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email"
      }')
    
    if echo "$UPDATE_INVALID_EMAIL" | grep -q "400"; then
        print_success "Erreur 400 retournee"
    else
        print_failure "Devrait retourner 400"
    fi
fi

# ============================================
# SECTION 8: VALIDATION DES CHAMPS
# ============================================

print_header "SECTION 8: VALIDATION DES CHAMPS"

# TEST 19
if [ -n "$USER1_ID" ]; then
    print_test "19" "Verifier presence de created_at et updated_at"
    USER_TIMESTAMPS=$(curl -s -X GET $API_URL/$USER1_ID)
    
    if echo "$USER_TIMESTAMPS" | grep -q "created_at" && echo "$USER_TIMESTAMPS" | grep -q "updated_at"; then
        print_success "Timestamps presents"
    else
        print_failure "Timestamps manquants"
    fi
fi

# TEST 20
if [ -n "$USER1_ID" ]; then
    print_test "20" "Verifier format UUID de l'ID"
    
    if [[ $USER1_ID =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]]; then
        print_success "ID est un UUID valide"
    else
        print_failure "ID n'est pas un UUID valide"
    fi
fi

# ============================================
# SECTION 9: ETAT FINAL
# ============================================

print_header "SECTION 9: ETAT FINAL"

print_test "21" "Liste finale des utilisateurs"
FINAL_USERS=$(curl -s -X GET $API_URL/)
echo "$FINAL_USERS" | python3 -m json.tool 2>/dev/null

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
echo "  - CREATE POST: Creations reussies"
echo "  - CREATE errors: Validations"
echo "  - READ ALL GET: Liste complete"
echo "  - READ ONE GET: Recuperation par ID"
echo "  - READ errors: Tests 404"
echo "  - UPDATE PUT: Modifications"
echo "  - UPDATE errors: Validations"
echo "  - Validation des champs"
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
