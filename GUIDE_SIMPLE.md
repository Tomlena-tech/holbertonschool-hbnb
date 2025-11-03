# 🚀 Guide Simple pour Récupérer votre Code

## Étape 1️⃣ : Ouvrir le Terminal

**Sur Mac :**
- Appuyez sur `Cmd + Espace`
- Tapez "Terminal"
- Appuyez sur `Entrée`

---

## Étape 2️⃣ : Aller dans votre dossier projet

Copiez-collez cette commande dans le Terminal :

```bash
cd /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb
```

Appuyez sur `Entrée`

---

## Étape 3️⃣ : Récupérer les nouveaux fichiers

Copiez-collez ces commandes **une par une** :

```bash
git fetch origin
```
Appuyez sur `Entrée`, attendez que ça finisse

```bash
git checkout claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
```
Appuyez sur `Entrée`

```bash
git pull
```
Appuyez sur `Entrée`

---

## Étape 4️⃣ : Vérifier que les fichiers sont là

```bash
ls -la part3/
```

Vous devriez voir :
- ✅ `run.py`
- ✅ `config.py`
- ✅ `requirements.txt`

---

## Étape 5️⃣ : Installer les dépendances

```bash
cd part3
```

Puis :

```bash
pip3 install -r requirements.txt
```

**Si ça ne marche pas**, essayez :

```bash
python3 -m pip install -r requirements.txt
```

---

## Étape 6️⃣ : Lancer l'application

```bash
python3 run.py
```

Vous devriez voir :
```
* Running on http://127.0.0.1:5000
```

---

## Étape 7️⃣ : Tester l'application

Ouvrez votre navigateur et allez sur :

**http://127.0.0.1:5000/api/v1/**

Vous verrez la documentation de l'API ! 🎉

---

## 🆘 Si vous avez une erreur

**Erreur : "command not found: git"**
- Installez Git : https://git-scm.com/download/mac

**Erreur : "No module named 'flask'"**
- Réessayez l'étape 5 avec `python3 -m pip install -r requirements.txt`

**Erreur : "fatal: not a git repository"**
- Vérifiez que vous êtes dans le bon dossier à l'étape 2

---

## 📞 Aide rapide

Toutes les commandes d'un coup (pour copier-coller) :

```bash
cd /Users/thomas/holbertonschool/holbertonschool-hbnb/holbertonschool-hbnb
git fetch origin
git checkout claude/continue-work-011CUjiheSWg4Dj5KXhc1xKX
git pull
cd part3
pip3 install -r requirements.txt
python3 run.py
```

Puis ouvrez : http://127.0.0.1:5000/api/v1/
