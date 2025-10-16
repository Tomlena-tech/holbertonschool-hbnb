#!/bin/bash

echo "========================================="
echo "    TESTS AMENITIES API - HBnB"
echo "========================================="

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. CREATE
echo -e "\n${BLUE}[TEST 1] CREATE - Créer Wi-Fi${NC}"
WIFI_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')
echo "$WIFI_RESPONSE"
WIFI_ID=$(echo $WIFI_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "${GREEN}✓ Wi-Fi créé avec ID: $WIFI_ID${NC}"

echo -e "\n${BLUE}[TEST 2] CREATE - Créer Swimming Pool${NC}"
POOL_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Swimming Pool"}')
echo "$POOL_RESPONSE"
POOL_ID=$(echo $POOL_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo -e "${GREEN}✓ Swimming Pool créé avec ID: $POOL_ID${NC}"

echo -e "\n${BLUE}[TEST 3] CREATE - Créer Parking${NC}"
curl -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Parking"}'
echo -e "${GREEN}✓ Parking créé${NC}"

# 2. READ ALL
echo -e "\n${BLUE}[TEST 4] READ - Lister toutes les amenities${NC}"
curl -s -X GET http://localhost:5000/api/v1/amenities/ | python3 -m json.tool
echo -e "${GREEN}✓ Liste récupérée${NC}"

# 3. READ ONE
echo -e "\n${BLUE}[TEST 5] READ - Récupérer Wi-Fi par ID${NC}"
curl -s -X GET http://localhost:5000/api/v1/amenities/$WIFI_ID | python3 -m json.tool
echo -e "${GREEN}✓ Wi-Fi récupéré${NC}"

# 4. UPDATE
echo -e "\n${BLUE}[TEST 6] UPDATE - Modifier Wi-Fi en High-Speed Wi-Fi${NC}"
curl -s -X PUT http://localhost:5000/api/v1/amenities/$WIFI_ID \
  -H "Content-Type: application/json" \
  -d '{"name": "High-Speed Wi-Fi"}' | python3 -m json.tool
echo -e "${GREEN}✓ Wi-Fi mis à jour${NC}"

# 5. Vérifier la mise à jour
echo -e "\n${BLUE}[TEST 7] READ - Vérifier la modification${NC}"
curl -s -X GET http://localhost:5000/api/v1/amenities/$WIFI_ID | python3 -m json.tool
echo -e "${GREEN}✓ Modification vérifiée${NC}"

# 6. Tests d'erreurs
echo -e "\n${BLUE}[TEST 8] ERROR - Créer sans nom${NC}"
curl -i -s -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{}' | grep "HTTP"
echo -e "${GREEN}✓ Erreur 400 attendue${NC}"

echo -e "\n${BLUE}[TEST 9] ERROR - Amenity inexistante${NC}"
curl -i -s -X GET http://localhost:5000/api/v1/amenities/fake-id-123 | grep "HTTP"
echo -e "${GREEN}✓ Erreur 404 attendue${NC}"

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${GREEN}✓ TOUS LES TESTS TERMINÉS${NC}"
echo -e "${BLUE}=========================================${NC}"
