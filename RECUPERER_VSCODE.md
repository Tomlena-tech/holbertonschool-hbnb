# 📂 Comment récupérer le code dans VSCode

## Méthode 1️⃣ : Depuis le Terminal (RECOMMANDÉ)

### Étape 1 : Ouvrir le Terminal

Sur Mac : `Cmd + Espace` → Tapez "Terminal" → Entrée

### Étape 2 : Aller dans votre projet

```bash
cd /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb
```

### Étape 3 : Récupérer les modifications

```bash
git pull origin claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
```

Vous verrez :
```
Updating a14fb18..9cc38da
Fast-forward
 part3/app/api/v1/amenities.py | 13 +++++++++++++
 part3/app/api/v1/places.py    | 13 +++++++++++++
 part3/app/api/v1/reviews.py   |  5 +++++
 part3/app/api/v1/users.py     | 13 +++++++++++++
 part3/app/services/facade.py  | 34 ++++++++++++++++++++++++++++++++++
 5 files changed, 78 insertions(+)
```

### Étape 4 : Ouvrir dans VSCode

**Option A - Depuis le Terminal :**
```bash
code .
```

**Option B - Depuis VSCode :**
1. Ouvrez VSCode
2. `File` → `Open Folder`
3. Naviguez vers : `/Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb`
4. Cliquez sur "Open"

---

## Méthode 2️⃣ : Directement depuis VSCode

### Étape 1 : Ouvrir votre projet dans VSCode

1. Lancez VSCode
2. `File` → `Open Folder`
3. Sélectionnez : `/Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb`

### Étape 2 : Ouvrir le Terminal intégré

Appuyez sur : `Ctrl + ` ` (backtick) ou `Terminal` → `New Terminal`

### Étape 3 : Récupérer les modifications

Dans le terminal VSCode :
```bash
git pull origin claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
```

### Étape 4 : Vérifier les fichiers modifiés

Dans VSCode, vous verrez les fichiers mis à jour dans l'explorateur :

```
part3/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── users.py         ← MODIFIÉ
│   │       ├── places.py        ← MODIFIÉ
│   │       ├── reviews.py       ← MODIFIÉ
│   │       └── amenities.py     ← MODIFIÉ
│   └── services/
│       └── facade.py            ← MODIFIÉ
```

---

## 🔍 Vérifier que tout est bien récupéré

### Dans le Terminal (VSCode ou Mac) :

```bash
git log --oneline -5
```

Vous devriez voir :
```
9cc38da fix(part3): implement critical business rules...
a14fb18 docs: add quick copy-paste commands file
5fe6014 docs: add simple step-by-step guide...
ee7f12b feat(part3): add missing configuration files
...
```

### Vérifier les fichiers modifiés :

```bash
git show --stat
```

---

## 🚀 Lancer l'application depuis VSCode

### Méthode A : Terminal VSCode

1. Ouvrez le terminal intégré : `Ctrl + ` `
2. Tapez :
```bash
cd part3
python3 run.py
```

### Méthode B : Run Python File

1. Ouvrez `part3/run.py` dans VSCode
2. Clic droit → `Run Python File in Terminal`

Vous verrez :
```
* Running on http://127.0.0.1:5000
```

---

## 🎯 Voir les corrections dans VSCode

### Fichier 1 : `part3/app/services/facade.py`

**Lignes 104-112** - Ownership Check :
```python
# CRITICAL BUSINESS RULE: User cannot review their own place
if place.owner.id == user_id:
    return {'error': 'Cannot review your own place', 'code': 'OWNER_REVIEW'}

# Check for duplicate review (one review per user per place)
existing_reviews = self.review_repo.get_all()
for review in existing_reviews:
    if review.user.id == user_id and review.place.id == place_id:
        return {'error': 'You have already reviewed this place', 'code': 'DUPLICATE_REVIEW'}
```

**Lignes 148-170** - Méthodes DELETE :
```python
def delete_user(self, user_id):
def delete_place(self, place_id):
def delete_amenity(self, amenity_id):
```

### Fichier 2 : `part3/app/api/v1/users.py`

**Lignes 62-73** - Endpoint DELETE :
```python
@api.response(200, 'User deleted successfully')
@api.response(404, 'User not found')
def delete(self, user_id):
    """Delete a user"""
    ...
```

### Fichier 3 : `part3/app/api/v1/places.py`

**Lignes 129-140** - Endpoint DELETE

### Fichier 4 : `part3/app/api/v1/amenities.py`

**Lignes 53-64** - Endpoint DELETE

### Fichier 5 : `part3/app/api/v1/reviews.py`

**Lignes 25-27** - Gestion des erreurs :
```python
# Check if the result is an error (dict with 'error' key)
if isinstance(new_review, dict) and 'error' in new_review:
    return new_review, 400
```

---

## ✅ Checklist finale

- [ ] `git pull` exécuté avec succès
- [ ] Projet ouvert dans VSCode
- [ ] Les 5 fichiers modifiés visibles
- [ ] Application lance sans erreur
- [ ] Swagger accessible sur http://127.0.0.1:5000/api/v1/

---

## 🆘 En cas de problème

### Erreur : "Your local changes would be overwritten"

```bash
git stash
git pull origin claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
git stash pop
```

### Erreur : "fatal: not a git repository"

Vérifiez que vous êtes dans le bon dossier :
```bash
pwd
# Devrait afficher : /Users/thomas/holbertonschool/.../holbertonschool-hbnb
```

### Le code ne marche pas

```bash
# Vérifier la branche
git branch

# Vous devez voir :
# * claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
```

---

## 📞 Commandes rapides

```bash
# Tout en une fois
cd /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb && \
git pull origin claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX && \
code .
```

Puis dans VSCode : `Ctrl + ` ` pour ouvrir le terminal et lancer :
```bash
cd part3 && python3 run.py
```
