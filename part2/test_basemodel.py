#!/usr/bin/python3
"""Test simple de BaseModel"""
print("🧪 Début du test de BaseModel...")

# Importer BaseModel
try:
    from app.models.base_model import BaseModel
    print("✓ Import réussi")
except Exception as e:
    print(f"❌ Erreur d'import: {e}")
    exit(1)

# Test 1: Créer un objet
print("\n1. Création d'un objet...")
try:
    obj = BaseModel()
    print(f"✓ Objet créé")
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

# Test 2: Vérifier l'ID
print("\n2. Test de l'ID...")
try:
    print(f"   ID: {obj.id}")
    print(f"✓ ID existe")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 3: Vérifier created_at
print("\n3. Test de created_at...")
try:
    print(f"   created_at: {obj.created_at}")
    print(f"✓ created_at existe")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 4: Vérifier updated_at
print("\n4. Test de updated_at...")
try:
    print(f"   updated_at: {obj.updated_at}")
    print(f"✓ updated_at existe")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 5: Tester save()
print("\n5. Test de save()...")
try:
    obj.save()
    print(f"✓ save() fonctionne")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 6: Tester update()
print("\n6. Test de update()...")
try:
    obj.update({'test': 'valeur'})
    print(f"✓ update() fonctionne")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 7: Tester to_dict()
print("\n7. Test de to_dict()...")
try:
    d = obj.to_dict()
    print(f"   Résultat: {d}")
    print(f"✓ to_dict() fonctionne")
except Exception as e:
    print(f"❌ to_dict() n'existe pas ou erreur: {e}")

print("\n✅ Tests terminés!")
